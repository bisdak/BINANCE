import time
import json
import re
import os
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from utils import selenium_utils as sel

FILENAME = 'binance.csv'


class Binance:
    def __init__(self, url, change):
        self.change = change
        self.url = url
        self.main()
    
    def scrape(self):
        coin_dict = {}
        now = datetime.now().strftime('%H:%M:%S')
        try:
            response = requests.get(self.url)
        except Exception:
            return

        data = json.loads(response.text)
        results = data['data']

        for result in results:
            skip = False
            for word in ['UPUSDT','DOWNUSDT']:
                if word in result['s']:
                    skip = True
                    break

            if result['q'] != 'USDT' or skip:
                continue
            
            coin_dict[f'{result["s"]}'] = result['c'] 

        df = pd.DataFrame(coin_dict.items(), columns=['Pair', f'{now}'])
        return df
    
    def append(self):
        df = self.scrape()
        if df.empty:
            return

        if not os.path.isfile(FILENAME):
            df.to_csv(FILENAME, index=False)
            return pd.DataFrame()
            
        b_df = pd.read_csv(FILENAME)
        merge = pd.merge(b_df, df, on="Pair", how='left')

        return merge

    def calc_save(self):
        df = self.append()

        if df.empty:
            return

        columns = len(df.columns)
    
        if columns >= 3:
            first_col = df[df.columns[-2 if columns == 3 else -3]].astype(float)
            last_col = df[df.columns[-1]].astype(float)

            df[f'change_{columns}'] = (last_col - first_col) / (0.01 * first_col)
            df.round(decimals=2)

        header = df.columns[-1]
        coins = df[df[header]>self.change]['Pair']
        if not coins.empty:
            print(coins)
        #max = df[header].max()

        #if max >= self.change:
           # print(f'{header} -> {max}')
            #os.system('mpg123 success.mp3')
        
        df.to_csv(FILENAME, index=False)


    def main(self):
        self.calc_save()

if __name__  == '__main__':
    url = 'https://api.yshyqxx.com/exchange-api/v2/public/asset-service/product/get-products?includeEtf=true'
    change = 1
    Binance(url, change)
