import json
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import requests
import streamlit as st

st.set_page_config(
    page_title="Dashboard Analyste & Value Bets", layout="wide", page_icon="⚽"
)

# ---------------------------------------------------------
# CONFIGURATION ET CHARGEMENT DES DONNÉES LOCALES
# ---------------------------------------------------------
API_KEY_ODDS = "6156984daef9e8e6ebe18b31d0afa411"  # Remplace par ta clé The Odds API


@st.cache_data(ttl=0)
def load_real_data():
  try:
    with open("data_5_leagues.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception as e:
    st.error(f"⚠ Impossible de lire 'data_5_leagues.json' : {e}")
    return None


all_data = load_real_data()

if not all_data:
  st.warning("Fichier de données introuvable sur GitHub.")
  st.stop()

# Match des ligues pour l'API The Odds API
LEAGUE_API_MAP = {
    "Premier League": "soccer_epl",
    "Ligue 1": "soccer_france_ligue_one",
    "LaLiga": "soccer_spain_la_liga",
    "Bundesliga": "soccer_germany_bundesliga",
    "Serie A": "soccer_italy_serie_a",
}

# ---------------------------------------------------------
# FONCTION : RECUPÉRATION DES COTES EN TEMPS RÉEL
# ---------------------------------------------------------
@st.cache_data(ttl=300)  # Cache de 5 minutes pour préserver les requêtes API
def fetch_live_odds(sport_key):
  if API_KEY_ODDS == "TA_CLE_API_ICI":
    return None

  url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
  params = {
      "apiKey": API_KEY_ODDS,
      "regions": "eu",
      "markets": "h2h",  # Cotes 1N2
      "bookmakers": "pinnacle,unibet_eu",  # Pinnacle & Kambi (Unibet)
  }
  try:
    response = requests.get(url, params=params)
    if response.status_code == 200:
      return response.json()
  except Exception:
    pass
  return None


# ---------------------------------------------------------
# INTERFACE PRINCIPALE : NAVIGATION
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "Navigation", ["Comparateur 1v1", "🎯 Value Bets Temps Réel"]
)

all_teams_list = []
for league_name, teams in all_data.items():
  for t in teams:
    t["Ligue"] = league_name
    all_teams_list.append(t)
team_names_sorted = sorted([t["Équipe"] for t in all_teams_list])

# ---------------------------------------------------------
# MODULE 1 : COMPARATEUR 1V1
# ---------------------------------------------------------
if menu == "Comparateur 1v1":
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

# ---------------------------------------------------------
# MODULE 2 : DÉTECTEUR DE VALUE BETS TEMPS RÉEL
# ---------------------------------------------------------
elif menu == "🎯 Value Bets Temps Réel":
  st.title("🎯 Détecteur de Value Bets (Pinnacle vs Kambi)")

  selected_league = st.selectbox(
      "Sélectionner la Ligue à analyser", list(LEAGUE_API_MAP.keys())
  )
  sport_key = LEAGUE_API_MAP[selected_league]

  if API_KEY_ODDS == "TA_CLE_API_ICI":
    st.info(
        "💡 Colle ta clé API The Odds API à la ligne 12 du code `app.py` pour"
        " activer l'injection en temps réel."
    )

  if st.button("🔄 Charger les cotes live"):
    st.cache_data.clear()

  live_matches = fetch_live_odds(sport_key)

  if not live_matches:
    st.warning("Aucune cote en temps réel disponible pour le moment.")
  else:
    value_bets_found = []

    for match in live_matches:
      home_team = match["home_team"]
      away_team = match["away_team"]

      # Recherche des données xG locales
      h_data = next(
          (
              t
              for t in all_data.get(selected_league, [])
              if t["Équipe"] in home_team or home_team in t["Équipe"]
          ),
          None,
      )
      a_data = next(
          (
              t
              for t in all_data.get(selected_league, [])
              if t["Équipe"] in away_team or away_team in t["Équipe"]
          ),
          None,
      )

      if h_data and a_data:
        # Probabilité estimée via le ratio xG
        prob_home = max(
            min(h_data["xG"] / (h_data["xG"] + a_data["xGA"] + 0.1), 0.85), 0.15
        )
        fair_odd_home = round(1 / prob_home, 2)

        # Extrait les cotes Pinnacle et Kambi (Unibet)
        pin_odd, kambi_odd = None, None
        for bm in match.get("bookmakers", []):
          if bm["key"] == "pinnacle":
            pin_odd = bm["markets"][0]["outcomes"][0]["price"]
          elif bm["key"] == "unibet_eu":
            kambi_odd = bm["markets"][0]["outcomes"][0]["price"]

        # Calcul des Expected Values
        ev_pin = (
            round(((prob_home * pin_odd) - 1) * 100, 2) if pin_odd else -999
        )
        ev_kambi = (
            round(((prob_home * kambi_odd) - 1) * 100, 2) if kambi_odd else -999
        )

        value_bets_found.append({
            "Match": f"{home_team} vs {away_team}",
            "Cote Équitable Model": fair_odd_home,
            "Cote Pinnacle": pin_odd if pin_odd else "N/A",
            "EV Pinnacle (%)": f"{ev_pin}%" if pin_odd else "N/A",
            "Cote Kambi (Unibet)": kambi_odd if kambi_odd else "N/A",
            "EV Kambi (%)": f"{ev_kambi}%" if kambi_odd else "N/A",
            "Détection Value": (
                "🔥 EXCELLENT VALUE"
                if ev_kambi > 5.0 or ev_pin > 5.0
                else ("✅ VALUE" if ev_kambi > 2.0 or ev_pin > 2.0 else "❌ OK")
            ),
        })

    if value_bets_found:
      st.dataframe(value_bets_found, use_container_width=True)
    else:
      st.info("Aucune opportunité détectée sur cette ligue.")
