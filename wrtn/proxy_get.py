from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import json

class ProxyManager:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--remote-debugging-port=9515")
        self.service = Service('./chromedriver/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def extract_proxy_info(self, row):
        try:
            proxy_address = row.find_element(By.CSS_SELECTOR, 'font.spy14').text
            proxy_type = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
            proxy_Anonymity = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            proxy_Country = row.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text
            proxy_hostname = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
            return {
                'Index': len(self.proxy_list) + 1,
                'Proxy address:port': proxy_address,
                'Proxy type': proxy_type,
                'Anonymity*': proxy_Anonymity,
                'Country (city)': proxy_Country,
                'Hostname/ORG': proxy_hostname
            }
        except:
            print(f"프록시 서버 정보 추출 중 오류 발생: {row}")
            return None

    def get_proxy_list(self):
        self.driver.get('https://spys.one/en/free-proxy-list/')
        wait = WebDriverWait(self.driver, 100)
        self.proxy_list = []
        for row in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.spy1x'))):
            proxy_info = self.extract_proxy_info(row)
            if proxy_info:
                self.proxy_list.append(proxy_info)
        for row in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.spy1xx'))):
            proxy_info = self.extract_proxy_info(row)
            if proxy_info:
                self.proxy_list.append(proxy_info)
        return self.proxy_list

    def save_proxy_list(self, file_name='wrtn\proxy_list.json'):
        proxy_list = self.get_proxy_list()
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(proxy_list, f, ensure_ascii=False, indent=4)
        print(f"프록시 서버 정보가 {file_name}에 저장되었습니다.")

if __name__ == "__main__":
    proxy_manager = ProxyManager()
    proxy_manager.save_proxy_list()
