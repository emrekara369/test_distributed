from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Firefox için seçenekler
options = Options()
options.headless = True  # Firefox'u headless modda çalıştır

# Webdriver ile Firefox'u başlat
driver = webdriver.Firefox(options=options)
driver.get("https://www.google.com")
print(driver.title)
driver.quit()
