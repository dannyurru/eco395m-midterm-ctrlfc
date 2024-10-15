import requests
from bs4 import BeautifulSoup

import os
import csv
import requests

from pprint import pprint

from bs4 import BeautifulSoup


SEASONS = []
for year in range(2003, 2024):
        SEASONS.append(f"{year}")


def soupify_season(season):
    """Given a season that extended from season to season + 1, return the soup taken from the ESPN site for Serie A scoring table"""

    URL = "https://www.espn.com/soccer/standings/_/league/ita.1/season/"
    url = URL + season

    headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept' : '*/*',
    'Cookie' : 'SWID=CFDF631C-A353-4440-C439-59AABF1B32F9; _dcf=1; connectionspeed=full; country=us; edition=espn-en-us; edition-view=espn-en-us; region=ccpa',
    'Cache-Control' : 'no-cache',
    'User-Agent' : '58.0.3029.110',
    'Connection' : 'keep-alive'
    }

    response = requests.get(url, headers = headers)
    html = response.text
    soup = BeautifulSoup(html, features = "html.parser")

    return soup

def get_table(soup):
    """Given the soup, return the object representing the scoring table"""

    return soup.find("div", class_ = "ResponsiveTable ResponsiveTable--fixed-left")

def get_team_names_from_table(table):
    """Given the table, return a list with every team name in order"""

    team_name_column = table.find("tbody", class_ = "Table__TBODY")
    teams_tr = team_name_column.find_all("tr", class_ = ["Table__TR Table__TR--sm Table__even", "filled Table__TR Table__TR--sm Table__even"])
    team_names = []
    for i in range(len(teams_tr)):
        team_span = teams_tr[i].find("span", class_ = "hide-mobile")
        team_names.append(team_span.find("a", class_ = "AnchorLink").string)
    return team_names

def get_stats_from_table(table):
    """Given the table, return a list of dicts which each represent the stats for one team"""

    stats_section = table.find("div", class_ = "Table__ScrollerWrapper relative overflow-hidden")
    stats_tbody = stats_section.find("tbody", class_ = "Table__TBODY")
    stats_rows = stats_tbody.find_all("tr", class_ = ["Table__TR Table__TR--sm Table__even", "filled Table__TR Table__TR--sm Table__even"])
    stats = []
    for i in range(len(stats_rows)):
        stats_tds = stats_rows[i].find_all("td", class_ = "Table__TD")
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
    """Returns a dict with team data for a particular season taken as a parameter"""

    soup = soupify_season(season)
    table = get_table(soup)

    team_names = get_team_names_from_table(table)
    stats = get_stats_from_table(table)
    team_data = {
        "year": season,
        "names": team_names,
        "stats": stats
    }

    return team_data

def write_data_to_csv(data, path):
    """Writing data to the CSV file"""

    with open(path, "w+") as outfile:
        outfile.write("Team Name,Games Played,Wins,Draws,Losses,Goals For,Goals Against,Goal Difference,Points,Year\n")
        for dict_ in data:
            for i in range(len(dict_["names"])):
                outfile.write(f'{dict_["names"][i]},{dict_["stats"][i]["GP"]},{dict_["stats"][i]["W"]},{dict_["stats"][i]["D"]},{dict_["stats"][i]["L"]},{dict_["stats"][i]["GF"]},{dict_["stats"][i]["GA"]},{dict_["stats"][i]["GD"]},{dict_["stats"][i]["P"]},{dict_["year"]}\n')

    
if __name__ == "__main__":

    BASE_DIR = os.path.expanduser("~/OneDrive/Documents/eco395m-midterm-project/scraping_code")

    CSV_PATH = os.path.join(BASE_DIR, "seriea.csv")

    data = []

    for year in SEASONS:
        team_data = get_team_data_from_soup(year)
        data.append(team_data)
    
    write_data_to_csv(data, CSV_PATH)