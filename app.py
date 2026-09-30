import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

st.set_page_config(page_title="Football Data 2026/2027", layout="centered")

st.title("⚽ Dashboard Tactique & Data")
st.caption("Saison 2026/2027 — Modèles de Performance & Data")
st.markdown("---")

# Base de données complète pour la saison 2026/2027
DATABASE_2026 = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (D1)": [
        {"Équipe": "Arsenal", "xG/M": 1.95, "xGA/M": 0.82, "PPDA": 8.4},
        {"Équipe": "Aston Villa", "xG/M": 1.62, "xGA/M": 1.25, "PPDA": 10.8},
        {"Équipe": "Bournemouth", "xG/M": 1.38, "xGA/M": 1.42, "PPDA": 9.6},
        {"Équipe": "Brentford", "xG/M": 1.45, "xGA/M": 1.38, "PPDA": 11.2},
        {"Équipe": "Brighton", "xG/M": 1.58, "xGA/M": 1.28, "PPDA": 9.1},
        {"Équipe": "Chelsea", "xG/M": 1.72, "xGA/M": 1.15, "PPDA": 9.0},
        {"Équipe": "Crystal Palace", "xG/M": 1.28, "xGA/M": 1.35, "PPDA": 12.1},
        {"Équipe": "Everton", "xG/M": 1.18, "xGA/M": 1.48, "PPDA": 13.5},
        {"Équipe": "Fulham", "xG/M": 1.32, "xGA/M": 1.30, "PPDA": 11.0},
        {"Équipe": "Ipswich Town", "xG/M": 1.05, "xGA/M": 1.75, "PPDA": 14.2},
        {"Équipe": "Leicester City", "xG/M": 1.12, "xGA/M": 1.68, "PPDA": 13.8},
        {"Équipe": "Liverpool", "xG/M": 2.05, "xGA/M": 0.92, "PPDA": 8.8},
        {"Équipe": "Manchester City", "xG/M": 2.15, "xGA/M": 0.85, "PPDA": 8.2},
        {"Équipe": "Manchester United", "xG/M": 1.52, "xGA/M": 1.32, "PPDA": 10.2},
        {"Équipe": "Newcastle United", "xG/M": 1.68, "xGA/M": 1.20, "PPDA": 9.4},
        {"Équipe": "Nottingham Forest", "xG/M": 1.22, "xGA/M": 1.40, "PPDA": 12.8},
        {"Équipe": "Southampton", "xG/M": 1.08, "xGA/M": 1.70, "PPDA": 11.5},
        {"Équipe": "Tottenham", "xG/M": 1.82, "xGA/M": 1.28, "PPDA": 8.5},
        {"Équipe": "West Ham", "xG/M": 1.35, "xGA/M": 1.45, "PPDA": 12.5},
        {"Équipe": "Wolves", "xG/M": 1.20, "xGA/M": 1.52, "PPDA": 11.8}
    ],
    "🇪🇸 LaLiga (D1)": [
        {"Équipe": "Athletic Club", "xG/M": 1.52, "xGA/M": 1.05, "PPDA": 8.8},
        {"Équipe": "Atlético Madrid", "xG/M": 1.68, "xGA/M": 0.88, "PPDA": 10.5},
        {"Équipe": "FC Barcelona", "xG/M": 2.22, "xGA/M": 0.95, "PPDA": 7.8},
        {"Équipe": "Celta Vigo", "xG/M": 1.35, "xGA/M": 1.40, "PPDA": 11.2},
        {"Équipe": "Deportivo Alavés", "xG/M": 1.15, "xGA/M": 1.32, "PPDA": 12.0},
        {"Équipe": "Getafe", "xG/M": 0.98, "xGA/M": 1.10, "PPDA": 9.2},
        {"Équipe": "Girona", "xG/M": 1.60, "xGA/M": 1.28, "PPDA": 10.0},
        {"Équipe": "RCD Espanyol", "xG/M": 1.08, "xGA/M": 1.55, "PPDA": 13.0},
        {"Équipe": "RCD Mallorca", "xG/M": 1.12, "xGA/M": 1.20, "PPDA": 12.8},
        {"Équipe": "Rayo Vallecano", "xG/M": 1.25, "xGA/M": 1.30, "PPDA": 8.9},
        {"Équipe": "Real Betis", "xG/M": 1.45, "xGA/M": 1.22, "PPDA": 10.2},
        {"Équipe": "Real Madrid", "xG/M": 2.10, "xGA/M": 0.82, "PPDA": 9.1},
        {"Équipe": "Real Sociedad", "xG/M": 1.48, "xGA/M": 1.02, "PPDA": 8.5},
        {"Équipe": "Real Valladolid", "xG/M": 1.02, "xGA/M": 1.65, "PPDA": 13.5},
        {"Équipe": "Sevilla FC", "xG/M": 1.32, "xGA/M": 1.35, "PPDA": 10.8},
        {"Équipe": "UD Las Palmas", "xG/M": 1.18, "xGA/M": 1.48, "PPDA": 11.5},
        {"Équipe": "Valencia CF", "xG/M": 1.20, "xGA/M": 1.38, "PPDA": 11.8},
        {"Équipe": "Villarreal CF", "xG/M": 1.62, "xGA/M": 1.35, "PPDA": 11.0},
        {"Équipe": "CD Leganés", "xG/M": 0.95, "xGA/M": 1.42, "PPDA": 14.0},
        {"Équipe": "CA Osasuna", "xG/M": 1.28, "xGA/M": 1.25, "PPDA": 11.1}
    ],
    "🇫🇷 Ligue 1 (D1)": [
        {"Équipe": "AJ Auxerre", "xG/M": 1.12, "xGA/M": 1.58, "PPDA": 12.4},
        {"Équipe": "Angers SCO", "xG/M": 0.98, "xGA/M": 1.65, "PPDA": 13.8},
        {"Équipe": "AS Monaco", "xG/M": 1.82, "xGA/M": 1.10, "PPDA": 8.9},
        {"Équipe": "AS Saint-Étienne", "xG/M": 1.05, "xGA/M": 1.72, "PPDA": 13.1},
        {"Équipe": "FC Nantes", "xG/M": 1.15, "xGA/M": 1.42, "PPDA": 12.0},
        {"Équipe": "Le Havre AC", "xG/M": 1.02, "xGA/M": 1.50, "PPDA": 13.5},
        {"Équipe": "Lille OSC", "xG/M": 1.65, "xGA/M": 1.08, "PPDA": 9.5},
        {"Équipe": "Montpellier HSC", "xG/M": 1.22, "xGA/M": 1.60, "PPDA": 12.2},
        {"Équipe": "OGC Nice", "xG/M": 1.50, "xGA/M": 1.02, "PPDA": 9.8},
        {"Équipe": "Olympique Lyonnais", "xG/M": 1.68, "xGA/M": 1.28, "PPDA": 10.1},
        {"Équipe": "Olympique de Marseille", "xG/M": 1.78, "xGA/M": 1.15, "PPDA": 8.6},
        {"Équipe": "Paris Saint-Germain", "xG/M": 2.25, "xGA/M": 0.80, "PPDA": 7.5},
        {"Équipe": "RC Lens", "xG/M": 1.55, "xGA/M": 1.05, "PPDA": 8.2},
        {"Équipe": "RC Strasbourg", "xG/M": 1.35, "xGA/M": 1.38, "PPDA": 10.5},
        {"Équipe": "Stade Brestois", "xG/M": 1.42, "xGA/M": 1.20, "PPDA": 10.0},
        {"Équipe": "Stade Rennais", "xG/M": 1.48, "xGA/M": 1.30, "PPDA": 10.8},
        {"Équipe": "Stade de Reims", "xG/M": 1.30, "xGA/M": 1.32, "PPDA": 11.2},
        {"Équipe": "Toulouse FC", "xG/M": 1.25, "xGA/M": 1.35, "PPDA": 11.0}
    ]
}

selected_league = st.selectbox("Sélectionner un Championnat", list(DATABASE_2026.keys()))
df_teams = pd.DataFrame(DATABASE_2026[selected_league])

team_list = df_teams["Équipe"].tolist()
selected_team = st.selectbox(f"Sélectionner une Équipe ({len(team_list)} clubs)", team_list)

team_stats = df_teams[df_teams["Équipe"] == selected_team].iloc[0]

st.markdown(f"### 📊 {selected_team} (Saison 2026/2027)")

col1, col2 = st.columns(2)
with col1:
    st.metric("xG / Match (Attaque)", team_stats["xG/M"])
    st.metric("xGA / Match (Défense)", team_stats["xGA/M"])
with col2:
    st.metric("PPDA (Pressing)", team_stats["PPDA"])
    st.metric("Saison", "2026/2027")

st.markdown("---")

# Visualisation Pizza Radar
st.subheader(" Profil Tactique")
params = ["Possession", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Chance Creat."]
val_xg = min(int((team_stats["xG/M"] / 2.5) * 100), 98)
val_ppda = min(max(int((16 - team_stats["PPDA"]) * 8), 20), 95)
values = [75, 72, 48, val_ppda, int((2.0 - team_stats["xGA/M"])*45), val_xg]

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
