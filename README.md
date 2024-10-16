# Project Goals
We want to collect the data from the Big 5 football leagues from 2003 to 2023 inclusive and use the data to create a "Team Strength" measure we can use to compare between leagues.

To collect the data for the Big 5 football leagues, we used the following five links:

Italy: https://www.espn.com/soccer/standings/_/league/ita.1/season/2003

Germany: https://www.espn.com/soccer/standings/_/league/ger.1/season/2003

France: https://www.espn.com/soccer/standings/_/league/fra.1/season/2003

England: https://www.espn.com/soccer/standings/_/league/eng.1/season/2003

Spain https://www.espn.com/soccer/standings/_/league/esp.1/season/2003

(These links will give you the statistics for the 2003-2004 season for each league.)

These links contain the following information in consecutive columns, regardless of league:
The names of the teams in each league in order of their season standing,
The number of games played,
The number of games won by each team per season,
The number of games ended in a draw by each team per season,
The number of games lost by each team per season,
The number of goals made by each team per season,
The number of goals against each team per season,
The difference between goals for and goals against for each team per season,
The number of points given to each team per season

The way that the URLs are designed make it so the year that the season was played appear as the last four digits of the link.

To collect the data, we run code that will use a base URL (i.e. For La Liga: "https://www.espn.com/soccer/standings/_/league/esp.1/season/") 
and a "season" string, which are the years 2003 to 2023, add these two strings together to create the URL per season,and run a for loop that 
will scrape the aforementioned columns with their respective headings and create a csv file with this information. 

We are creating the following columns using data that we either scraped or calculated:
The year of the season,
The standing of each team per season,
The "Relative Team Strength (RTS)" for each team per season

We are calculating the RTS measure for each team by calculating the following:

((Goal Difference - the minimum of each Goal Difference)/(the standard deviation of Goal Difference)) x ((Points - the average number of points)/(the standard deviation of Points))

# Findings


# Reproducibility
To reproduce the data, you must use ESPN's soccer standing website. 