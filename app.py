import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import pandas as pd

# Configuration de la page web adaptée aux écrans mobiles
st.set_page_config(page_title="Foot Analytics Mobile", layout="centered")

st.title("⚽ Dashboard Tactique & Data")
st.markdown("---")

# Menu déroulant pour le choix de l'équipe
team = st.selectbox("Sélectionner une équipe", ["Real Madrid", "Barcelona", "Shamrock Rovers"])

st.markdown("---")

# Métriques clés sous forme de cartes d'affichage
st.metric("Possession Moyenne", "61.1%", "2nd La Liga")
st.metric("xG / Match", "2.20", "+0.45 vs moy.")
st.metric("xGA / Match", "1.14", "-0.16 vs moy.")
st.metric("PPDA (Pressing Understat)", "14.0", "14th (Bloc Médian)")

st.markdown("---")

# Visualisation Radar (PyPizza)
st.subheader("📊 Profil Tactique")
params = ["Possession", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Chance Creat."]
values = [88, 82, 35, 42, 65, 90]

pizza = PyPizza(
    params=params,
    straight_line_color="#000000",
    straight_line_lw=1,
    other_circle_ls="--"
)

fig, ax = pizza.make_pizza(
    values, 
    figsize=(6, 6),
    param_location=110,
    kwargs_slices=dict(facecolor="#1A73E8", edgecolor="#000000", linewidth=1.5),
    kwargs_params=dict(color="#000000", fontsize=10, va="center")
)
st.pyplot(fig)

st.markdown("---")

# Graphique de la tendance xG
st.subheader("📈 Tendance xG (Moyenne Glissante)")
data = pd.DataFrame({
    'Match': [f"M{i}" for i in range(1, 8)],
    'xG Pour': [1.8, 2.4, 2.1, 1.9, 2.8, 2.0, 2.4],
    'xG Contre': [0.9, 1.2, 1.4, 0.8, 1.1, 1.5, 1.1]
})

fig_xg, ax_xg = plt.subplots(figsize=(6, 4))
ax_xg.plot(data['Match'], data['xG Pour'], label='xG Pour', color='blue', linewidth=2)
ax_xg.plot(data['Match'], data['xG Contre'], label='xG Contre', color='orange', linewidth=2)
ax_xg.set_ylabel("Expected Goals")
ax_xg.grid(True, linestyle='--', alpha=0.5)
ax_xg.legend()
st.pyplot(fig_xg)
