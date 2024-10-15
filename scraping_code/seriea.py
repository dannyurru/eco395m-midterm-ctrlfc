import os
import requests
import csv
from pprint import pprint

from bs4 import BeautifulSoup

SEASONS = [str(year) for year in range(2003, 2024)]

def soupify_season(season):
    """Given a season, return the soup from the ESPN site for Serie A standings."""
    URL = "https://www.espn.com/soccer/standings/_/league/ita.1/season/"
    url = URL + season

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'User-Agent': '58.0.3029.110',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data for season {season}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_table(soup):
    if not soup:
        return None
    return soup.find("div", class_="ResponsiveTable ResponsiveTable--fixed-left")

def get_team_names_from_table(table):
    if not table:
        return []
    
    team_name_column = table.find("tbody", class_="Table__TBODY")
    teams_tr = team_name_column.find_all("tr", class_=["Table__TR Table__TR--sm Table__even", "filled Table__TR Table__TR--sm Table__even"])
    team_names = []
    for team in teams_tr:
        team_span = team.find("span", class_="hide-mobile")
        if team_span:
            team_names.append(team_span.find("a", class_="AnchorLink").string)
    return team_names

def get_stats_from_table(table):
    if not table:
        return []
    
    stats_section = table.find("div", class_="Table__ScrollerWrapper relative overflow-hidden")
    stats_tbody = stats_section.find("tbody", class_="Table__TBODY")
    stats_rows = stats_tbody.find_all("tr", class_=["Table__TR Table__TR--sm Table__even", "filled Table__TR Table__TR--sm Table__even"])
    stats = []
    for row in stats_rows:
        stats_tds = row.find_all("td", class_="Table__TD")
        stats.append(
            {
                "GP": stats_tds[0].string,
                "W": stats_tds[1].string,
                "D": stats_tds[2].string,
                "L": stats_tds[3].string,
                "GF": stats_tds[4].string,
                "GA": stats_tds[5].string,
                "GD": stats_tds[6].string,
                "P": stats_tds[7].string,
            }
        )
    return stats

def get_team_data_from_soup(season):
    soup = soupify_season(season)
    table = get_table(soup)

    if not table:
        return {"year": season, "names": [], "stats": []}

    team_names = get_team_names_from_table(table)
    stats = get_stats_from_table(table)
    return {"year": season, "names": team_names, "stats": stats}

def write_data_to_csv(data, path):
    """Write data to the CSV file."""
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, "w+", newline="") as outfile:
        outfile.write("Team Name,Games Played,Wins,Draws,Losses,Goals For,Goals Against,Goal Difference,Points,Year\n")
        for dict_ in data:
            for i in range(len(dict_["names"])):
                outfile.write(f'{dict_["names"][i]},{dict_["stats"][i]["GP"]},{dict_["stats"][i]["W"]},{dict_["stats"][i]["D"]},{dict_["stats"][i]["L"]},{dict_["stats"][i]["GF"]},{dict_["stats"][i]["GA"]},{dict_["stats"][i]["GD"]},{dict_["stats"][i]["P"]},{dict_["year"]}\n')

if __name__ == "__main__":
    BASE_DIR = os.path.expanduser("~/OneDrive/Documents/eco395m-midterm-project/csv_collection")
    CSV_PATH = os.path.join(BASE_DIR, "seriea.csv")

    data = []
    for year in SEASONS:
        team_data = get_team_data_from_soup(year)
        data.append(team_data)

    write_data_to_csv(data, CSV_PATH)

