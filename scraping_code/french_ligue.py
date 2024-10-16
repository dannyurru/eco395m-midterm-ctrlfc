import os
import csv
import requests
from bs4 import BeautifulSoup
import statistics

OUTPUT_DIR = "csv_collection"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "french_ligue_data.csv")

headers = {
    "Accept": "/", 
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Chrome/58.0.3029.110",
    "Connection": "keep-alive",
    "Cookie": "SWID=75534310-463B-4EC6-CE90-8370E807F123;dcf=1; connectionspeed=full; country=us; edition=espn-en-us; edition-view=espn-en-us; region=ccpa"
}

def fetch_data_for_year(year):
    url = f"https://www.espn.com/soccer/standings/_/league/FRA.1/season/{year}"
    try:
        rq = requests.get(url, headers=headers, timeout=10)
        rq.raise_for_status()  # Ensure we catch bad requests (4xx, 5xx)
    except requests.RequestException as e:
        print(f"Failed to fetch data for year {year}: {e}")
        return None
    return rq.text

def parse_html(html):
    soup = BeautifulSoup(html, features="html.parser")
    teams = [row.get_text() for row in soup.find_all("span", class_="hide-mobile")]
    stats = [stat.get_text() for stat in soup.find_all("span", class_="stat-cell")]
    return teams, stats

def calculate_rts_for_year(rows):
    goal_differences = [int(row[8]) for row in rows]
    points = [int(row[9]) for row in rows]
    
    min_goal_diff = min(goal_differences) - 1
    min_points = min(points) - 1

    std_goal_diff = statistics.stdev(goal_differences) if len(goal_differences) > 1 else 1
    std_points = statistics.stdev(points) if len(points) > 1 else 1

    for row in rows:
        goal_diff = int(row[8])
        point = int(row[9])
        rts = ((goal_diff - min_goal_diff) / std_goal_diff) * ((point - min_points) / std_points)
        row.append(round(rts, 2))

def scrape_ligue_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_data = []
    for year in range(2003, 2024):
        html = fetch_data_for_year(year)
        if not html:
            continue
        teams, stats = parse_html(html)
        standings = list(range(1, len(teams) + 1))

        # Combine teams and stats into rows
        rows = []
        for i, team in enumerate(teams):
            stats_for_team = stats[i*8:(i+1)*8]
            row = [standings[i], team] + stats_for_team + [year]
            rows.append(row)
        
        # Calculate RTS for this year and append to the data
        calculate_rts_for_year(rows)
        all_data.extend(rows)
    
    return all_data

def write_to_csv(data):
    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Standing", "Team Name", "Games Played", "Wins", "Draws", "Losses", 
                         "Goals For", "Goals Against", "Goal Difference", "Points", "Year", "Relative Team Strength"])
        writer.writerows(data)

if __name__ == "__main__":
    ligue_data = scrape_ligue_data()
    if ligue_data:
        write_to_csv(ligue_data)
    else:
        print("No data to write.")
