# analyzer.py

def extract_user_profile(bar_data):
    spirits = []
    proofs = []
    prices = []

    for bottle in bar_data:
        product = bottle.get('product', {})
        if 'spirit' in product:
            spirits.append(product['spirit'])
        if 'proof' in product and isinstance(product['proof'], (int, float)):
            proofs.append(product['proof'])
        if 'price' in bottle and isinstance(bottle['price'], (int, float)):
            prices.append(bottle['price'])

    profile = {
        'favorite_spirit': most_common(spirits),
        'average_proof': average(proofs),
        'target_price': average(prices)
    }
    return profile

def most_common(lst):
    return max(set(lst), key=lst.count) if lst else None

def average(lst):
    return sum(lst) / len(lst) if lst else None
