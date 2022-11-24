import random
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def init_browser() -> WebDriver:
    # Chrome Driverにセットするオプションの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # ヘッドレスモードを有効にする。
    options.add_argument('--no-sandbox') # sandboxモードを解除する。この記述がないとエラーになってしまう。 
    options.add_argument('--disable-dev-shm-usage') # /dev/shmパーティションの使用を禁止し、パーティションが小さすぎることによる、クラッシュを回避する。
    options.add_argument('--disable-gpu')
    user_agent = [
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36']
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    options.add_argument('--user-agent=' + UA)
    # Webドライバーをセット
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    return driver
