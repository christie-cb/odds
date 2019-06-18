import odds_compare

def test_end_to_end():
    market = [{'best_price': '3.50', 'runner_name': 'Hold The Note'},
              {'best_price': '5.0', 'runner_name': 'Breaking Waves'}] 
    preds = '''13 0 Huntingdon 
    name: {}, pred-odds: {}, mkt-odds, edge
    Hold The Note 3.66634469749 3.59625077463 -0.0191182031806
    Breaking Waves 4.0214420245 4.13685045133 0.0286982694571'''
    preds_dict = odds_compare.parse_preds(preds)
    dicts = odds_compare.join_runners(market, preds_dict)
    bets = odds_compare.find_bets(dicts)
    assert '13 0 Huntingdon' in bets[0]['race']
    assert 'Breaking Waves' in bets[0]['name']
    assert 'ev' in bets[0].keys()

# fns: parse_preds, join_runners, find_bets, get_ev

def test_parse_preds():
    preds = '''13 0 Huntingdon 
    name: {}, pred-odds: {}, mkt-odds, edge
    Hold The Note 3.66634469749 3.59625077463 -0.0191182031806
    Breaking Waves 4.0214420245 4.13685045133 0.0286982694571'''
    preds_dict = odds_compare.parse_preds(preds)
    assert '13 0 Huntingdon' in preds_dict['race']
    assert type(preds_dict['runners']) == list
    assert preds_dict['runners'][0]['name'] == 'Breaking Waves'
    for runner in preds_dict['runners']:
        assert runner['ev'] >= 0

def test_join_runners():
    preds_dict = {'race': '13 0 Huntingdon', 
                  'runners': [{'name': 'Breaking Waves',
                              'pred': '4.0'}]}
    market = [[{'best_price': '0', 'runner_name': 'irrelevant_market'}, {'best_price': '3.50', 'runner_name': 'Hold The Note'},
              {'best_price': '5.0', 'runner_name': 'Breaking Waves'}]]
    dicts = odds_compare.join_runners(preds_dict, market)
    assert len(dicts) == 1  # i.e. irrelevant market not included
    assert dicts[0]['race'] == '13 0 Huntingdon'
    assert len(dicts[0]['runners']) == 2
    assert 'best_price' in dicts[0]['runners'][0]
    assert 'pred' in dicts[0]['runners'][0]

def test_find_bets():
    dicts = [
        {'race': '13 0 Huntingdon', 'runners': [
            {'name': 'Breaking Waves', 'pred': '4.0', 'best_price': '5.0'},
            {'name': 'Hold The Note', 'pred': '10.0', 'best_price': '5.0'}]}]
    bets = odds_compare.find_bets(dicts)
    runners = bets[0]['runners']
    for bet in runners:
        assert bet['name'] != 'Hold The Note'

def test_get_ev():
    ev = odds_compare.get_ev(2.0, 128 / 100 + 1.)
    assert ev == 0.1
