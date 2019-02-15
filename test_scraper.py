import odds_scraper
import bs4

end_to_end_html = '''<html>
    <body>
    <div class="table-container">
    <table id="not the one">
    <table id="betsTable">
    <tbody>
    <tr class="HORSE-NAME">
    <td class="number-table odds bg-yellow" data-fraction="9/4">
    <td class="number-table odds" data-fraction="2/1">
    '''

def test_end_to_end():
    url = 'https://easyodds.com/horse-racing/'
    html = odds_scraper.get_html(url)
    e_html = bs4.BeautifulSoup(end_to_end_html, "html.parser")
    table = odds_scraper.get_bet_table(e_html)
    runner = odds_scraper.get_runner_info(table)
    assert 2 / 1 not in str(runner)
    assert 9 / 4 in str(runner)
    assert 'horse-name' in str(runner)
    assert type(html) == bs4.BeautifulSoup

def test_get_html():
    url = 'https://easyodds.com/horse-racing/'
    html = odds_scraper.get_html(url)
    assert type(html) == odds_scraper.bs4.BeautifulSoup

def test_get_table():
    html = '''<html>
    <body>
    <div class="table-container">
    <table id="not the one">
    <table id="betsTable">
    <tbody><INFO>'''
    html = odds_scraper.bs4.BeautifulSoup(html, "html.parser")
    table = odds_scraper.get_bet_table(html)
    assert 'info' in str(table)

def test_get_runners():
    html = '''
    <tbody>
    <tr class="tr-odds" data-selection-name="HORSE-NAME">
    <td data-fraction="9/4" class="bg-yellow">
    '''
    html = bs4.BeautifulSoup(html, "html.parser")
    runners = odds_scraper.get_runners(html)
    assert 'tr' in str(runners[0])

def test_get_runner_info():
    html = '''<tr data-selection-name="Gowanbuster"
    <td class="number-table odds bg-yellow" data-fraction="9/4">
    <td class="number-table odds" data-fraction="2/1">'''
    html = odds_scraper.bs4.BeautifulSoup(html, "html.parser")
    runner = odds_scraper.get_runner_info(html)
    assert 'gowanbuster' in str(runner)
    assert '9/4' in str(runner) and '2/1' not in str(runner)
