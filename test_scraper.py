import odds_scraper
import bs4

end_to_end_html = '''<html>
    <body>
    <div class="table-container">
    <table id="not the one">
    <table id="betsTable">
    <tbody>
    <tr class="selection-row-non-exchange tr-odds" data-selection-name="HORSE-NAME">
    <td class="number-table odds bg-yellow" data-decimal="3.25">
    <td class="number-table odds" data-decimal="3.0">
    '''

def test_end_to_end():
    url = 'https://easyodds.com/horse-racing/'
    html = odds_scraper.get_html(url)
    e_html = bs4.BeautifulSoup(end_to_end_html, "html.parser")
    table = odds_scraper.get_bet_table(e_html)
    runner = odds_scraper.get_runners(table)[0]
    assert '3.0' not in runner['best_price']
    assert '3.25' in runner['best_price']
    assert 'HORSE-NAME' in runner['runner_name']
    assert type(html) == bs4.BeautifulSoup

def test_get_gb_urls():
    html = '''<div class="racecard" data-group="united-kingdom">
    <table class="matches-list">
    <thead>
    <tr class="racecard-row"><a href="URL">
    '''
    html = bs4.BeautifulSoup(html, "html.parser")
    urls = odds_scraper.get_gb_urls(html)
    assert 'URL' in str(urls[0])

def test_get_html():
    url = 'https://easyodds.com/horse-racing/'
    html = odds_scraper.get_html(url)
    assert type(html) == odds_scraper.bs4.BeautifulSoup

def test_get_table():
    html = '''<html>
    <body>
    <div class="table-container">
    <tbody><INFO>
    <tr class="selection-row-non-exchange tr-odds">
    <td class="bg-yellow">'''
    html = odds_scraper.bs4.BeautifulSoup(html, "html.parser")
    table = odds_scraper.get_bet_table(html)
    assert 'tr-odds' in str(table)
    assert 'bg-yellow' in str(table)

def test_get_runners():
    html = '''
    <tbody>
    <tr class="tr-odds" data-selection-name="HORSE-NAME">
    <td data-fraction="9/4" class="bg-yellow">
    '''
    html = bs4.BeautifulSoup(html, "html.parser")
    html = [html]
    runners = odds_scraper.get_runners(html)
    assert 'best_price' in runners[0]
    assert 'runner_name' in runners[0] 
