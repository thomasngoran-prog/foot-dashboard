import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import pandas as pd

# Configuration de la page mobile
st.set_page_config(page_title="Top 5 Mondial - Analytics", layout="centered")

st.title("⚽ Top 5 Mondial - Data & Tactique")
st.markdown("---")

# Base de données pour le Top 5 Mondial
teams_data = {
    "Real Madrid": {
        "league": "La Liga",
        "ppg": "2.14", "ppg_sub": "4th La Liga",
        "poss": "61.1%", "poss_sub": "2nd La Liga",
        "xg": "2.20", "xg_sub": "+0.45 vs moy.",
        "xga": "1.14", "xga_sub": "-0.16 vs moy.",
        "ppda": "14.0", "ppda_sub": "Bloc Médian / Attentiste",
        "radar_values": [88, 82, 35, 42, 65, 90],
        "xg_for": [1.8, 2.4, 2.1, 1.9, 2.8, 2.0, 2.4],
        "xg_ag": [0.9, 1.2, 1.4, 0.8, 1.1, 1.5, 1.1]
    },
    "FC Barcelona": {
        "league": "La Liga",
        "ppg": "3.00", "ppg_sub": "1er La Liga",
        "poss": "68.4%", "poss_sub": "1er La Liga",
        "xg": "2.85", "xg_sub": "+1.20 vs moy.",
        "xga": "0.75", "xga_sub": "-0.55 vs moy.",
        "ppda": "7.0", "ppda_sub": "Pressing Très Intense",
        "radar_values": [98, 95, 20, 95, 80, 96],
        "xg_for": [2.5, 3.1, 2.8, 3.4, 2.9, 3.0, 2.7],
        "xg_ag": [0.6, 0.8, 0.5, 0.9, 0.7, 0.4, 0.8]
    },
    "Manchester City": {
        "league": "Premier League",
        "ppg": "2.40", "ppg_sub": "1er Premier League",
        "poss": "66.2%", "poss_sub": "1er Premier League",
        "xg": "2.35", "xg_sub": "+0.70 vs moy.",
        "xga": "0.85", "xga_sub": "-0.40 vs moy.",
        "ppda": "8.5", "ppda_sub": "Contre-Pressing Haut",
        "radar_values": [95, 92, 25, 88, 85, 92],
        "xg_for": [2.1, 2.6, 2.2, 2.8, 2.0, 2.5, 2.3],
        "xg_ag": [0.7, 0.9, 0.8, 1.0, 0.6, 0.7, 0.9]
    },
    "Arsenal": {
        "league": "Premier League",
        "ppg": "2.25", "ppg_sub": "2nd Premier League",
        "poss": "59.8%", "poss_sub": "3rd Premier League",
        "xg": "2.10", "xg_sub": "+0.50 vs moy.",
        "xga": "0.80", "xga_sub": "Meilleure défense PL",
        "ppda": "9.1", "ppda_sub": "Bloc Haut Structuré",
        "radar_values": [82, 85, 45, 85, 92, 86],
        "xg_for": [1.9, 2.2, 2.0, 2.5, 1.8, 2.3, 2.1],
        "xg_ag": [0.6, 0.8, 0.7, 0.9, 0.5, 0.8, 0.6]
    },
    "Bayern Munich": {
        "league": "Bundesliga",
        "ppg": "2.60", "ppg_sub": "1er Bundesliga",
        "poss": "64.5%", "poss_sub": "1er Bundesliga",
        "xg": "2.65", "xg_sub": "+0.95 vs moy.",
        "xga": "0.90", "xga_sub": "-0.35 vs moy.",
        "ppda": "7.8", "ppda_sub": "Pressing Agressif",
        "radar_values": [90, 88, 40, 92, 78, 95],
        "xg_for": [2.4, 2.8, 2.3, 3.0, 2.2, 2.7, 2.6],
        "xg_ag": [0.8, 1.1, 0.9, 0.7, 1.0, 0.8, 0.9]
    }
}

# Sélection de l'équipe
selected_team = st.selectbox("Sélectionner une équipe", list(teams_data.keys()))
t = teams_data[selected_team]

st.markdown(f"### 🏆 {selected_team} ({t['league']})")

# Affichage des KPIs
st.metric("Points / Match", t["ppg"], t["ppg_sub"])
st.metric("Possession Moyenne", t["poss"], t["poss_sub"])
st.metric("xG / Match (Attaque)", t["xg"], t["xg_sub"])
st.metric("xGA / Match (Défense)", t["xga"], t["xga_sub"])
st.metric("PPDA (Intensité Pressing)", t["ppda"], t["ppda_sub"])

st.markdown("---")

# Radar Tactique
st.subheader("📊 Profil Tactique & Style")
params = ["Possession", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Chance Creat."]

pizza = PyPizza(
    params=params,
    straight_line_color="#000000",
    straight_line_lw=1,
    other_circle_ls="--"
)

fig, ax = pizza.make_pizza(
    t["radar_values"], 
    figsize=(6, 6),
    param_location=110,
    kwargs_slices=dict(facecolor="#1A73E8", edgecolor="#000000", linewidth=1.5),
    kwargs_params=dict(color="#000000", fontsize=10, va="center")
)
st.pyplot(fig)

st.markdown("---")

# Courbe de forme xG
st.subheader("📈 Tendance xG (Moyenne Glissante)")
data = pd.DataFrame({
    'Match': [f"M{i}" for i in range(1, 8)],
    'xG Pour': t["xg_for"],
    'xG Contre': t["xg_ag"]
})

fig_xg, ax_xg = plt.subplots(figsize=(6, 4))
ax_xg.plot(data['Match'], data['xG Pour'], label='xG Pour', color='blue', linewidth=2)
ax_xg.plot(data['Match'], data['xG Contre'], label='xG Contre', color='orange', linewidth=2)
ax_xg.set_ylabel("Expected Goals")
ax_xg.grid(True, linestyle='--', alpha=0.5)
ax_xg.legend()
st.pyplot(fig_xg)
