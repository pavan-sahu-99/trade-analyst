from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import json

def sectorials():
    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(options=options)

    # Step 1: Load NSE homepage to get cookies
    driver.get("https://www.nseindia.com")
    time.sleep(3)  # Let cookies load

    # Step 2: Hit actual API endpoint using Selenium cookies
    url = "https://www.nseindia.com/api/allIndices"
    driver.get(url)
    time.sleep(2)

    # Step 3: Parse JSON response from the page source
    text = driver.find_element("tag name", "pre").text
    data = json.loads(text).get("data", [])

    sector_keywords = [
        "NIFTY AUTO", "NIFTY BANK", "NIFTY FINANCIAL SERVICES", "NIFTY FMCG",
        "NIFTY IT", "NIFTY MEDIA", "NIFTY METAL", "NIFTY PHARMA", "NIFTY PSU BANK",
        "NIFTY PRIVATE BANK", "NIFTY REALTY", "NIFTY HEALTHCARE INDEX", "NIFTY OIL & GAS"
    ]

    sectoral_data = [index for index in data if index['index'] in sector_keywords]
    df = pd.DataFrame(sectoral_data)
    #print(df.columns)
    '''Index(['key', 'index', 'indexSymbol', 'last', 'variation', 'percentChange',
        'open', 'high', 'low', 'previousClose', 'yearHigh', 'yearLow',
        'indicativeClose', 'pe', 'pb', 'dy', 'declines', 'advances',
        'unchanged', 'perChange365d', 'date365dAgo', 'chart365dPath',
        'date30dAgo', 'perChange30d', 'chart30dPath', 'chartTodayPath',
        'previousDay', 'oneWeekAgo', 'oneMonthAgo', 'oneYearAgo'],
        dtype='object')'''
    filtered_df = df[["index" ,"previousClose", 'last',"percentChange"]].copy()
    filtered_df.columns = ["Index", "previousClose", "LTP","%Change"]
    #print(filtered_df.head(10))
    #filtered_df.to_excel(r"C:\Users\user\OneDrive\Desktop\Trade_Analyst\data\sectorial_indices_data.xlsx", index=False)

    driver.quit()
    return filtered_df
