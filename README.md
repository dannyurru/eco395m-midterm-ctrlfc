# Project Goal
We want to collect the data from the Big 5 football leagues from 2003 to 2023 inclusive and use the data to create a " Relative Team Strength" (RTS) measure we can use to compare between leagues. 
We can use the RTS to compare the competitiveness of each season within leagues, and to standarize teams in order to measure across leagues.

# Data Collection
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

We are creating the following columns using data that we either scraped or calculated from existing data:

The year of the season,

The standing of each team per season,

The "Relative Team Strength (RTS)" for each team per season

# Our Measure
We are calculating the RTS measure for each team by calculating the following:

(Goal Difference - (Minimum Goal Difference - 1)/std(Goal Difference) * (Points - (Minimum Points - 1))/std(Points)

=======
We will implicitly place scores in brackets based on their RTS:

0-5: Poor Team Strength

5-10: Fair Team Strength

10-15: Good Team Strength

15+: Great Team Strength

# Limitations
Some limitations of our data and measurements include:

Not including seasons before 2003

Our measure is strong at distinguishing differences in the strength of higher-performing teams, but weak at distinguishing the flaws in lower-performing teams



# Findings
Highest RTS score from 2003-2023 seasons in each league:
English Premier League: Manchester United (2007-08) [RTS: 16.63]
La Liga: Barcelona (2018) [17.79]



# Weaknesses of Data and Findings
The structure of the RTS calculation makes it so the team in the lowest standing of the season would have an RTS of zero. However, when running the calculations, two issues seem to arise:

The team in the last standing will have a RTS that is greater than zero

The team in the last standing will have an RTS that is not the lowest of their respective season



# Reproducibility
To reproduce the data, you must use ESPN's website on soccer standings, regardless of the league. Copy either of the 5 links listed above without the year at the end and insert it into the base URL of either code to define it. After this, the code should create the CSV file after running it. 
