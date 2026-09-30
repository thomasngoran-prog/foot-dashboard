import json
import streamlit as st

st.set_page_config(
    page_title="Dashboard Data Football", layout="wide", page_icon="⚽"
)


# 1. Chargement strict du fichier JSON
@st.cache_data(ttl=0)  # Désactive le cache pour forcer la lecture directe
def load_real_data():
  try:
    with open("data_5_leagues.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception as e:
    st.error(f"⚠️️ Impossible de lire 'data_5_leagues.json' : {e}")
    return None


all_data = load_real_data()

if all_data is None:
  st.warning(
    "Vérifie que le fichier 'data_5_leagues.json' est bien présent à la racine"
    " de ton dépôt GitHub."
  )
  st.stop()

# 2. Interface utilisateur
st.title("⚽ Dashboard Analyste - 5 Grands Championnats (2026/2027)")

# Sélection du championnat
league_names = list(all_data.keys())
selected_league = st.sidebar.selectbox("Choisir une Ligue", league_names)

# Liste des équipes réelles
teams_list = all_data[selected_league]
team_names = [t["Équipe"] for t in teams_list]

selected_team_name = st.sidebar.selectbox("Choisir une Équipe", team_names)

# Récupération des données de l'équipe sélectionnée
team_data = next(
    t for t in teams_list if t["Équipe"] == selected_team_name
)

# 3. Affichage des métriques réelles
st.header(f"📊 {selected_team_name} ({selected_league})")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Matchs Joués", team_data.get("Matchs", 0))
col2.metric("xG / match", team_data.get("xG", 0.0))
col3.metric("xGA / match", team_data.get("xGA", 0.0))
col4.metric("PPDA", team_data.get("PPDA", 0.0))

# Affichage du tableau complet de la ligue
st.subheader(f"Classement Data - {selected_league}")
st.dataframe(teams_list, use_container_width=True)
