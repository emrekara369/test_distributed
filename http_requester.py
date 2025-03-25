import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def fetch_url(url):
    """Selenium ile URL'yi açıp sayfa içeriğini döndürür."""
    options = Options()
    options.add_argument("--headless")  # Görüntüsüz modda çalıştır
    options.add_argument("--no-sandbox")  # Sandbox problemi yaşamamak için
    options.add_argument("--disable-dev-shm-usage")  # Dev.shm kullanımını devre dışı bırak

    # ChromeDriver'ı uygun yol ile başlatıyoruz
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()

    return page_source

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python http_requester.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    print(f"İstek gönderiliyor: {target_url}")

    try:
        page_content = fetch_url(target_url)
        result = {"url": target_url, "content": page_content[:500]}  # İlk 500 karakteri al
    except Exception as e:
        result = {"url": target_url, "error": str(e)}

    print(json.dumps(result))
