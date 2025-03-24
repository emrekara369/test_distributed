import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def http_requester():
    """Selenium kullanarak HTTP isteği yapar."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://example.com"  # Hedef URL
    driver.get(url)
    time.sleep(2)  # Sayfanın yüklenmesini bekle

    response_body = driver.page_source
    driver.quit()

    return response_body[:500]  # İlk 500 karakteri döndürelim

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Hata: Çalıştırılacak modül belirtilmedi.")
        sys.exit(1)

    module_name = sys.argv[1]

    if module_name == "http_requester":
        print(http_requester())
    else:
        print(f"Hata: {module_name} modülü tanımlı değil.")
