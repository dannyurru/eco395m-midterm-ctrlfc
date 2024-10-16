import os
import csv

BASE_DIR = "csv_collection"
OUTPUT_PATH = os.path.join(BASE_DIR, "europesorted.csv")


league_mapping = {
    "bundesliga_data.csv": "Bundesliga",
    "la_liga_data.csv": "La Liga",
    "epl.csv": "English Premier League",
    "french_ligue_data.csv": "French Ligue 1",
    "seria.csv": "Serie A"
}

combined_data = []

for file in league_mapping.keys():
    file_path = os.path.join(BASE_DIR, file)
    try:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                
                print(f"Processing row keys: {row.keys()}")
                
                if 'Relative Team Strength' in row:
                    
                    try:
                        row['Relative Team Strength'] = float(row['Relative Team Strength'])
                        
                        row['League'] = league_mapping[file]
                        combined_data.append(row)
                    except ValueError as ve:
                        print(f"Could not convert '{row['Relative Team Strength']}' to float: {ve}")
                else:
                    print(f"Key 'Relative Team Strength' not found in row: {row}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

combined_data_sorted = sorted(combined_data, key=lambda x: x['Relative Team Strength'], reverse=True)

with open(OUTPUT_PATH, "w", newline="") as outfile:
    fieldnames = ['League', 'Standing', 'Team Name', 'Games Played', 'Wins', 'Draws', 'Losses', 
                  'Goals For', 'Goals Against', 'Goal Difference', 'Points', 'Year', 'Relative Team Strength']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in combined_data_sorted:
        writer.writerow(row)

print(f"Combined and sorted data has been written to {OUTPUT_PATH}")
