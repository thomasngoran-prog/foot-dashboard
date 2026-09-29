import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import pandas as pd

# Configuration optimisée pour mobile
st.set_page_config(page_title="Football Data & Tactique", layout="centered")

st.title("⚽ Dashboard Tactique & Data")
st.caption("Sources : Understat | FBref | Opta Analyst")
st.markdown("---")

# Base de données structurée par Ligue et Division (Data Understat / FBref / Opta)
leagues_data = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (D1)": {
        "Arsenal": {
            "poss": "59.8%", "poss_sub": "3rd PL (FBref)",
            "xg": "2.10", "xg_sub": "+0.50 vs moy. (Understat)",
            "xga": "0.80", "xga_sub": "1st PL Defensive xG (Understat)",
            "ppda": "9.1", "ppda_sub": "Bloc Haut Structuré (Opta)",
            "radar": [82, 85, 45, 85, 92, 86],
            "xg_for": [1.9, 2.2, 2.0, 2.5, 1.8, 2.3, 2.1],
            "xg_ag": [0.6, 0.8, 0.7, 0.9, 0.5, 0.8, 0.6]
        },
        "Manchester City": {
            "poss": "66.2%", "poss_sub": "1st PL (FBref)",
            "xg": "2.35", "xg_sub": "+0.70 vs moy. (Understat)",
            "xga": "0.85", "xga_sub": "-0.40 vs moy. (Understat)",
            "ppda": "8.5", "ppda_sub": "Contre-Pressing Haut (Opta)",
            "radar": [95, 92, 25, 88, 85, 92],
            "xg_for": [2.1, 2.6, 2.2, 2.8, 2.0, 2.5, 2.3],
            "xg_ag": [0.7, 0.9, 0.8, 1.0, 0.6, 0.7, 0.9]
        }
    },
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 EFL Championship (D2)": {
        "Leeds United": {
            "poss": "62.4%", "poss_sub": "1st Championship (FBref)",
            "xg": "1.95", "xg_sub": "+0.60 vs moy. (FBref)",
            "xga": "0.90", "xga_sub": "Top 3 Défense (FBref)",
            "ppda": "8.0", "ppda_sub": "Gegenpressing (Opta)",
            "radar": [88, 80, 50, 90, 82, 85],
            "xg_for": [1.7, 2.1, 1.9, 2.3, 1.8, 2.0, 2.2],
            "xg_ag": [0.8, 0.9, 0.7, 1.1, 0.8, 0.9, 0.7]
        }
    },
    "🇪🇸 LaLiga (D1)": {
        "FC Barcelona": {
            "poss": "68.4%", "poss_sub": "1st LaLiga (FBref)",
            "xg": "2.85", "xg_sub": "1st LaLiga xG (Understat)",
            "xga": "0.75", "xga_sub": "-0.55 vs moy. (Understat)",
            "ppda": "7.0", "ppda_sub": "Pressing Très Intense (Opta)",
            "radar": [98, 95, 20, 95, 80, 96],
            "xg_for": [2.5, 3.1, 2.8, 3.4, 2.9, 3.0, 2.7],
            "xg_ag": [0.6, 0.8, 0.5, 0.9, 0.7, 0.4, 0.8]
        },
        "Real Madrid": {
            "poss": "61.1%", "poss_sub": "2nd LaLiga (FBref)",
            "xg": "2.20", "xg_sub": "+0.45 vs moy. (Understat)",
            "xga": "1.14", "xga_sub": "-0.16 vs moy. (Understat)",
            "ppda": "14.0", "ppda_sub": "Bloc Médian (Opta)",
            "radar": [88, 82, 35, 42, 65, 90],
            "xg_for": [1.8, 2.4, 2.1, 1.9, 2.8, 2.0, 2.4],
            "xg_ag": [0.9, 1.2, 1.4, 0.8, 1.1, 1.5, 1.1]
        }
    },
    "🇪🇸 LaLiga Hypermotion (D2)": {
        "RCD Espanyol": {
            "poss": "55.1%", "poss_sub": "Top 5 LaLiga2 (FBref)",
            "xg": "1.65", "xg_sub": "+0.30 vs moy. (FBref)",
            "xga": "1.05", "xga_sub": "Défense Solide (FBref)",
            "ppda": "10.5", "ppda_sub": "Bloc Médian-Haut (Opta)",
            "radar": [75, 72, 55, 70, 78, 76],
            "xg_for": [1.5, 1.8, 1.4, 1.9, 1.6, 1.7, 1.8],
            "xg_ag": [1.0, 1.1, 0.9, 1.2, 1.0, 0.8, 1.1]
        }
    },
    "🇩🇪 Bundesliga (D1)": {
        "Bayern Munich": {
            "poss": "64.5%", "poss_sub": "1st Bundesliga (FBref)",
            "xg": "2.65", "xg_sub": "1st Bundesliga xG (Understat)",
            "xga": "0.90", "xga_sub": "-0.35 vs moy. (Understat)",
            "ppda": "7.8", "ppda_sub": "Pressing Agressif (Opta)",
            "radar": [90, 88, 40, 92, 78, 95],
            "xg_for": [2.4, 2.8, 2.3, 3.0, 2.2, 2.7, 2.6],
            "xg_ag": [0.8, 1.1, 0.9, 0.7, 1.0, 0.8, 0.9]
        }
    },
    "🇩🇪 2. Bundesliga (D2)": {
        "Hamburger SV": {
            "poss": "58.0%", "poss_sub": "Top 3 2.Bündesliga (FBref)",
            "xg": "1.80", "xg_sub": "+0.45 vs moy. (FBref)",
            "xga": "1.20", "xga_sub": "Jeu Ouvert (FBref)",
            "ppda": "9.5", "ppda_sub": "Pressing Proactif (Opta)",
            "radar": [80, 78, 45, 82, 70, 82],
            "xg_for": [1.6, 2.0, 1.7, 2.1, 1.5, 1.9, 2.0],
            "xg_ag": [1.1, 1.3, 1.0, 1.4, 1.1, 1.2, 1.0]
        }
    },
    "🇮🇹 Serie A (D1)": {
        "Inter Milan": {
            "poss": "57.5%", "poss_sub": "Top 3 Serie A (FBref)",
            "xg": "2.15", "xg_sub": "1st Serie A xG (Understat)",
            "xga": "0.85", "xga_sub": "Meilleure Défense (Understat)",
            "ppda": "11.2", "ppda_sub": "Bloc Compact Structuré (Opta)",
            "radar": [78, 88, 60, 68, 90, 88],
            "xg_for": [2.0, 2.3, 1.9, 2.4, 2.1, 2.2, 2.5],
            "xg_ag": [0.7, 0.8, 0.9, 0.6, 0.8, 0.7, 0.9]
        }
    },
    "🇮🇹 Serie B (D2)": {
        "Palermo": {
            "poss": "52.8%", "poss_sub": "Milieu de Tableau (FBref)",
            "xg": "1.45", "xg_sub": "+0.15 vs moy. (FBref)",
            "xga": "1.15", "xga_sub": "Standard D2 (FBref)",
            "ppda": "12.0", "ppda_sub": "Attente / Contre (Opta)",
            "radar": [68, 65, 62, 58, 68, 70],
            "xg_for": [1.3, 1.5, 1.2, 1.6, 1.4, 1.5, 1.6],
            "xg_ag": [1.1, 1.2, 1.0, 1.3, 1.1, 1.0, 1.2]
        }
    },
    "🇫🇷 Ligue 1 (D1)": {
        "Paris Saint-Germain": {
            "poss": "65.0%", "poss_sub": "1st Ligue 1 (FBref)",
            "xg": "2.40", "xg_sub": "1st Ligue 1 xG (Understat)",
            "xga": "0.95", "xga_sub": "-0.30 vs moy. (Understat)",
            "ppda": "8.2", "ppda_sub": "Contre-Pressing (Opta)",
            "radar": [92, 90, 30, 86, 80, 94],
            "xg_for": [2.2, 2.6, 2.1, 2.7, 2.3, 2.5, 2.4],
            "xg_ag": [0.8, 1.0, 0.9, 1.1, 0.7, 0.9, 1.0]
        }
    },
    "🇫🇷 Ligue 2 (D2)": {
        "FC Lorient": {
            "poss": "56.2%", "poss_sub": "Top 3 Ligue 2 (FBref)",
            "xg": "1.60", "xg_sub": "+0.35 vs moy. (FBref)",
            "xga": "1.00", "xga_sub": "Solide D2 (FBref)",
            "ppda": "10.0", "ppda_sub": "Pressing Médian (Opta)",
            "radar": [74, 76, 50, 72, 75, 78],
            "xg_for": [1.4, 1.7, 1.5, 1.8, 1.6, 1.5, 1.7],
            "xg_ag": [0.9, 1.1, 1.0, 1.2, 0.8, 1.0, 0.9]
        }
    }
}

