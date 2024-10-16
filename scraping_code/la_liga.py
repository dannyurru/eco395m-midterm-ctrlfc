import requests
from bs4 import BeautifulSoup
import csv
import os
import statistics

OUTPUT_DIR = "csv_collection"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "la_liga_data.csv")

headers = {
        "Accept": "*/*", 
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Chrome/58.0.3029.110",
        "Connection": "keep-alive",
        "Cookie": "SWID=75534310-463B-4EC6-CE90-8370E807F123;dcf=1; connectionspeed=full; country=us; edition=espn-en-us; edition-view=espn-en-us; region=ccpa"
        }

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Standing" ,"Team Name","Games Played", "Wins", "Draws", "Losses", "Goals For", "Goals Against", "Goal Difference", "Points", "Year"])

    for year in range(2003, 2024):
        url = f"https://www.espn.com/soccer/standings/_/league/ESP.1/season/{year}"
        rq = requests.get(url, headers=headers)
        html = rq.text
        soup = BeautifulSoup(html, features="html.parser")

        subhead = soup.find_all("th", title="", class_="tar subHeader__item--content Table__TH")

        teams = [row.get_text() for row in soup.find_all("span", class_="hide-mobile")]

        stats = [stat.get_text() for stat in soup.find_all("span", class_="stat-cell")]

        standings = list(range(1, len(teams) + 1))

        for i, team in enumerate(teams):
            stats_for_team = stats[i*8:(i+1)*8]
            writer.writerow([standings[i], team] + stats_for_team + [year])

with open(OUTPUT_PATH, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    data = [row for row in reader]

yearly_data = {}
for row in data:
    year = row[10]
    if year not in yearly_data:
        yearly_data[year] = []
    yearly_data[year].append(row)

for year, rows in yearly_data.items():
    goal_differences = []
    points = []
    for row in rows:
        goal_diff = int(row[8])
        point = int(row[9])
        goal_differences.append(goal_diff)
        points.append(point)
        
    min_goal_diff = min(goal_differences) - 1
    min_points = min(points) - 1

    std_goal_diff = statistics.stdev(goal_differences)
    std_points = statistics.stdev(points)

    for row in rows:
        goal_diff = int(row[8])
        point = int(row[9])
        rts = ((goal_diff - min_goal_diff) / std_goal_diff) * ((point - min_points) / std_points)
        row.append(rts)

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header + ["RTS"])
    for year, rows in yearly_data.items():
        writer.writerows(rows)