import requests

term = "Madonna"

res = requests.get(
    'https://itunes.apple.com/search', params={'term': term, 'limit': 5})


data = res.json()

for result in data['results']:
    print(result['trackName'])
    print(result['collectionName'])

data = {
    'username': 'chickenz',
    'tweets': [
        'hello!', 'goodbye!', 'bock bock!', {
            'id': 1,  'text': 'my first tweet!'}
    ]
}

requests.post('https://en27bnye2btkl.x.pipedream.net', json=data)
