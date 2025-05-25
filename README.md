# Football Data Warehouse for Top 5 European Leagues

**Team Name:** Top5  
**Team Members:** Mateusz Deptuch, Norbert Frydrysiak  
**Project Topic:** Analysis of Football Players and Teams from the Top 5 European Leagues  
**Leagues Covered:** La Liga, Premier League, Bundesliga, Serie A, Ligue 1

## Project Goal

To build a data warehouse that supports the analysis of seasonal statistics for football players and teams.

### Benefits
- Centralized data source for seasonal and historical comparisons.
- Enables cross-sectional reports (e.g., top scorers, teams with highest xG).
- Useful for sports analysts, scouts, journalists, and data enthusiasts.

## Data Sources

| Source          | Data Scope                          | Format       | Access         | Refresh Frequency |
|-----------------|--------------------------------------|--------------|----------------|--------------------|
| FBref           | Player & match statistics            | HTML/CSV     | Public (scraping) | Weekly (automated) |
| Wikipedia       | League & Ballon d’Or winners         | HTML         | Public         | Seasonally (manual)|
| Transfermarkt   | Club info, managers, squads (auxiliary) | HTML     | Public         | TBD                |

## ETL Process

- Scraping and loading data into a star schema model.
- Standardizing player and club names (e.g., no special characters or capital letters).
- Type conversions (e.g., dates, integers, strings).
- Merging data from multiple sources using standardized keys.
- Calculating derived metrics (e.g., xG - Goals).
- Handling nulls (e.g., using "N/A").
- Loading into the data warehouse.

## Data Warehouse Schema

**Fact Tables:**
- `PlayerStatsFact`
- `MatchStatsFact`

**Dimension Tables:**
- `DimPlayer`, `DimClub`, `DimSeason`, `DimDate`, `DimMatchProfile`

## Key Metrics

- MinutesPlayed, MatchesPlayed, GamesStarted
- Goals, Assists, PenaltyKicksMade
- ExpectedGoals (xG), ExpectedAssists (xA)
- ProgressivePasses, ProgressiveCarries
- YellowCards, RedCards
- GoalsFor, GoalsAgainst, ExpectedGoalsAllowed (xGA)
- Possession, Attendance

## Descriptive Attributes

Player info, club details, match metadata, and season-level indicators such as:
- Ballon d’Or winner, league champions
- Match dates, referee, formation, opponent formation

## Planned Reports

1. **Player Rankings (per season):**
    - Top scorers, assisters, xG leaders, performance efficiency

2. **Team Comparisons:**
    - xG vs xGA, ball possession, match attendance

3. **Season Overview:**
    - League champions, Ballon d’Or winner, most popular formations

## Example Pages for Scraping

- [FBref Squad Stats](https://fbref.com/en/squads/206d90db/2024-2025/all_comps/Barcelona-Stats-All-Competitions)
- [Wikipedia Player Info](https://en.wikipedia.org/wiki/Robert_Lewandowski)

---

**Architecture:** Classic ETL pipeline → Star Schema Data Warehouse → BI Reports.
