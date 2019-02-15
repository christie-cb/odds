import requests
import bs4

first_url = 'https://easyodds.com/horse-racing#'

def get_html(url):
    results = requests.get(url)
    html = bs4.BeautifulSoup(results.text, "html.parser")
    return html

def get_gb_urls(html):
    racecard = html.select('div.racecard')
    gb_racecard = str(racecard[0])
    gb_html = bs4.BeautifulSoup(gb_racecard, "html.parser")
    gb_matches = gb_html.select('table.matches-list')
    racecard_urls = []
    for match in gb_matches:
        for url in match.find_all('a'):
            url = url.get('href')
            racecard_urls.append(url)
    return racecard_urls

def get_bet_table(racecard_html):
    bet_table = racecard_html.find_all('table')[1]
    table_body = bet_table.tbody
    return table_body 

def get_horse_names(bet_table):
    names = []
    for bet in bet_table:
        if 'tr-odds' in bet['class']:
            name = bet.get('data-selection-name')
            names.append(name)
    return names


if __name__ == '__main__':
    html = get_html(first_url)
    gb_cards = get_gb_urls(html)
    early_race = gb_cards[0]
    early_html = get_html(early_race)
    early_bets = get_bet_table(early_html)
    for runner in early_bets:
        available_odds = runner.find_all('td')
        for odd in available_odds:
            if 'bg-yellow' in odd['class']:
                print(odd)
