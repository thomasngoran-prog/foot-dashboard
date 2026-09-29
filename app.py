import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

st.set_page_config(page_title="Football Data Scraper 2026/2027", layout="centered")

st.title("⚽ Dashboard Tactique & Data Scraping")
st.caption("Données extraites en direct : Understat | FBref | Opta")
st.markdown("---")

# Dictionnaire de correspondance des ligues
LEAGUES_MAPPING = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (D1)": {"understat": "EPL", "fbref": "9/Premier-League-Stats"},
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 EFL Championship (D2)": {"understat": "Championship", "fbref": "10/Championship-Stats"},
    "🇪🇸 LaLiga (D1)": {"understat": "La_liga", "fbref": "12/La-Liga-Stats"},
    "🇪🇸 LaLiga Hypermotion (D2)": {"understat": "La_liga2", "fbref": "17/La-Liga-2-Stats"},
    "🇩🇪 Bundesliga (D1)": {"understat": "Bundesliga", "fbref": "20/Bundesliga-Stats"},
    "🇩🇪 2. Bundesliga (D2)": {"understat": "2_Bundesliga", "fbref": "33/2-Bundesliga-Stats"},
    "🇮🇹 Serie A (D1)": {"understat": "Serie_A", "fbref": "11/Serie-A-Stats"},
    "🇮🇹 Serie B (D2)": {"understat": "Serie_B", "fbref": "18/Serie-B-Stats"},
    "🇫🇷 Ligue 1 (D1)": {"understat": "Ligue_1", "fbref": "13/Ligue-1-Stats"},
    "🇫🇷 Ligue 2 (D2)": {"understat": "Ligue_2", "fbref": "60/Ligue-2-Stats"}
}

selected_league_label = st.selectbox("Sélectionner un Championnat", list(LEAGUES_MAPPING.keys()))
league_info = LEAGUES_MAPPING[selected_league_label]

# Fonction de Scraping pour Understat (xG, xGA, PPDA, toutes les équipes)
@st.cache_data(ttl=3600)
def scrape_understat_league(league_code, season=2026):
    url = f"https://understat.com/league/{league_code}/{season}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraction du script JSON contenant les données de toutes les équipes
        scripts = soup.find_all('script')
        teams_data = None
        for script in scripts:
            if 'teamsData' in str(script.string):
                content = str(script.string)
                start = content.find("JSON.parse('") + 12
                end = content.find("')\n;") or content.find("');")
                json_raw = content[start:end].encode('utf-8').decode('unicode_escape')
                import json
                teams_data = json.loads(json_raw)
                break
                
        if not teams_data:
            return None

        # Structuration dans un DataFrame Pandas
        parsed_teams = []
        for team_id, team_info in teams_data.items():
            title = team_info['title']
            history = team_info['history']
            
            # Calcul des moyennes par match sur la saison 2026/2027
            matches_played = len(history)
            if matches_played == 0:
                continue
                
            total_xg = sum(float(m['xG']) for m in history)
            total_xga = sum(float(m['xGA']) for m in history)
            total_ppda = sum(float(m['ppda']['att']) / max(1, float(m['ppda']['def'])) for m in history)
            
            parsed_teams.append({
                "Équipe": title,
                "Matchs": matches_played,
                "xG/M": round(total_xg / matches_played, 2),
                "xGA/M": round(total_xga / matches_played, 2),
                "PPDA": round(total_ppda / matches_played, 1)
            })
            
        df = pd.DataFrame(parsed_teams)
        return df.sort_values(by="Équipe").reset_index(drop=True)
    
    except Exception as e:
        st.error(f"Erreur de scraping Understat : {e}")
        return None

# Lancement du scraper avec indicateur de chargement
with st.spinner("Scraping des données en direct pour la saison 2026/2027..."):
    df_teams = scrape_understat_league(league_info["understat"], season=2026)

if df_teams is not None and not df_teams.empty:
    # Liste dynamique des 20 équipes extraites par le scraper
    team_list = df_teams["Équipe"].tolist()
    selected_team = st.selectbox("Sélectionner une Équipe (Extraites dynamiquement)", team_list)
    
    # Récupération des données de l'équipe sélectionnée
    team_stats = df_teams[df_teams["Équipe"] == selected_team].iloc[0]
    
    st.markdown(f"### 📊 Stats en direct : {selected_team} (2026/2027)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("xG / Match (Understat)", team_stats["xG/M"])
        st.metric("xGA / Match (Understat)", team_stats["xGA/M"])
    with col2:
        st.metric("PPDA Pressing (Understat)", team_stats["PPDA"])
        st.metric("Matchs Joués", team_stats["Matchs"])
        
    st.markdown("---")
    
    # Affichage du classement complet de la ligue issu du scraping
    with st.expander("Voir le tableau complet des 20 équipes scrapées"):
        st.dataframe(df_teams, use_container_width=True)

else:
    st.warning("Impossible de scraper les données en direct pour le moment. Vérifiez l'accès à Understat.")
