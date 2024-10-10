import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.premierleague.com/tables"

season_code = 578
home_away = "home"

payload = {
    "co": 1
    "se": season_code
    "ha": home_away
}



def get_table(soup):
    """Given a soup input, return a list of the table element"""
    return soup.find_all("tbody", class_ = "league-table__tbody isPL")

