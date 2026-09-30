import json
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Dashboard Analyste & Value Bets Global",
    layout="wide",
    page_icon="⚽",
)

# ---------------------------------------------------------
# CONFIGURATION & CLE API
# ---------------------------------------------------------
API_KEY_ODDS = "TA_CLE_API_ICI"  # Remplace par ta clé The Odds API

LEAGUES_MAP = {
    "Premier League": "soccer_epl",
    "Ligue 1": "soccer_france_ligue_one",
    "LaLiga": "soccer_spain_la_liga",
    "Bundesliga": "soccer_germany_bundesliga",
    "Serie A": "soccer_italy_serie_a",
}


# ---------------------------------------------------------
# CHARGEMENT DES DONNÉES LOCALES
# ---------------------------------------------------------
@st.cache_data(ttl=0)
def load_real_data():
  try:
    with open("data_5_leagues.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception as e:
    st.error(f"⚠ Erreur de lecture de 'data_5_leagues.json' : {e}")
    return None


all_data = load_real_data()

if not all_data:
  st.warning("Fichier 'data_5_leagues.json' introuvable.")
  st.stop()


# ---------------------------------------------------------
# REQUÊTES API ODDS TEMPS RÉEL (Pinnacle + Kambi)
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def fetch_league_odds(sport_key):
  if API_KEY_ODDS == "TA_CLE_API_ICI":
    return None
  url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
  params = {
      "apiKey": API_KEY_ODDS,
      "regions": "eu",
      "markets": "h2h",
      "bookmakers": "pinnacle,unibet_eu",  # unibet_eu représente Kambi
  }
  try:
    res = requests.get(url, params=params)
    if res.status_code == 200:
      return res.json()
  except Exception:
    pass
  return None


def match_team_name(api_name, local_teams):
  """Trouve l'équipe correspondante dans le fichier local avec vérification stricte."""
  api_name_clean = api_name.lower().replace(" ", "").replace("fc", "")
  for t in local_teams:
    local_name_clean = t["Équipe"].lower().replace(" ", "").replace("fc", "")
    if (
        api_name_clean in local_name_clean
        or local_name_clean in api_name_clean
    ):
      return t
  return None


# ---------------------------------------------------------
# NAVIGATION SIDEBAR
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "Navigation", ["🔥 Scanner Value Bets Global", "⚽ Comparateur 1v1"]
)

all_teams_list = []
for league_name, teams in all_data.items():
  for t in teams:
    t["Ligue"] = league_name
    all_teams_list.append(t)
team_names_sorted = sorted([t["Équipe"] for t in all_teams_list])

# ---------------------------------------------------------
# MODULE 1 : SCANNER VALUE BETS
# ---------------------------------------------------------
if menu == "🔥 Scanner Value Bets Global":
  st.title("🔥 Scanner de Value Bets Multi-Championnats")

  col_b1, col_b2 = st.columns([1, 4])
  with col_b1:
    btn_scan = st.button("🔄 Lancer le Scan Global")
  with col_b2:
    min_ev = st.slider(
        "Seuil d'Expected Value minimale (%)",
        min_value=1.0,
        max_value=15.0,
        value=3.0,
        step=0.5,
    )

  if btn_scan:
    st.cache_data.clear()

  all_value_bets = []

  with st.spinner("Analyse précise des cotes et métriques en cours..."):
    for league_name, sport_key in LEAGUES_MAP.items():
      matches = fetch_league_odds(sport_key)
      if not matches:
        continue

      league_teams = all_data.get(league_name, [])

      for match in matches:
        home_team_api = match["home_team"]
        away_team_api = match["away_team"]

        h_data = match_team_name(home_team_api, league_teams)
        a_data = match_team_name(away_team_api, league_teams)

        # On n'analyse que si les DEUX équipes sont correctement identifiées
        if h_data and a_data:
          # Estimation xG de la puissance relative
          xg_h = h_data.get("xG", 1.2)
          xga_a = a_data.get("xGA", 1.2)

          # Estimation de probabilité ajustée avec avantage domicile (+15%)
          lambda_home = xg_h * (xga_a / 1.2) * 1.15
          prob_home = min(max(lambda_home / (lambda_home + 1.2), 0.15), 0.85)

          fair_odd = round(1 / prob_home, 2)

          pin_odd, kambi_odd = None, None
          for bm in match.get("bookmakers", []):
            if bm["key"] == "pinnacle":
              for outcome in bm["markets"][0]["outcomes"]:
                if outcome["name"] == home_team_api:
                  pin_odd = outcome["price"]
            elif bm["key"] == "unibet_eu":
              for outcome in bm["markets"][0]["outcomes"]:
                if outcome["name"] == home_team_api:
                  kambi_odd = outcome["price"]

          ev_pin = (
              round(((prob_home * pin_odd) - 1) * 100, 2) if pin_odd else -999
          )
          ev_kambi = (
              round(((prob_home * kambi_odd) - 1) * 100, 2)
              if kambi_odd
              else -999
          )

          # Filtre anti-erreur : On exclut les EV aberrantes (> 35%)
          valid_pin = min_ev <= ev_pin <= 35.0
          valid_kambi = min_ev <= ev_kambi <= 35.0

          if valid_pin or valid_kambi:
            all_value_bets.append({
                "Ligue": league_name,
                "Match": f"{home_team_api} vs {away_team_api}",
                "Cote Modèle": fair_odd,
                "Cote Pinnacle": pin_odd if pin_odd else "-",
                "EV Pinnacle (%)": f"+{ev_pin}%" if valid_pin else "-",
                "Cote Kambi": kambi_odd if kambi_odd else "-",
                "EV Kambi (%)": f"+{ev_kambi}%" if valid_kambi else "-",
                "Best EV": max(
                    ev_pin if valid_pin else -999,
                    ev_kambi if valid_kambi else -999,
                ),
            })

  if all_value_bets:
    df_val = pd.DataFrame(all_value_bets)
    df_val = df_val.sort_values(by="Best EV", ascending=False).drop(
        columns=["Best EV"]
    )
    st.success(f"🎉 {len(df_val)} opportunités Value réalistes détectées !")
    st.dataframe(df_val, use_container_width=True)
  else:
    st.info(
        "Aucune opportunité Value ne respecte les critères de sécurité"
        " actuellement."
    )

