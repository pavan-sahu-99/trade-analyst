import pandas as pd
import json
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os


def get_sector_data(sector_name):
    try:
        # Load F&O symbols
        fo_df = pd.read_csv(r"C:\Users\user\OneDrive\Desktop\Trade_Analyst\data\f&o data.csv")
        fo_symbols = set(fo_df['Symbol'].str.upper().str.strip())

        # Setup headless browser
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Get cookies from homepage
        driver.get("https://www.nseindia.com")
        time.sleep(3)

        # Encode and fetch sector data
        encoded_index = urllib.parse.quote(sector_name)
        url = f"https://www.nseindia.com/api/equity-stockIndices?index={encoded_index}"
        driver.get(url)
        time.sleep(2)

        text = driver.find_element("tag name", "pre").text
        response = json.loads(text)
        stock_data = response.get("data", [])

        driver.quit()

        if stock_data:
            df = pd.DataFrame(stock_data)
            df = df[df['symbol'].str.upper().isin(fo_symbols)]  # Filter F&O only
            df = df[["symbol", "lastPrice", "pChange", "totalTradedVolume", "totalTradedValue"]]
            df.columns = ["Symbol", "Last Price", "% Change", "Volume", "Total Traded Value"]
            return df
        else:
            return pd.DataFrame()

    except Exception as e:
        print(f"Error fetching sector data for {sector_name}: {e}")
        return pd.DataFrame()

#data = get_sector_data("NIFTY AUTO")
#print(data)
