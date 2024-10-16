import os
import csv
import requests
import statistics

from pprint import pprint

from bs4 import BeautifulSoup


SEASONS = []
for year in range(2003, 2024):
    SEASONS.append(f"{year}")


def soupify_season(season):
    """Given a season that extended from season to season + 1, return the soup taken from the ESPN site for EPL scoring table"""

    URL = "https://www.espn.com/soccer/standings/_/league/ENG.1/season/"
    url = URL + season

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, features="html.parser")

    return soup


def get_table(soup):
    """Given the soup, return the object representing the scoring table"""

    return soup.find("div", class_="ResponsiveTable ResponsiveTable--fixed-left")


def get_team_names_from_table(table):
    """Given the table, return a list with every team name in order"""

    team_name_column = table.find("tbody", class_="Table__TBODY")
    teams_tr = team_name_column.find_all(
        "tr",
        class_=[
            "Table__TR Table__TR--sm Table__even",
            "filled Table__TR Table__TR--sm Table__even",
        ],
    )
    team_names = []
    for i in range(len(teams_tr)):
        team_span = teams_tr[i].find("span", class_="hide-mobile")
        team_names.append(team_span.find("a", class_="AnchorLink").string)
    return team_names


def get_stats_from_table(table):
    """Given the table, return a list of dicts which each represent the stats for one team"""

    stats_section = table.find(
        "div", class_="Table__ScrollerWrapper relative overflow-hidden"
    )
    stats_tbody = stats_section.find("tbody", class_="Table__TBODY")
    stats_rows = stats_tbody.find_all(
        "tr",
        class_=[
            "Table__TR Table__TR--sm Table__even",
            "filled Table__TR Table__TR--sm Table__even",
        ],
    )
    stats = []
    for i in range(len(stats_rows)):
        stats_tds = stats_rows[i].find_all("td", class_="Table__TD")
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
    team_data = {"year": season, "names": team_names, "stats": stats}

    return team_data


def write_data_to_csv(data, path):
    """Writing data to the CSV file"""

    with open(path, "w+") as outfile:
        outfile.write(
            "Standing,Team Name,Games Played,Wins,Draws,Losses,Goals For,Goals Against,Goal Difference,Points,Year,Relative Team Strength\n"
        )
        for dict_ in data:
            for i in range(len(dict_["names"])):
                minimum_GD = 100
                minimum_points = 100
                GD_diffs = []
                points_ = []
                for j in range(len(dict_["names"])):
                    points_.append(int(dict_["stats"][j]["P"]))
                    minimum_GD = min(minimum_GD, int(dict_["stats"][j]["GD"]))
                    minimum_points = min(minimum_points, int(dict_["stats"][j]["P"]))
                for j in range(len(dict_["names"])):
                    GD_diffs.append(int(dict_["stats"][j]["GD"]) - (minimum_GD - 1))
                stdev_GD_diff = statistics.stdev(GD_diffs)
                stdev_points = statistics.stdev(points_)
                dict_["RTS"] = []
                for j in range(len(dict_["names"])):
                    team_rts = round(
                        (int(GD_diffs[j]) / stdev_GD_diff)
                        * (
                            (int(dict_["stats"][j]["P"]) - (minimum_points - 1))
                            / stdev_points
                        ),
                        2,
                    )
                    dict_["RTS"].append(team_rts)



                outfile.write(
                    f'{i + 1},{dict_["names"][i]},{dict_["stats"][i]["GP"]},{dict_["stats"][i]["W"]},{dict_["stats"][i]["D"]},{dict_["stats"][i]["L"]},{dict_["stats"][i]["GF"]},{dict_["stats"][i]["GA"]},{dict_["stats"][i]["GD"]},{dict_["stats"][i]["P"]},{dict_["year"]},{float(dict_["RTS"][i])}\n'
                )

if __name__ == "__main__":

    BASE_DIR = "csv_collection"
    CSV_PATH = os.path.join(BASE_DIR, "epl.csv")

    data = []

    for year in SEASONS:
        team_data = get_team_data_from_soup(year)
        data.append(team_data)

    write_data_to_csv(data, CSV_PATH)