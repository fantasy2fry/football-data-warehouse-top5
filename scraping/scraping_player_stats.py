import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://fbref.com"
USER_AGENT = {"User-Agent": "Mozilla/5.0"}

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
    print(url)
    try:
        res = requests.get(url, headers=USER_AGENT)
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table')
        if table is None:
            print(f"No table for {team_name} {season}/{season+1}")
            return None

        headers = [th.get('data-stat') for th in table.find_all('th') if th.get('data-stat')]
        rows = []
        for row in table.tbody.find_all('tr'):
            if row.get('class') and 'thead' in row['class']:
                continue
            row_data = [td.text.strip() for td in row.find_all('td')]
            if row_data:
                rows.append(row_data)

        df = pd.DataFrame(rows, columns=headers[1:])  # skip row index column
        df["Season"] = f"{season}/{season+1}"
        df["Team"] = team_name
        return df
    except Exception as e:
        print(f"Error for {team_name} {season}: {e}")
        return None

def main():
    all_data = []
    for league, url in LEAGUE_URLS.items():
        print(f"Fetching teams from {league}...")
        teams = get_squad_links(url)
        print(teams)
        for season in SEASONS:
            for team_name, team_id in teams.items():
                print(f"Scraping {team_name} {season}/{season+1}")
                df = scrape_season_team(season, team_name, team_id)
                print(df)
                if df is not None:
                    df["League"] = league
                    all_data.append(df)
                time.sleep(4)  # polite delay

    combined = pd.concat(all_data, ignore_index=True)
    combined.to_csv("fbref_top5_2017_2025.csv", index=False)
    print("Saved to fbref_top5_2017_2025.csv")

if __name__ == "__main__":
    main()
