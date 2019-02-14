import requests
import bs4

first_url = 'https://easyodds.com/horse-racing#'

def get_html(url):
    results = requests.get(url)
    html = bs4.BeautifulSoup(results.text)
    return html

def get_gb_racecard_urls(html):
    racecard = html.select('div.racecard')
    gb_racecard = str(racecard[0])
    gb_html = bs4.BeautifulSoup(gb_racecard)
    gb_matches = gb_html.select('table.matches-list')
    racecard_urls = []
    for match in gb_matches:
        for url in match.find_all('a'):
            url = url.get('href')
            racecard_urls.append(url)
    return racecard_urls

def get_bet_table(racecard_html):
    bet_table = racecard_html.find_all('table')[1]
    bet_body = bet_table.tbody
    bets = bet_body.find_all('tr')
    return bets

def get_horse_names(bet_table):
    names = []
    for bet in bet_table:
        if 'tr-odds' in bet['class']:
            name = bet.get('data-selection-name')
            names.append(name)
    return names

def get_best_price(bet_table):
    for bet in bet_table:
        if 'tr-odds' in bet['class']:
            odds = bet.find_all('td')
    return odds


if __name__ == '__main__':
    html = get_html(first_url)
    gb_cards = get_gb_racecard_urls(html)
    early_race = gb_cards[0]
    early_html = get_html(early_race)
    early_bets = get_bet_table(early_html)
    early_horses = get_horse_names(early_bets)
