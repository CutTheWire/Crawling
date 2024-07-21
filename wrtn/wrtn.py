import csv
import gc
import io
import os
import sys
import time
import tracemalloc

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 터미널에서 한글 깨짐 방지
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# .env 파일 로드 여기에 실제 ./wrtn/.env경로를 env를 넣으세요
load_dotenv()

WRTN_ID = os.getenv('wrtn_email')
WRTN_PW = os.getenv('wrtn_password')
WRTN_URL = os.getenv('wrtn_url')

class Auto:
    def __init__(self) -> None:
        '''
        ### options.add_argument("--remote-debugging-port=9515")
        - Chrome browser를 원격 디버깅 모드, 디버깅을 위한 포트를 지정하는 옵션
            
        ### Service('./chromedriver/chromedriver.exe')
        - ChromeDriver 실행 파일의 경로
        '''
        self.running = False
        self.driver = None

        options = Options()
        options.add_argument("--remote-debugging-port=9515")
        service = Service('./chromedriver/chromedriver.exe')

        self.wrtn_url = WRTN_URL
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(self.wrtn_url)

        # 로그 파일 헤더 작성
        log_dir = "wrtn"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.log_file_path = os.path.join(log_dir, "memory_log.csv")

        # 파일이 없을 때만 헤더를 추가
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w", newline='', encoding="utf-8") as log_file:
                writer = csv.writer(log_file)
                writer.writerow([
                    "timestamp",
                    "current_memory_usage_bytes",
                    "current_memory_usage_formatted",
                    "peak_memory_usage_bytes",
                    "peak_memory_usage_formatted"
                ])

    def format_memory_size(self, size_in_bytes):
        if size_in_bytes < 1024:
            return f"{size_in_bytes} bytes"
        elif size_in_bytes < 1024**2:
            return f"{size_in_bytes / 1024:.2f} KB"
        else:
            return f"{size_in_bytes / 1024**2:.2f} MB"

    def log_memory_usage(self) -> None:
        '''현재 메모리 사용량 로그 기록'''
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        current_formatted = self.format_memory_size(current)
        peak_formatted = self.format_memory_size(peak)

        # 로그 기록
        log_entry = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "current_memory_usage_bytes": f"{current}bytes",
            "current_memory_usage_formatted": current_formatted,
            "peak_memory_usage_bytes": f"{peak}bytes",
            "peak_memory_usage_formatted": peak_formatted
        }

        # CSV 파일에 기록
        with open(self.log_file_path, "a", newline='', encoding="utf-8") as log_file:  # 'a' 모드로 변경
            writer = csv.writer(log_file)
            writer.writerow([
                log_entry["timestamp"],
                log_entry["current_memory_usage_bytes"],
                log_entry["current_memory_usage_formatted"],
                log_entry["peak_memory_usage_bytes"],
                log_entry["peak_memory_usage_formatted"]
            ])

    def get_first_button(self) -> WebDriverWait:
        '''대화 답변 1번째 클릭 함수'''
        return WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@class='css-x7f1x9'])[1]"))
        )

    def check_driver_status(self) -> bool:
        '''While 상태'''
        try:
            self.driver.current_url
            return True
        except:
            self.driver = None
            return False

    def login(self) -> None:
        '''Wrtn 로그인'''
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

    def perform_deletion(self) -> None:
        '''대화 목록 삭제'''
        try:
            edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "css-15wn0bx"))
            )
            edit_button.click()

            parent_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-1hw5egt"))
            )
            confirm_button = parent_element.find_element(By.CLASS_NAME, "css-14nl16v")
            confirm_button.click()

            parent_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-3cmpyx"))
            )
            delete_button = parent_element.find_element(By.CLASS_NAME, "css-9xfakb")
            delete_button.click()
            second_delete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-opiluf"))
            )
            second_delete_button.click()

        except TimeoutException:
            print("삭제 요소를 찾는 데 시간이 너무 오래 걸립니다.")
        except Exception as e:
            print(f"Error during deletion: {str(e)}")

    def run_script(self) -> None:
        self.running = True
        count = 0
        
        try:
            self.first_button = self.get_first_button()
            self.first_button.click()
            time.sleep(1)
            self.login()
            time.sleep(2)
            self.driver.get(self.wrtn_url)
            
            while self.running:
                tracemalloc.start()
                time.sleep(1)
                self.first_button = self.get_first_button()
                self.first_button.click()
                time.sleep(1)
                self.driver.get(self.wrtn_url)
                count += 1
                
                if count == 10:
                    self.perform_deletion()
                    time.sleep(1)
                    count = 0
                    self.log_memory_usage()
                    time.sleep(1)

        except TimeoutException:
            print("요소를 찾는 데 시간이 너무 오래 걸립니다.")
        except Exception as e:
            print(f"Error during automation: {str(e)}")


if __name__ == "__main__":
    auto = Auto()
    auto.run_script()
    gc.collect()
    sys.exit()
