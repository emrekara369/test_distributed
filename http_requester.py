import base64

import requests
import urllib3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def make_request(url,type):
    try:
        if type == "http":
            response = requests.get(url,verify=False,timeout=5).text
            response = base64.b64encode(response.encode("ascii")).decode("ascii")
            return response
        elif type == "selenium":
            options = Options()
            options.add_argument("--headless")
            browser = webdriver.Firefox(options=options)
            browser.get(url)
            response =  browser.page_source
            response = base64.b64encode(response.encode("ascii")).decode("ascii")
            return response
    except:
        return None
