# headless google-chromeの例


import os
import shutil
from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

HOME = os.environ['HOME']
target_url = 'https://www.pixiv.net/artworks/75863105'
options = Options()
options.add_argument("--headless")
options.add_argument('window-size=2024x2024')
options.add_argument(f'user-data-dir=work_dir')
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


driver = webdriver.Chrome(executable_path=shutil.which('chromedriver'), options=options)
driver.get(target_url)
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="presentation"]')))
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@target='_blank']")))
time.sleep(5.0)
html = driver.page_source
soup = BeautifulSoup(html, 'html5lib')
driver.save_screenshot("screenshot.png")

for idx, img in enumerate(soup.find_all('img')):
    src = img.get('src')
    headers = {'referer':target_url,
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    r = requests.get(src, headers=headers)
    print(src, r.status_code)
    binary = r.content
    with open(f'{idx:04d}.jpeg', 'wb') as fp:
        fp.write(binary)