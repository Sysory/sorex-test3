import asyncio
import logging
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from currency import Currency

class CryptoAPI:
    JSON_PATH = "data.json"
    def __init__(self, apiKey : str):
        self.__apiKey = apiKey

    async def loadActualData(self, currs : list[Currency]) -> dict[str : str]:
        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

        currsIDs = []
        for curr in currs:
            currsIDs.append(curr.id.upper())

        parameters = {
            'symbol':f'{','.join(currsIDs)}',
            'convert':'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'Accept-Encoding': 'deflate, gzip',
            'X-CMC_PRO_API_KEY': self.apiKey,
        }

        session = Session()
        session.headers.update(headers)

        try:
            await asyncio.sleep(0)
            response = session.get(url, params=parameters)
            await asyncio.sleep(0)
            data = json.loads(response.text)

            # print(data)
            prices = {}
            for curr in currsIDs:
                prices[curr] = data["data"][curr]["quote"]["USD"]["price"]
            
            return prices
            
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            logging.warning(f"An error occurs while fetching currencies data for {currsIDs}")

# async def main():
#     c1 = Currency("BTC", 1, 2)
#     c2 = Currency("ETH", 1, 2)
#     print(await CryptoAPI.loadActualData([c1, c2]))

# if __name__ == "__main__":
#     asyncio.run(main())
