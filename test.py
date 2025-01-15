import requests

def get_token_accounts_by_owner(address):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://explorer.solana.com',
        'priority': 'u=1, i',
        'referer': 'https://explorer.solana.com/',
        'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'solana-client': 'js/1.0.0-maintenance',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    json_data = {
        'method': 'getTokenAccountsByOwner',
        'jsonrpc': '2.0',
        'params': [
            address,
            {
                'programId': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA',
            },
            {
                'encoding': 'jsonParsed',
                'commitment': 'processed',
            },
        ],
        'id': '0e918902-7c91-4d28-b7c7-bc78cc832b8c',
    }

    response = requests.post('https://explorer-api.mainnet-beta.solana.com/', headers=headers, json=json_data)
    if response.status_code == 200:
        json_data = response.json()
        result = json_data['result']
        value = result['value']
        for data in value:
            info = data['account']['data']['parsed']['info']
            if info['mint'] == 'sBkHx3cdCxENqq2CheAxDFpBeMY31dsaCUAfmdGpump':
                return info['tokenAmount']['uiAmount']

# Example usage:
address = '7pJSGeKasboboUa2LWyLqYXZax7RPwbBdnk2GUmXYbsz'
print(get_token_accounts_by_owner(address))