# Menu de sélection : 1. Championnat, 2. Équipe
selected_league = st.selectbox("Sélectionner un Championnat", list(leagues_data.keys()))
teams_in_league = leagues_data[selected_league]

selected_team = st.selectbox("Sélectionner une Équipe", list(teams_in_league.keys()))
t = teams_in_league[selected_team]

st.markdown(f"### 📊 {selected_team}")

# Métriques clés (FBref / Understat / Opta Analyst)
st.metric("Possession (FBref)", t["poss"], t["poss_sub"])
st.metric("xG / Match (Understat)", t["xg"], t["xg_sub"])
st.metric("xGA / Match (Understat)", t["xga"], t["xga_sub"])
st.metric("PPDA Pressing (Opta / Understat)", t["ppda"], t["ppda_sub"])

st.markdown("---")

# Radar de profil tactique
st.subheader(" Profil Tactique & Style")
params = ["Possession", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Chance Creat."]

pizza = PyPizza(
    params=params,
    straight_line_color="#000000",
    straight_line_lw=1,
    other_circle_ls="--"
)

fig, ax = pizza.make_pizza(
    t["radar"], 
    figsize=(6, 6),
    param_location=110,
    kwargs_slices=dict(facecolor="#1A73E8", edgecolor="#000000", linewidth=1.5),
    kwargs_params=dict(color="#000000", fontsize=10, va="center")
)
st.pyplot(fig)

st.markdown("---")

# Courbe de tendance xG
st.subheader("📈 Tendance xG (Rolling Average)")
data = pd.DataFrame({
    'Match': [f"M{i}" for i in range(1, 8)],
    'xG Pour': t["xg_for"],
    'xG Contre': t["xg_ag"]
})

fig_xg, ax_xg = plt.subplots(figsize=(6, 4))
ax_xg.plot(data['Match'], data['xG Pour'], label='xG Pour (Attaque)', color='blue', linewidth=2)
ax_xg.plot(data['Match'], data['xG Contre'], label='xG Contre (Défense)', color='orange', linewidth=2)
ax_xg.set_ylabel("Expected Goals")
ax_xg.grid(True, linestyle='--', alpha=0.5)
ax_xg.legend()
st.pyplot(fig_xg)
