import os
import datetime
import logging
import sys
sys.path.append('C:\\Users\\81901\\Desktop\\Project\\PeerLodge\\scraping_sample\\indeed\src\\utils')
sys.path.append('C:\\Users\\81901\\Desktop\\Project\\PeerLodge\\scraping_sample\\indeed\src\\model')
import utils.csv as csv_util
import utils.browser as browser
import utils.croller as croller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    
    # CSV作成
    str_today = datetime.date.today().strftime('%Y-%m-%d')
    temp_file_path = f'indeed_{str_today}.csv'
    csv_util.write_header(temp_file_path)
    
    # # 検索条件えお指定したurlを取得
    url = croller.get_url('エンジニア', '東京')
    
    # # seleniumのchromeブラウザを初期化
    driver = browser.init_browser()
    result_list = []
    result_list = croller.get_records(driver, result_list, url)

    csv_util.output_result(result_list, temp_file_path)
    driver.quit()