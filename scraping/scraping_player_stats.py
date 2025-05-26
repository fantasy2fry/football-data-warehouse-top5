import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from unidecode import unidecode

BASE_URL = "https://fbref.com"
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# Mapping: league name → URL fragment used on squad index pages
LEAGUE_URLS = {
    "Premier League": "/en/comps/9/Premier-League-Stats",
    "La Liga": "/en/comps/12/La-Liga-Stats",
    "Bundesliga": "/en/comps/20/Bundesliga-Stats",
    "Serie A": "/en/comps/11/Serie-A-Stats",
    "Ligue 1": "/en/comps/13/Ligue-1-Stats"
}

SEASONS = list(range(2017, 2024))  # 2017–2024
SEASONS = list(range(2023, 2024))

def get_squad_links(league_url):
    """Returns a dict: {team_name: team_id} for the current league"""
    r = requests.get(BASE_URL + league_url, headers=USER_AGENT)
    soup = BeautifulSoup(r.text, "html.parser")
    squad_links = soup.select("table.stats_table a[href*='/squads/']")
    teams = {}
    for a in squad_links:
        href = a["href"]
        name = a.text.strip()
        parts = href.split("/")
        if len(parts) > 3:
            team_id = parts[3]
            teams[name] = team_id
    return teams

def scrape_season_team(season, team_name, team_id):
    """Scrapes one season for one team, returns a DataFrame"""
    url = f"{BASE_URL}/en/squads/{team_id}/{season}-{season+1}/all_comps/{team_name.replace(' ', '-')}-Stats-All-Competitions"
    try:
        dfs = pd.read_html(url)
        if not dfs:
            print(f"No data found for {team_name} {season}")
            return None
        player_stats = dfs[0]  # Player stats table
        match_stats = dfs[5]   # Match stats table
        #save the data
        player_stats["Season"] = f"{season}-{season+1}"
        player_stats["Team_Scraping"] = team_name
        match_stats["Season"] = f"{season}-{season+1}"
        match_stats["Team_Scraping"] = team_name
        player_stats.to_csv(f"data_ps/player_stats_{team_name}_{season}.csv", index=False)
        match_stats.to_csv(f"data_ms/match_stats_{team_name}_{season}.csv", index=False)
        return player_stats, match_stats
    except Exception as e:
        print(f"Error for {team_name} {season}: {e}")
        return None

def main():
    for league, url in LEAGUE_URLS.items():
        print(f"Fetching teams from {league}...")
        teams = get_squad_links(url)
        print(teams)
        for season in SEASONS:
            for team_name, team_id in teams.items():
                print(f"Scraping {team_name} {season}/{season+1}")
                scrape_season_team(season, team_name, team_id)
                time.sleep(4)  # polite delay
    print("Saved to All CSV files in data_ps and data_ms folders")

if __name__ == "__main__":
    main()
