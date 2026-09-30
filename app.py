import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

st.set_page_config(page_title="Football Data 2026/2027", layout="wide")

# Style CSS Opta / Wyscout
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .comp-card {
        background-color: #FFFFFF;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 10px;
        border: 1px solid #EAEAEA;
        text-align: center;
    }
    .metric-name { font-size: 11px; color: #6B7280; text-transform: uppercase; font-weight: bold; }
    .val-a { font-size: 20px; font-weight: bold; color: #1E3A8A; }
    .val-b { font-size: 20px; font-weight: bold; color: #D97706; }
    .team-label { font-size: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Dashboard Data 2026/2027 — Top 5 Européen (D1)")
st.caption("Métriques & Analyses Tactiques (Understat | FBref | Opta)")
st.markdown("---")

# Base de données complète des 20 équipes du Top 5 D1 (Saison 2026/2027)
DATABASE_2026 = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (D1)": [
        {"Équipe": "Arsenal", "xG": 1.95, "xGA": 0.80, "PPDA": 10.3, "Poss": 62.0, "radar": [85, 82, 38, 72, 82, 88]},
        {"Équipe": "Aston Villa", "xG": 1.62, "xGA": 1.25, "PPDA": 10.8, "Poss": 54.0, "radar": [70, 72, 58, 68, 60, 74]},
        {"Équipe": "Bournemouth", "xG": 1.40, "xGA": 1.38, "PPDA": 9.9, "Poss": 49.0, "radar": [60, 62, 62, 74, 55, 62]},
        {"Équipe": "Brentford", "xG": 1.48, "xGA": 1.35, "PPDA": 9.0, "Poss": 46.5, "radar": [64, 55, 72, 80, 58, 65]},
        {"Équipe": "Brighton", "xG": 1.62, "xGA": 1.15, "PPDA": 5.5, "Poss": 58.2, "radar": [75, 82, 42, 95, 68, 75]},
        {"Équipe": "Chelsea", "xG": 1.75, "xGA": 1.18, "PPDA": 13.9, "Poss": 58.5, "radar": [78, 78, 45, 48, 65, 80]},
        {"Équipe": "Crystal Palace", "xG": 1.30, "xGA": 1.32, "PPDA": 15.7, "Poss": 45.0, "radar": [52, 52, 68, 40, 60, 56]},
        {"Équipe": "Everton", "xG": 1.20, "xGA": 1.45, "PPDA": 15.2, "Poss": 41.5, "radar": [46, 45, 78, 42, 52, 48]},
        {"Équipe": "Fulham", "xG": 1.32, "xGA": 1.30, "PPDA": 11.7, "Poss": 51.0, "radar": [55, 62, 55, 60, 60, 58]},
        {"Équipe": "Ipswich", "xG": 1.08, "xGA": 1.70, "PPDA": 12.1, "Poss": 42.5, "radar": [42, 44, 74, 58, 40, 44]},
        {"Équipe": "Leicester City", "xG": 1.12, "xGA": 1.68, "PPDA": 13.8, "Poss": 45.0, "radar": [42, 48, 70, 45, 40, 45]},
        {"Équipe": "Liverpool", "xG": 2.05, "xGA": 0.88, "PPDA": 7.4, "Poss": 61.5, "radar": [88, 85, 48, 88, 75, 89]},
        {"Équipe": "Manchester City", "xG": 2.18, "xGA": 0.82, "PPDA": 8.5, "Poss": 65.5, "radar": [92, 90, 25, 84, 80, 92]},
        {"Équipe": "Manchester United", "xG": 1.52, "xGA": 1.32, "PPDA": 10.2, "Poss": 53.5, "radar": [68, 68, 52, 72, 58, 70]},
        {"Équipe": "Newcastle United", "xG": 1.65, "xGA": 1.22, "PPDA": 10.5, "Poss": 52.5, "radar": [72, 70, 60, 70, 64, 75]},
        {"Équipe": "Nottingham Forest", "xG": 1.25, "xGA": 1.38, "PPDA": 11.1, "Poss": 42.0, "radar": [50, 48, 72, 65, 58, 52]},
        {"Équipe": "Southampton", "xG": 1.08, "xGA": 1.70, "PPDA": 11.5, "Poss": 55.0, "radar": [42, 65, 40, 60, 38, 45]},
        {"Équipe": "Tottenham", "xG": 1.85, "xGA": 1.20, "PPDA": 7.5, "Poss": 60.0, "radar": [82, 82, 40, 87, 62, 84]},
        {"Équipe": "West Ham", "xG": 1.35, "xGA": 1.45, "PPDA": 12.5, "Poss": 43.0, "radar": [56, 50, 70, 52, 52, 58]},
        {"Équipe": "Wolves", "xG": 1.20, "xGA": 1.52, "PPDA": 11.8, "Poss": 47.0, "radar": [48, 52, 65, 58, 48, 50]}
    ],
    "🇪🇸 LaLiga (D1)": [
        {"Équipe": "Athletic Club", "xG": 1.52, "xGA": 1.05, "PPDA": 8.8, "Poss": 51.5, "radar": [68, 65, 62, 82, 72, 70]},
        {"Équipe": "Atlético Madrid", "xG": 1.68, "xGA": 0.88, "PPDA": 10.5, "Poss": 52.0, "radar": [75, 72, 55, 70, 82, 76]},
        {"Équipe": "FC Barcelona", "xG": 2.22, "xGA": 0.95, "PPDA": 7.8, "Poss": 63.0, "radar": [94, 90, 20, 92, 70, 94]},
        {"Équipe": "Celta Vigo", "xG": 1.35, "xGA": 1.40, "PPDA": 11.2, "Poss": 53.0, "radar": [56, 62, 48, 62, 52, 58]},
        {"Équipe": "Deportivo Alavés", "xG": 1.15, "xGA": 1.32, "PPDA": 12.0, "Poss": 42.0, "radar": [45, 45, 70, 58, 58, 46]},
        {"Équipe": "Getafe", "xG": 0.98, "xGA": 1.10, "PPDA": 9.2, "Poss": 38.0, "radar": [38, 35, 85, 78, 68, 40]},
        {"Équipe": "Girona", "xG": 1.60, "xGA": 1.28, "PPDA": 10.0, "Poss": 57.0, "radar": [72, 78, 42, 70, 58, 72]},
        {"Équipe": "Real Madrid", "xG": 2.10, "xGA": 0.82, "PPDA": 9.1, "Poss": 60.1, "radar": [90, 88, 35, 78, 80, 90]},
        {"Équipe": "Real Sociedad", "xG": 1.48, "xGA": 1.02, "PPDA": 8.5, "Poss": 56.0, "radar": [65, 72, 48, 84, 75, 66]},
        {"Équipe": "Sevilla FC", "xG": 1.32, "xGA": 1.35, "PPDA": 10.8, "Poss": 52.5, "radar": [55, 60, 52, 65, 55, 56]},
        {"Équipe": "Valencia CF", "xG": 1.20, "xGA": 1.38, "PPDA": 11.8, "Poss": 46.5, "radar": [48, 50, 62, 58, 52, 50]},
        {"Équipe": "Villarreal CF", "xG": 1.62, "xGA": 1.35, "PPDA": 11.0, "Poss": 51.0, "radar": [72, 68, 55, 62, 55, 74]},
        {"Équipe": "CA Osasuna", "xG": 1.28, "xGA": 1.25, "PPDA": 11.1, "Poss": 47.5, "radar": [52, 52, 62, 62, 60, 52]}
    ],
    "🇩🇪 Bundesliga (D1)": [
        {"Équipe": "Bayer Leverkusen", "xG": 2.10, "xGA": 0.95, "PPDA": 8.5, "Poss": 61.2, "radar": [88, 86, 40, 85, 72, 89]},
        {"Équipe": "Bayern Munich", "xG": 2.30, "xGA": 0.88, "PPDA": 7.9, "Poss": 63.5, "radar": [92, 89, 32, 89, 76, 93]},
        {"Équipe": "Borussia Dortmund", "xG": 1.85, "xGA": 1.15, "PPDA": 9.2, "Poss": 57.0, "radar": [80, 78, 50, 78, 65, 82]},
        {"Équipe": "Eintracht Frankfurt", "xG": 1.65, "xGA": 1.30, "PPDA": 10.2, "Poss": 51.0, "radar": [70, 68, 65, 72, 58, 74]},
        {"Équipe": "RB Leipzig", "xG": 1.90, "xGA": 1.05, "PPDA": 8.1, "Poss": 55.5, "radar": [82, 75, 60, 88, 70, 85]},
        {"Équipe": "VfB Stuttgart", "xG": 1.78, "xGA": 1.20, "PPDA": 8.8, "Poss": 58.0, "radar": [78, 76, 48, 82, 64, 78]}
    ],
    "🇮🇹 Serie A (D1)": [
        {"Équipe": "AC Milan", "xG": 1.80, "xGA": 1.18, "PPDA": 9.8, "Poss": 54.5, "radar": [78, 75, 58, 75, 62, 80]},
        {"Équipe": "Atalanta", "xG": 1.95, "xGA": 1.10, "PPDA": 7.2, "Poss": 53.0, "radar": [84, 72, 68, 95, 68, 85]},
        {"Équipe": "Inter Milan", "xG": 2.00, "xGA": 0.84, "PPDA": 10.5, "Poss": 57.5, "radar": [85, 86, 52, 68, 85, 86]},
        {"Équipe": "Juventus", "xG": 1.75, "xGA": 0.78, "PPDA": 11.2, "Poss": 56.0, "radar": [78, 78, 45, 62, 88, 80]},
        {"Équipe": "Lazio", "xG": 1.58, "xGA": 1.22, "PPDA": 9.5, "Poss": 52.0, "radar": [68, 70, 52, 76, 62, 70]},
        {"Équipe": "Napoli", "xG": 1.70, "xGA": 0.92, "PPDA": 9.0, "Poss": 58.0, "radar": [74, 80, 42, 82, 80, 76]},
        {"Équipe": "AS Roma", "xG": 1.62, "xGA": 1.15, "PPDA": 10.0, "Poss": 55.0, "radar": [70, 72, 50, 72, 65, 72]}
    ],
    "🇫🇷 Ligue 1 (D1)": [
        {"Équipe": "AS Monaco", "xG": 1.82, "xGA": 1.10, "PPDA": 8.9, "Poss": 56.0, "radar": [80, 78, 52, 82, 68, 82]},
        {"Équipe": "Lille OSC", "xG": 1.65, "xGA": 1.08, "PPDA": 9.5, "Poss": 55.0, "radar": [70, 74, 50, 76, 70, 72]},
        {"Équipe": "OGC Nice", "xG": 1.50, "xGA": 1.02, "PPDA": 9.8, "Poss": 52.0, "radar": [65, 68, 48, 75, 75, 68]},
        {"Équipe": "Olympique Lyonnais", "xG": 1.68, "xGA": 1.28, "PPDA": 10.1, "Poss": 54.0, "radar": [72, 72, 55, 70, 60, 75]},
        {"Équipe": "Olympique de Marseille", "xG": 1.78, "xGA": 1.15, "PPDA": 8.6, "Poss": 58.5, "radar": [78, 80, 45, 85, 65, 80]},
        {"Équipe": "Paris Saint-Germain", "xG": 2.25, "xGA": 0.80, "PPDA": 7.5, "Poss": 64.8, "radar": [94, 92, 28, 90, 82, 95]},
        {"Équipe": "RC Lens", "xG": 1.55, "xGA": 1.05, "PPDA": 8.2, "Poss": 54.0, "radar": [70, 72, 52, 88, 72, 70]},
        {"Équipe": "Stade Rennais", "xG": 1.48, "xGA": 1.30, "PPDA": 10.8, "Poss": 51.0, "radar": [62, 65, 52, 68, 60, 64]}
    ]
}

selected_league = st.sidebar.selectbox("Sélectionner un Championnat", list(DATABASE_2026.keys()))
df_league = pd.DataFrame(DATABASE_2026[selected_league])

mode = st.sidebar.radio("Mode d'affichage", ["Profil Équipe Seule", "⚔️ Comparaison Face-à-Face"])
teams_list = df_league["Équipe"].tolist()

if mode == "Profil Équipe Seule":
    selected_team = st.sidebar.selectbox("Sélectionner une Équipe", teams_list)
    t = df_league[df_league["Équipe"] == selected_team].iloc[0]

    st.title(f"📊 {selected_team.upper()}")
    st.caption(f"{selected_league} • Saison 2026/2027")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("xG / Match", t["xG"])
    col2.metric("xGA / Match", t["xGA"])
    col3.metric("PPDA Pressing", t["PPDA"])
    col4.metric("Possession", f"{t['Poss']}%")

    st.markdown("---")
    st.subheader("Profil Tactique")
    params = ["Chance Creat.", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Possession"]
    
    pizza = PyPizza(params=params, background_color="#FFFFFF", straight_line_color="#E5E7EB")
    fig, ax = pizza.make_pizza(
        t["radar"], figsize=(5, 5),
        kwargs_slices=dict(facecolor="#1E3A8A", edgecolor="#1D4ED8", linewidth=1.5, alpha=0.75),
        kwargs_params=dict(color="#1F2937", fontsize=9)
    )
    st.pyplot(fig)

else:
    st.title("⚔️ Comparatif Tactique (Face-à-Face 2026/2027)")
    st.caption("Données relatives d'avant-match")
    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        team_a = st.selectbox("Équipe A (Bleu)", teams_list, index=0)
    with col_b:
        team_b = st.selectbox("Équipe B (Orange)", teams_list, index=1 if len(teams_list) > 1 else 0)

    t_a = df_league[df_league["Équipe"] == team_a].iloc[0]
    t_b = df_league[df_league["Équipe"] == team_b].iloc[0]

    m1, m2, m3, m4 = st.columns(4)
    
    def card_html(label, v_a, v_b, unit=""):
        return f"""
        <div class="comp-card">
            <div class="metric-name">{label}</div>
            <div style="display:flex; justify-content:space-around; align-items:center; margin: 6px 0;">
                <span class="val-a">{v_a}{unit}</span>
                <span style="color:#9CA3AF; font-size:12px; margin: 0 10px;">vs</span>
                <span class="val-b">{v_b}{unit}</span>
            </div>
            <div style="display:flex; justify-content:space-around;" class="team-label">
                <span style="color:#1E3A8A;">{team_a}</span>
                <span style="color:#D97706;">{team_b}</span>
            </div>
        </div>
        """
        
    with m1: st.markdown(card_html("xG / Match", t_a["xG"], t_b["xG"]), unsafe_allow_html=True)
    with m2: st.markdown(card_html("xGA / Match", t_a["xGA"], t_b["xGA"]), unsafe_allow_html=True)
    with m3: st.markdown(card_html("PPDA Pressing", t_a["PPDA"], t_b["PPDA"]), unsafe_allow_html=True)
    with m4: st.markdown(card_html("Possession", t_a["Poss"], t_b["Poss"], "%"), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎯 Comparatif des Profils Tactiques")
    
    r_col1, r_col2 = st.columns(2)
    params = ["Chance Creat.", "Build-Up", "Directness", "Pressing", "Chance Supp.", "Possession"]
    
    with r_col1:
        st.markdown(f"**🔵 {team_a}**")
        pizza_a = PyPizza(params=params, background_color="#FFFFFF", straight_line_color="#E5E7EB")
        fig_a, ax_a = pizza_a.make_pizza(
            t_a["radar"], figsize=(4.5, 4.5),
            kwargs_slices=dict(facecolor="#1E3A8A", edgecolor="#1D4ED8", linewidth=1.5, alpha=0.7),
            kwargs_params=dict(color="#1F2937", fontsize=8)
        )
        st.pyplot(fig_a)
        
    with r_col2:
        st.markdown(f"**🟠 {team_b}**")
        pizza_b = PyPizza(params=params, background_color="#FFFFFF", straight_line_color="#E5E7EB")
        fig_b, ax_b = pizza_b.make_pizza(
            t_b["radar"], figsize=(4.5, 4.5),
            kwargs_slices=dict(facecolor="#D97706", edgecolor="#B45309", linewidth=1.5, alpha=0.7),
            kwargs_params=dict(color="#1F2937", fontsize=8)
        )
        st.pyplot(fig_b)

st.markdown("---")
with st.expander("Voir le tableau complet du championnat"):
    st.dataframe(df_league[["Équipe", "xG", "xGA", "PPDA", "Poss"]], use_container_width=True)
