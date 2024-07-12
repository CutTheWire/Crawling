from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import os
import sys
import time

# .env 파일 로드 여기에 실제 ./wrtn/.env경로를 env를 넣으세요
load_dotenv()

WRTN_ID = os.getenv('wrtn_email')
WRTN_PW = os.getenv('wrtn_password')


class Auto:
    def __init__(self) -> None:
        self.running = False
        self.driver = None

        options = Options()
        options.add_argument("--remote-debugging-port=9515")
        service = Service('./chromedriver/chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get('https://wrtn.ai/character/u/66900ad96b6ae50a0463e19f?type=c')

    def get_first_button(self):
        button_text = "*천천히 복도에서 마주보고 걸어오며* 렐리, 어딜 그렇게 급하게 뛰어가?"
        return WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[p[text()='{button_text}']]"))
        )

    def check_driver_status(self):
        try:
            self.driver.current_url
            return True
        except:
            self.driver = None
            return False

    def login_naver(self):
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-1utg1yz'))
            )
            login_button.click()
            time.sleep(1)

            id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            id_input.send_keys(WRTN_ID)

            pw_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            pw_input.send_keys(WRTN_PW)

            login_submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'css-wk1976'))
            )
            login_submit_button.click()

        except TimeoutException:
            print("로그인 요소를 찾는 데 시간이 너무 오래 걸립니다.")
        except Exception as e:
            print(f"Error during login: {str(e)}")

    def run_script(self):
        self.running = True
        try:
            self.first_button = self.get_first_button()
            self.first_button.click()
            time.sleep(1)

            self.login_naver()
            time.sleep(1)
            self.driver.get('https://wrtn.ai/character/u/66900ad96b6ae50a0463e19f?type=c')

            while self.running:
                time.sleep(2)
                self.first_button = self.get_first_button()
                self.first_button.click()
                time.sleep(2)
                self.driver.get('https://wrtn.ai/character/u/66900ad96b6ae50a0463e19f?type=c')

        except TimeoutException:
            print("요소를 찾는 데 시간이 너무 오래 걸립니다.")
        except Exception as e:
            print(f"Error during automation: {str(e)}")

if __name__ == "__main__":
    auto = Auto()
    auto.run_script()
    sys.exit()
