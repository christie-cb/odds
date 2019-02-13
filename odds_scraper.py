import requests
import bs4

url = 'https://easyodds.com/horse-racing#'

def get_html(url):
    results = requests.get(url)
    html = bs4.BeautifulSoup(results.text)
    return html

def get_uk_times(html):
    times = html.find_all(class_="r_time")
    uk_racecard = html.findAll("div", {"class": "racecard", "data-group": "united-kingdom"})
    times = uk_racecard.find_all(class_="r_time")
    return times 
