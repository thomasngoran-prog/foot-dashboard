import streamlit as st
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

st.set_page_config(page_title="Football Data 2026/2027", layout="centered")

st.title("⚽ Dashboard Tactique & Data")
st.caption("Saison 2026/2027 — Données Understat")
st.markdown("---")

# Championnats (Top 5 D1)
LEAGUES = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (D1)": "EPL",
    "🇪🇸 LaLiga (D1)": "La_liga",
    "🇩🇪 Bundesliga (D1)": "Bundesliga",
    "🇮🇹 Serie A (D1)": "Serie_A",
    "🇫🇷 Ligue 1 (D1)": "Ligue_1",
}

selected_league_label = st.selectbox("Sélectionner un Championnat", list(LEAGUES.keys()))
league_code = LEAGUES[selected_league_label]

@st.cache_data(ttl=3600)
def load_understat_data(league, season=2026):
    url = f"https://understat.com/main/getdata/{league}/{season}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        data = response.json()
        teams_data = data.get("teams", {})
        
        parsed_teams = []
        for team_id, info in teams_data.items():
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

with st.spinner("Chargement des 20 équipes (2026/2027)..."):
    df_teams = load_understat_data(league_code, season=2026)

if df_teams is not None and not df_teams.empty:
    team_list = df_teams["Équipe"].tolist()
    selected_team = st.selectbox("Sélectionner une Équipe (20 équipes disponibles)", team_list)
    
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
    
    # Radar Tactique
    st.subheader(" Profil Tactique")
    params = ["Possession", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Chance Creat."]
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
    with st.expander("Voir le tableau récapitulatif des 20 équipes"):
        st.dataframe(df_teams, use_container_width=True)
else:
    st.warning("Chargement en cours ou données temporairement indisponibles. Actualisez la page.")
