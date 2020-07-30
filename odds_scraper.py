import requests
import bs4
import time


def get_html(url):
    results = requests.get(url)
    html = bs4.BeautifulSoup(results.text, "html.parser")
    return html

def get_gb_urls(html):
    contents = html.find('div', class_="row row-no horse-racing-holder")
    matches = contents.find_all('id="horse-racing-menu-link"')
    urls = []
    for match in matches:
        url = match.get('href')
        urls.append(url)
    unique_urls = list(dict.fromkeys(urls))
    return unique_urls 

def get_bet_table(racecard_html):
    table = racecard_html.find('div', class_="table-container")
    rows = table.find_all('tr', class_="selection-row-non-exchange")
    return rows

def replace_non_runners(subrow):
    if subrow is None:
        subrow = '<td data-decimal="0">'
        replacement = bs4.BeautifulSoup(subrow, "html.parser")
    else:
        replacement = subrow
    return replacement

def get_runners(rows):
    runners = []
    for row in rows:
        runner_name = row.get('data-selection-name')
        best_price_subrow = row.find('td', class_="bg-yellow")
        best_price_subrow = replace_non_runners(best_price_subrow)
        best_price = best_price_subrow.get('data-decimal')
        runners.append({
            'best_price': best_price,
            'runner_name': runner_name
        })
    return runners


if __name__ == '__main__':
    
    first_url = 'https://easyodds.com/horse-racing#'
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
