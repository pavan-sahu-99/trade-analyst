from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import json

def get_oi_spurts():
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
    url = "https://www.nseindia.com/api/live-analysis-oi-spurts-underlyings"
    driver.get(url)
    time.sleep(2)

    # Step 3: Parse JSON response from the page source
    text = driver.find_element("tag name", "pre").text
    data = json.loads(text).get("data", [])
    df = pd.DataFrame(data)
    filtered_df = df[["symbol", "underlyingValue", "volume", "changeInOI", "avgInOI"]].copy()
    filtered_df.columns = ["symbol", "cmp", "volume", "changeInOI", "%changeInOI"]
    driver.quit()
    return filtered_df

#data = get_oi_spurts()
#print(data.head())
