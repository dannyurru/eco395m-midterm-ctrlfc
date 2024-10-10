import requests
from bs4 import BeautifulSoup

base_url = "https://www.espn.com/soccer/standings/_/league/ita.1/season/"
seasons = [f"{year}/{year+1}" for year in range(2003, 2024)]