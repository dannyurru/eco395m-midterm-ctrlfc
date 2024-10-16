import os
import csv

BASE_DIR = "csv_collection"
OUTPUT_PATH = os.path.join(BASE_DIR, "europesorted.csv")

csv_files = [
    "bundesliga_data.csv",
    "la_liga_data.csv",
    "epl.csv",
    "french_ligue_data.csv",
    "seriea.csv"
]

combined_data = []

for file in csv_files:
    file_path = os.path.join(BASE_DIR, file)
    try:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Debugging: print the keys of the current row
                print(f"Processing row keys: {row.keys()}")
                
                # Check if the key exists before conversion
                if 'Relative Team Strength' in row:
                    # Attempt to convert the value to float
                    try:
                        row['Relative Team Strength'] = float(row['Relative Team Strength'])
                        combined_data.append(row)
                    except ValueError as ve:
                        print(f"Could not convert '{row['Relative Team Strength']}' to float: {ve}")
                else:
                    print(f"Key 'Relative Team Strength' not found in row: {row}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Sort the combined data
combined_data_sorted = sorted(combined_data, key=lambda x: x['Relative Team Strength'], reverse=True)

# Write the sorted data to a new CSV file
with open(OUTPUT_PATH, "w", newline="") as outfile:
    fieldnames = ['Standing', 'Team Name', 'Games Played', 'Wins', 'Draws', 'Losses', 
                  'Goals For', 'Goals Against', 'Goal Difference', 'Points', 'Year', 'Relative Team Strength']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in combined_data_sorted:
        writer.writerow(row)

print(f"Combined and sorted data has been written to {OUTPUT_PATH}")
