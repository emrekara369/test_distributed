import json
import random
import sys
import time
from urllib.parse import unquote
import base64

import requests
from bs4 import BeautifulSoup

print("Received:", sys.argv[1])
def get_useragent():
    """
    Generates a random user agent string mimicking the format of various software versions.

    The user agent string is composed of:
    - Lynx version: Lynx/x.y.z where x is 2-3, y is 8-9, and z is 0-2
    - libwww version: libwww-FM/x.y where x is 2-3 and y is 13-15
    - SSL-MM version: SSL-MM/x.y where x is 1-2 and y is 3-5
    - OpenSSL version: OpenSSL/x.y.z where x is 1-3, y is 0-4, and z is 0-9

    Returns:
        str: A randomly generated user agent string.
    """
    lynx_version = f"Lynx/{random.randint(2, 3)}.{random.randint(8, 9)}.{random.randint(0, 2)}"
    libwww_version = f"libwww-FM/{random.randint(2, 3)}.{random.randint(13, 15)}"
    ssl_mm_version = f"SSL-MM/{random.randint(1, 2)}.{random.randint(3, 5)}"
    openssl_version = f"OpenSSL/{random.randint(1, 3)}.{random.randint(0, 4)}.{random.randint(0, 9)}"
    return f"{lynx_version} {libwww_version} {ssl_mm_version} {openssl_version}"

def send_req(query,start_date,end_date):
    url = "https://www.google.com/search"
    if start_date and end_date:
        url += f"?tbs=cdr:1,cd_min:{start_date},cd_max:{end_date}"
    elif start_date:
        url += f"?tbs=cdr:1,cd_min:{start_date}"
    elif end_date:
        url += f"?tbs=cdr:1,cd_max:{end_date}"
        
    resp = requests.get(
        url=url,
        headers={
            "User-Agent": get_useragent(),
            "Accept": "*/*"
        },
        params={
            "q": query,
            "num": 500,
            "hl": "en",
            "start": 0,
            "safe": "active",
            "gl": None
        },
        proxies=None,
        timeout=5,
        verify=None,
        cookies = {
            'CONSENT': 'PENDING+987', # Bypasses the consent page
            'SOCS': 'CAESHAgBEhIaAB',
        }
    )
    resp.raise_for_status()
    return resp

def fetch_urls(query, start_date=None, end_date=None):
    """
    Fetches URLs from Google search results for a given query.

    Args:
        query (str): The search query.
        start_date (str, optional): The start date for filtering search results. Defaults to None.
        end_date (str, optional): The end date for filtering search results. Defaults to None.

    Returns:
        list: A list of unique URLs fetched from the search results.
    """
    start = 0
    fetched_results = 0  # Keep track of the total fetched results
    fetched_links = set()  # to keep track of links that are already seen previously
    while fetched_results < 500:
        resp = send_req(query, start_date, end_date)
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", class_="ezO2md")
        new_results = 0  # Keep track of new results in this iteration

        for result in result_block:
            # Find the link tag within the result block
            link_tag = result.find("a", href=True)
            # Extract and decode the link URL
            link = unquote(link_tag["href"].split("&")[0].replace("/url?q=", "")) if link_tag else ""
            # Check if the link has already been fetched and if unique results are required
            if link in fetched_links or not link.startswith("http"):
                continue  # Skip this result if the link is not unique
            # Add the link to the set of fetched links
            fetched_links.add(link)
            fetched_results += 1
            # Increment the count of new results in this iteration
            new_results += 1
            if fetched_results >= 500:
                break  # Stop if we have fetched the desired number of results

        if new_results == 0:
            break  # Break the loop if no new results were found in this iteration

        start += 10  # Prepare for the next set of results
        time.sleep(2)
    return list(fetched_links)

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
        results.extend(fetch_urls(query, start_date, end_date))
        time.sleep(5)
    with open("/home/ubuntu/results.txt","w") as f:
        f.write("\n".join(results))

search(json.loads(base64.b64decode(sys.argv[-1])))
