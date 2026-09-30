import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

st.set_page_config(page_title="Team Profile Dashboard", layout="wide")

# Styling CSS personnalisé
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 12px;
        border: 1px solid #EAEAEA;
    }
    .metric-title {
        font-size: 11px;
        color: #6C757D;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #111827;
    }
    .metric-sub {
        font-size: 10px;
        color: #9CA3AF;
    }
    .badge {
        background-color: #059669;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        float: right;
    }
    </style>
""", unsafe_allow_html=True)

# Base de données d'exemple
DATABASE = {
    "Arsenal": {"League": "Premier League", "Rank": "1st", "Form": "3-5-2", "PPG": 2.10, "Goals": 1.95, "xG": 1.90, "xGA": 0.85, "Poss": 62.5, "PPDA": 8.4},
    "Real Madrid": {"League": "LaLiga", "Rank": "1st", "Form": "4-3-3", "PPG": 2.25, "Goals": 2.15, "xG": 2.10, "xGA": 0.82, "Poss": 60.1, "PPDA": 9.1},
    "Paris Saint-Germain": {"League": "Ligue 1", "Rank": "1st", "Form": "4-3-3", "PPG": 2.35, "Goals": 2.40, "xG": 2.25, "xGA": 0.80, "Poss": 64.8, "PPDA": 7.5}
}

# Barre latérale pour la sélection
selected_team = st.sidebar.selectbox("Sélectionner une équipe", list(DATABASE.keys()))
data = DATABASE[selected_team]

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title(selected_team.upper())
    st.caption(f"{data['League']} • {data['Form']} • Saison 2026/2027")
with col_h2:
    st.markdown("<h3 style='text-align: right; color: #1E3A8A;'>POSSESSION-DOMINANT</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right; color: #6B7280; font-size: 11px;'>TEAM PROFILE COMPARED TO LEAGUE AVERAGE</p>", unsafe_allow_html=True)

st.markdown("---")

# Section Haute : Profile Radar + Key Metrics
col_top_left, col_top_right = st.columns([1, 1])

with col_top_left:
    st.subheader("Profile")
    st.caption("STYLE SCORE VS LEAGUE • DASHED RING = LEAGUE AVERAGE")
    
    params_main = ["Possession", "Build-Up\nPatience", "Directness", "Press\nIntensity", "Chance\nSuppression", "Chance\nCreation"]
    values_main = [85, 78, 35, 82, 70, 88]
    
    pizza = PyPizza(
        params=params_main,
        background_color="#FFFFFF",
        straight_line_color="#E5E7EB",
        straight_line_lw=1,
        last_circle_lw=1,
        other_circle_ls="--"
    )
    fig1, ax1 = pizza.make_pizza(
        values_main,
        figsize=(4.5, 4.5),
        kwargs_slices=dict(facecolor="#3B82F6", edgecolor="#1D4ED8", linewidth=1.5, alpha=0.7),
        kwargs_params=dict(color="#1F2937", fontsize=9, va="center")
    )
    st.pyplot(fig1)

with col_top_right:
    st.subheader("Key Metrics")
    st.caption("PER GAME • RANK AMONG LEAGUE TEAMS")
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f'<div class="metric-card"><span class="badge">1st</span><div class="metric-title">Points per game</div><div class="metric-value">{data["PPG"]}</div><div class="metric-sub">League avg 1.34</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><span class="badge" style="background-color:#D97706;">6th</span><div class="metric-title">xG</div><div class="metric-value">{data["xG"]}</div><div class="metric-sub">League avg 1.44</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><span class="badge">1st</span><div class="metric-title">Possession</div><div class="metric-value">{data["Poss"]}%</div><div class="metric-sub">League avg 50.0%</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><span class="badge">3rd</span><div class="metric-title">Goals</div><div class="metric-value">{data["Goals"]}</div><div class="metric-sub">League avg 1.39</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><span class="badge">3rd</span><div class="metric-title">xG Against</div><div class="metric-value">{data["xGA"]}</div><div class="metric-sub">League avg 1.43</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><span class="badge" style="background-color:#2563EB;">4th</span><div class="metric-title">PPDA</div><div class="metric-value">{data["PPDA"]}</div><div class="metric-sub">League avg 11.5</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Section Milieu : 3 Radars Détaillés
col_mid1, col_mid2, col_mid3 = st.columns(3)

def mini_radar(params, values):
    pizza = PyPizza(
        params=params, background_color="#FFFFFF",
        straight_line_color="#E5E7EB", straight_line_lw=1, last_circle_lw=1, other_circle_ls="--"
    )
    fig, ax = pizza.make_pizza(
        values, figsize=(3.5, 3.5),
        kwargs_slices=dict(facecolor="#818CF8", edgecolor="#4338CA", linewidth=1, alpha=0.6),
        kwargs_params=dict(color="#374151", fontsize=7, va="center")
    )
    return fig

with col_mid1:
    st.subheader("Build-Up")
    f1 = mini_radar(["Possession", "Passes", "Pass Acc %", "Passes/Poss", "Tempo", "Prog Passes", "Ball Security", "Long Pass %"], [80, 85, 88, 75, 60, 70, 82, 40])
    st.pyplot(f1)

with col_mid2:
    st.subheader("Chance Creation")
    f2 = mini_radar(["xG", "Shots", "xG/Shot", "Box Touches", "Box Entries", "Deep Comp.", "Crosses", "Shot Proximity"], [75, 70, 65, 80, 85, 78, 50, 60])
    st.pyplot(f2)

with col_mid3:
    st.subheader("Defending")
    f3 = mini_radar(["Press (PPDA)", "High Recov.", "Interceptions", "Def Duels %", "Aerial Won %", "Opp Pass Acc", "xG Against", "Shots Against"], [85, 80, 65, 55, 60, 75, 82, 78])
    st.pyplot(f3)

st.markdown("---")

# Section Basse : Charts Matplotlib
col_bot1, col_bot2, col_bot3 = st.columns([1.2, 1.2, 1])

with col_bot1:
    st.subheader("League Style Map")
    fig_map, ax_map = plt.subplots(figsize=(4, 3))
    ax_map.scatter([58.4], [9.1], color="#1E3A8A", s=80)
    ax_map.scatter([42.5, 48.0, 52.1], [13.2, 11.5, 10.2], color="#9CA3AF", alpha=0.6, s=30)
    ax_map.set_xlabel("Possession %", fontsize=8)
    ax_map.set_ylabel("PPDA (More Intense ↑)", fontsize=8)
    ax_map.invert_yaxis()
    ax_map.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig_map)

with col_bot2:
    st.subheader("xG Trend")
    fig_trend, ax_trend = plt.subplots(figsize=(4, 3))
    ax_trend.plot([1.2, 1.5, 1.3, 1.8, 2.1, 1.9, 2.2], label="xG For", color="#1E3A8A", linewidth=2)
    ax_trend.plot([0.8, 0.9, 0.7, 1.1, 0.8, 0.9, 0.6], label="xG Against", color="#F59E0B", linewidth=2)
    ax_trend.legend(fontsize=7)
    ax_trend.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig_trend)

with col_bot3:
    st.subheader("Shape & Attack Mix")
    st.markdown("**FORMATIONS USED**")
    st.progress(0.72, text="3-5-2 (72%)")
    st.progress(0.18, text="3-4-2-1 (18%)")
    st.markdown("**ATTACK MIX**")
    st.caption("Positional: 72% | Counter: 18% | Set piece: 10%")
