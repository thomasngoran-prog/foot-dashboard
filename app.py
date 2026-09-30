import json
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import streamlit as st

st.set_page_config(
    page_title="Dashboard Analyste & Comparateur", layout="wide", page_icon="⚽"
)


# 1. Chargement des données
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
  st.warning(
      "Fichier 'data_5_leagues.json' introuvable. Vérifie le déploiement GitHub."
  )
  st.stop()

# Structuration de la liste globale de toutes les équipes
all_teams_list = []
for league_name, teams in all_data.items():
  for t in teams:
    t["Ligue"] = league_name
    all_teams_list.append(t)

team_names_sorted = sorted([t["Équipe"] for t in all_teams_list])

st.title("⚽ Comparateur Tactique 1v1")

# 2. Sélecteurs d'équipes côte à côte
col_sel1, col_sel2 = st.columns(2)

with col_sel1:
  team1_name = st.selectbox(
      "Sélectionner Équipe 1 (Bleu)", team_names_sorted, index=0, key="t1_select"
  )
with col_sel2:
  default_idx = 1 if len(team_names_sorted) > 1 else 0
  team2_name = st.selectbox(
      "Sélectionner Équipe 2 (Rouge)",
      team_names_sorted,
      index=default_idx,
      key="t2_select",
  )

t1 = next(t for t in all_teams_list if t["Équipe"] == team1_name)
t2 = next(t for t in all_teams_list if t["Équipe"] == team2_name)

st.markdown("---")

# 3. Métriques clés comparées
st.subheader("📊 Comparaison des Métriques Clés (par match)")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
  st.metric("Championnat", f"{t1['Ligue']}", f"vs {t2['Ligue']}")

with c2:
  diff_m = t1.get("Matchs", 0) - t2.get("Matchs", 0)
  st.metric("Matchs Joués", t1.get("Matchs", 0), delta=f"{diff_m} vs T2")

with c3:
  diff_xg = round(t1.get("xG", 0.0) - t2.get("xG", 0.0), 2)
  st.metric("xG Marqués", t1.get("xG", 0.0), delta=diff_xg)

with c4:
  # xGA : une valeur plus basse est meilleure
  diff_xga = round(t2.get("xGA", 0.0) - t1.get("xGA", 0.0), 2)
  st.metric("xGA Concédés", t1.get("xGA", 0.0), delta=diff_xga)

with c5:
  # PPDA : une valeur plus basse = pressing plus intense
  diff_ppda = round(t2.get("PPDA", 0.0) - t1.get("PPDA", 0.0), 2)
  st.metric("PPDA (Pressing)", t1.get("PPDA", 0.0), delta=diff_ppda)

st.markdown("---")

# 4. Profil Radar PyPizza
st.subheader("🕸️ Profil Radar Tactique")

# Axes d'analyse
params = [
    "xG (Attaque)",
    "SCA (Création)",
    "GS (Buts)",
    "PPDA (Pressing)",
    "xGA (Défense)",
    "xC (Corners)",
]

# Initialisation du générateur PyPizza
baker = PyPizza(
    params=params,
    straight_line_color="#444444",
    straight_line_lw=1,
    last_circle_lw=1,
    other_circle_lw=1,
    other_circle_ls="--",
)

# Génération des données radar (fallback si la liste radar est incomplète)
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

# Légende et style sombre
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
