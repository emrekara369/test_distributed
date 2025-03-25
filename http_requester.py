import argparse
import base64
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def fetch_url(url, request_mode, query=None):
    """
    Fetches the content of a web page.

    Args:
        url (str): The URL of the web page to fetch.
        request_mode (str): The request mode, either "dorker" or "normal".
        query (str, optional): The search query to be used in "dorker" mode.

    Returns:
        str: The page source of the fetched web page.
    """
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    if request_mode == "dorker":
        driver.get("https://google.com")
        search_bar = driver.find_element(By.CLASS_NAME, "textarea")
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)
    elif request_mode == "normal":
        driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-m", "--mode",choices=["normal", "dorker"],required=True,help="Define the request mode")
    parser.add_argument("-q", "--query",help="Define the query for dork request")
    parser.add_argument("-u", "--url",help="Define the request url")
    args = parser.parse_args()

    if args.mode == "normal":
        if args.query:
            parser.error("Query (-q) cannot be used in normal mode.")
        if not args.url:
            parser.error("URL (-u) is required in normal mode.")

    elif args.mode == "dorker":
        if not args.query:
            parser.error("Query (-q) is required in dorker mode.")
        if not args.url:
            parser.error("URL (-u) is required in dorker mode.")
    target_url = args.url
    request_mode = args.mode
    try:
        page_content = fetch_url(target_url,request_mode)
        result = {"url": target_url, "content": base64.b64encode(page_content.encode("ascii")).decode("ascii")}
    except Exception as e:
        result = {"url": target_url, "content": ""}
    print(json.dumps(result))