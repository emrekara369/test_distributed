import base64
import json
import sys
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from xvfbwrapper import Xvfb


def send_req_with_selenium(query, start_date=None, end_date=None):
    """
    Sends a search request to Google using Selenium to bypass bot detection.
    
    Args:
        query (str): The search query.
        start_date (str, optional): The start date for filtering search results. Defaults to None.
        end_date (str, optional): The end date for filtering search results. Defaults to None.
    
    Returns:
        requests.Response: The response object containing the search results.
    """
    results = []
    with Xvfb(width=1920, height=1080, colordepth=24):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        try:
            driver = webdriver.Chrome(options=options)

            driver.get("https://www.google.com/")
            time.sleep(2)

            try:
                driver.find_elements(By.TAG_NAME,"button")[4].click()
                time.sleep(1)
            except BaseException as ex:
                error_msg = ''.join(traceback.format_exception(type(ex), value=ex, tb=ex.__traceback__))
                print(error_msg)

            search_bar = driver.find_element(By.TAG_NAME,"textarea")
            search_bar.send_keys(query)
            search_bar.submit()
            time.sleep(4)
            if driver.find_element(By.ID,"topstuff").size["height"] == 0:
                search_result_div = driver.find_element(By.XPATH,'//div[@id="search"]')
                results.extend([_.get_attribute("href") for _ in search_result_div.find_elements(By.TAG_NAME,"a")])
                try:
                    page_number = len(driver.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"td"))-2
                except:
                    page_number = 1
                for page in range(1,page_number):
                    driver.get(driver.current_url+"&start="+str(page*10))
                    time.sleep(2)
                    search_result_div = driver.find_element(By.XPATH,'//div[@id="search"]')
                    results.extend([_.get_attribute("href") for _ in search_result_div.find_elements(By.TAG_NAME,"a")])
        except BaseException as ex:
            error_msg = ''.join(traceback.format_exception(type(ex), value=ex, tb=ex.__traceback__))
            print(error_msg)
            driver.quit()
        return results

def search(queries, start_date=None, end_date=None):
    """
    Search for URLs related to a given query.

    Args:
        query (str): The search query.
        start_date (str, optional): The start date for filtering results. Defaults to None.
        end_date (str, optional): The end date for filtering results. Defaults to None.

    Returns:
        list: A list of URLs related to the search query.
    """
    results = []
    for query in queries:
        results.extend(send_req_with_selenium(query, start_date, end_date))
        time.sleep(5)
    results = list(set(results))
    with open("/home/ubuntu/results.txt","w") as f:
        f.write("\n".join(results))

search(json.loads(base64.b64decode(sys.argv[-1])))