# ---------------------------------------------------------
# MODULE 2 : COMPARATEUR 1V1
# ---------------------------------------------------------
elif menu == "⚽ Comparateur 1v1":
  st.title("⚽ Comparateur Tactique 1v1")

  col_sel1, col_sel2 = st.columns(2)
  with col_sel1:
    team1_name = st.selectbox(
        "Équipe 1 (Bleu)", team_names_sorted, index=0, key="t1_select"
    )
  with col_sel2:
    default_idx = 1 if len(team_names_sorted) > 1 else 0
    team2_name = st.selectbox(
        "Équipe 2 (Rouge)",
        team_names_sorted,
        index=default_idx,
        key="t2_select",
    )

  t1 = next(t for t in all_teams_list if t["Équipe"] == team1_name)
  t2 = next(t for t in all_teams_list if t["Équipe"] == team2_name)

  st.markdown("---")
  st.subheader("📊 Métriques Clés (par match)")

  c1, c2, c3, c4, c5 = st.columns(5)
  c1.metric("Championnat", f"{t1['Ligue']}", f"vs {t2['Ligue']}")
  c2.metric(
      "Matchs", t1.get("Matchs", 0), delta=t1.get("Matchs", 0) - t2.get("Matchs", 0)
  )
  c3.metric(
      "xG Marqués",
      t1.get("xG", 0.0),
      delta=round(t1.get("xG", 0.0) - t2.get("xG", 0.0), 2),
  )
  c4.metric(
      "xGA Concédés",
      t1.get("xGA", 0.0),
      delta=round(t2.get("xGA", 0.0) - t1.get("xGA", 0.0), 2),
  )
  c5.metric(
      "PPDA (Pressing)",
      t1.get("PPDA", 0.0),
      delta=round(t2.get("PPDA", 0.0) - t1.get("PPDA", 0.0), 2),
  )

  st.markdown("---")
  st.subheader("🕸️ Radar Tactique")

  params_pizza = [
      "xG (Attaque)",
      "SCA (Création)",
      "GS (Buts)",
      "PPDA (Pressing)",
      "xGA (Défense)",
      "xC (Corners)",
  ]
  baker = PyPizza(
      params=params_pizza,
      straight_line_color="#444444",
      straight_line_lw=1,
      last_circle_lw=1,
      other_circle_lw=1,
      other_circle_ls="--",
  )

  r1 = t1.get("radar", [50, 50, 50, 50, 50, 50])
  r2 = t2.get("radar", [50, 50, 50, 50, 50, 50])

  fig, ax = baker.make_pizza(
      r1,
      compare_values=r2,
      figsize=(8, 8),
      param_location=110,
      kwargs_slices=dict(
          facecolor="#1A78CF", edgecolor="#000000", zorder=2, alpha=0.6
      ),
      kwargs_compare=dict(
          facecolor="#FF4B4B", edgecolor="#000000", zorder=2, alpha=0.6
      ),
      kwargs_params=dict(color="#FFFFFF", fontsize=11, va="center"),
      kwargs_values=dict(
          color="#FFFFFF",
          fontsize=10,
          zorder=3,
          bbox=dict(
              edgecolor="#1A78CF",
              facecolor="#1A78CF",
              boxstyle="round,pad=0.2",
              lw=1,
          ),
      ),
      kwargs_compare_values=dict(
          color="#FFFFFF",
          fontsize=10,
          zorder=3,
          bbox=dict(
              edgecolor="#FF4B4B",
              facecolor="#FF4B4B",
              boxstyle="round,pad=0.2",
              lw=1,
          ),
      ),
  )

  fig.text(
      0.22,
      0.95,
      f"■ {t1['Équipe']} ({t1['Ligue']})",
      size=13,
      color="#1A78CF",
      weight="bold",
  )
  fig.text(
      0.60,
      0.95,
      f"■ {t2['Équipe']} ({t2['Ligue']})",
      size=13,
      color="#FF4B4B",
      weight="bold",
  )
  fig.patch.set_facecolor("#0E1117")
  ax.set_facecolor("#0E1117")

  st.pyplot(fig)
