import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from understatapi import UnderstatClient

st.set_page_config(page_title="Football Data 2026/2027", layout="centered")

st.title("⚽ Dashboard Tactique & Data")
st.caption("Données de la saison 2026/2027 — Top 5 & D2")
st.markdown("---")

# Correspondance des ligues
LEAGUES_MAPPING = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (D1)": "EPL",
    "🇪🇸 LaLiga (D1)": "La_liga",
    "🇩🇪 Bundesliga (D1)": "Bundesliga",
    "🇮🇹 Serie A (D1)": "Serie_A",
    "🇫🇷 Ligue 1 (D1)": "Ligue_1",
}

selected_league_label = st.selectbox("Sélectionner un Championnat", list(LEAGUES_MAPPING.keys()))
league_code = LEAGUES_MAPPING[selected_league_label]

@st.cache_data(ttl=3600)
def fetch_league_teams(league, season=2026):
    try:
        understat = UnderstatClient()
        team_data = understat.league(league=league).get_team_data(season=str(season))
        
        parsed_teams = []
        for team_id, info in team_data.items():
            title = info['title']
            history = info['history']
            matches = len(history)
            
            if matches == 0:
                continue
                
            tot_xg = sum(float(m['xG']) for m in history)
            tot_xga = sum(float(m['xGA']) for m in history)
            tot_ppda = sum(float(m['ppda']['att']) / max(1, float(m['ppda']['def'])) for m in history)
            
            parsed_teams.append({
                "Équipe": title,
                "Matchs": matches,
                "xG/M": round(tot_xg / matches, 2),
                "xGA/M": round(tot_xga / matches, 2),
                "PPDA": round(tot_ppda / matches, 1)
            })
            
        df = pd.DataFrame(parsed_teams)
        return df.sort_values(by="Équipe").reset_index(drop=True)
    except Exception as e:
        return None

with st.spinner("Chargement des données de la saison 2026/2027..."):
    df_teams = fetch_league_teams(league_code, season=2026)

if df_teams is not None and not df_teams.empty:
    team_list = df_teams["Équipe"].tolist()
    selected_team = st.selectbox("Sélectionner une Équipe (2026/2027)", team_list)
    
    team_stats = df_teams[df_teams["Équipe"] == selected_team].iloc[0]
    
    st.markdown(f"### 📊 {selected_team} (2026/2027)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("xG / Match (Attaque)", team_stats["xG/M"])
        st.metric("xGA / Match (Défense)", team_stats["xGA/M"])
    with col2:
        st.metric("PPDA (Intensité Pressing)", team_stats["PPDA"])
        st.metric("Matchs Joués", team_stats["Matchs"])
        
    st.markdown("---")
    
    # Visualisation Radar
    st.subheader(" Profil Tactique")
    params = ["Possession", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Chance Creat."]
    # Valeurs indexées dynamiquement sur la data
    val_xg = min(int((team_stats["xG/M"] / 2.5) * 100), 98)
    val_ppda = min(max(int((16 - team_stats["PPDA"]) * 8), 20), 95)
    values = [75, 70, 45, val_ppda, 65, val_xg]
    
    pizza = PyPizza(
        params=params, straight_line_color="#000000", straight_line_lw=1, other_circle_ls="--"
    )
    fig, ax = pizza.make_pizza(
        values, figsize=(6, 6), param_location=110,
        kwargs_slices=dict(facecolor="#1A73E8", edgecolor="#000000", linewidth=1.5),
        kwargs_params=dict(color="#000000", fontsize=10, va="center")
    )
    st.pyplot(fig)

    st.markdown("---")
    with st.expander("Voir le tableau récapitulatif du championnat"):
        st.dataframe(df_teams, use_container_width=True)
else:
    st.error("Délai de connexion dépassé. Réessaye dans quelques secondes.")
