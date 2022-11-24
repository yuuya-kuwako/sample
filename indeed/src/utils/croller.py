import datetime
import re
import logging
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from browser import init_browser
from model.OutputModel import ResultData

logger = logging.getLogger(__name__)

def get_url(position, location):
    """Generate url from position and location"""
    template = 'https://jp.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url

def get_detail_records(sub_driver:WebDriver, detail_urls:list):
    recruit_list = []
    for detail_url in detail_urls:
        sub_driver.get(detail_url)
        sleep(1)
        html = sub_driver.page_source.encode('utf-8')
        detail_soup = BeautifulSoup(html,'html.parser')
        try:
            # 会社名
            corporate_name = detail_soup.find_all('div','jobsearch-InlineCompanyRating-companyHeader')[1].text.replace(',','')
            # 採用媒体
            recruit_medium = 'indeed'
            # 取得日時
            exec_date =  datetime.datetime.now().strftime('%Y-%m-%d')
            # 募集職種
            elem_occupation = detail_soup.find('h1','jobsearch-JobInfoHeader-title')
            occupation = '' if not elem_occupation else elem_occupation.text.replace(',','')
            # 募集形態
            elem_recruit_form = detail_soup.find(id='salaryInfoAndJobType').find_all('span')
            recruit_form = ''
            if len(elem_recruit_form) > 1:
                recruit_form = elem_recruit_form[1].text.replace(',','')
            recruit_form = re.sub(r"[ -]", "", recruit_form)
            # 募集URL
            recruit_url = detail_url
            # 勤務地
            elem_working_location = detail_soup.find('div','jobsearch-JobInfoHeader-subtitle')
            working_location = '' if not elem_working_location else elem_working_location.contents[1].contents[0].text.replace(',','')
            # 募集タイトル
            recruit_title = occupation
            # 募集詳細
            elem_recruit_detail = detail_soup.find('div','jobsearch-JobComponent-description')
            recruit_detail = '' if not elem_recruit_detail else elem_recruit_detail.text.replace(',','')
            # 改行コード、空白が含まれているので削除する
            recruit_detail = "".join(recruit_detail.splitlines())
            recruit_detail = recruit_detail.strip()
            # 募集ターゲット
            recruit_target = str(recruit_detail)
            # 給与
            elem_salary = detail_soup.find(id='salaryInfoAndJobType').find_all('span')
            salary = '' if not elem_salary else elem_salary[0].text.replace(',','')
            # キーワード
            elem_category = detail_soup.find('span','jobsearch-CmiJobCategory-content')
            category = '' if not elem_category else '/' + elem_category.text.replace(',','')
            elem_tags = detail_soup.find('ul','jobsearch-JobTag')
            tag_name = ''
            if elem_tags:
                tag_name = '/'
                tags = elem_tags.contents
                for tag in tags:
                    tag_name = tag_name+tag.text.replace(',','') + '/'
            keyword = category + tag_name
        except AttributeError:
            continue
        except TimeoutException:
            logger.error("TimeoutExceptionが発生しました: for %s", detail_url)
            continue
        except Exception as e:
            logger.error("想定外の例外発生しました: %s", str(e))
            continue
        
        recruit_list.append(ResultData(corporate_name, recruit_medium, exec_date, occupation, recruit_form, recruit_url, working_location, recruit_title, recruit_detail, recruit_target, salary, keyword))
        sleep(1)
    
    return recruit_list

def get_records(driver:WebDriver, result_list:list, url:str):
    base_url = 'https://jp.indeed.com'
    while True:
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html,'html.parser')
        
        
        # メインページにある募集項目のURL一覧を取得
        cards = soup.find_all('div','job_seen_beacon')
        sleep(2)
        detail_urls = []
        for card in cards:
            detail_urls.append(base_url + card.h2.a.get('href'))
            
        sub_driver = init_browser()
        # データ取得
        result_list.extend(get_detail_records(sub_driver, detail_urls))
        sub_driver.quit()
        try:
            url = base_url + soup.find('a', {'aria-label': 'Next Page'}).get('href')
        except AttributeError:
            break
    return result_list
