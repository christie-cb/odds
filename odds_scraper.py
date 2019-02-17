import requests
import bs4
import time

first_url = 'https://easyodds.com/horse-racing#'

def get_html(url):
    results = requests.get(url)
    html = bs4.BeautifulSoup(results.text, "html.parser")
    return html

def get_gb_urls(html):
    matches = html.find('div', class_="racecard")
    matches_info = matches.find_all('a')
    urls = []
    for match in matches_info:
        url = match.get('href')
        urls.append(url)
    unique_urls = list(dict.fromkeys(urls))
    return unique_urls 

def get_bet_table(racecard_html):
    table = racecard_html.find('div', class_="table-container")
    rows = table.find_all('tr', class_="selection-row-non-exchange")
    return rows

def get_runners(rows):
    runners = []
    for row in rows:
        runner_name = row.get('data-selection-name')
        best_price_subrow = row.find('td', class_="bg-yellow") 
        if best_price_subrow is not None:  # its only None when NR
            best_price = best_price_subrow.get('data-decimal')
            runners.append({
                'best_price': best_price,
                'runner_name': runner_name
            })
    return runners


if __name__ == '__main__':
    start = time.time()
    html = get_html(first_url)
    gb_cards = get_gb_urls(html)
    all_runners = []
    for race in gb_cards:
        race_html = get_html(race)
        rows = get_bet_table(race_html)
        runners = get_runners(rows)
        all_runners.append(runners)
    print(all_runners)
    print(time.time() - start)
