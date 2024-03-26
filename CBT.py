import tkinter as tk
from tkinter import font
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import threading
import sys

class TK:
    def __init__(self) -> None:
        self.a = Auto()
        self.root = tk.Tk()
        self.root.title("WebSite Auto")
        self.root.geometry("300x100")
        self.root.resizable(False, False)

        self.start_label_style = {
            'bg_1': '#35B558',
            'bg_2': '#B53538',
            'fg': 'white',
            'font': font.Font(family="Helvetica", size=15)
        }

       
        self.button_1 = tk.Button(self.root, text="한문제씩 풀기", command=lambda: self.start_script("s_view.php", "문제풀기"))
        self.button_1.configure(bg=self.start_label_style['bg_1'], fg=self.start_label_style['fg'], font=self.start_label_style['font'])
        self.button_1.pack(fill=tk.BOTH, expand=True)

        self.button_2 = tk.Button(self.root, text="문제와 답", command=lambda: self.start_script("onlyview.php", "문제보기"))
        self.button_2.configure(bg=self.start_label_style['bg_2'], fg=self.start_label_style['fg'], font=self.start_label_style['font'])
        self.button_2.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    def start_script(self, php_text ,button_text):
        # 창이 이미 열려있는지 확인
        if self.a.check_driver_status():
            print("창이 이미 열려 있습니다.")
        else:
            # 창이 열려있지 않다면 스크립트를 실행
            threading.Thread(target=self.a.run_script(php=php_text, order=button_text)).start()


    def update_button_status(self):
        # 창 상태에 따라 버튼 활성화/비활성화
        if self.a.check_driver_status():
            self.button_1.configure(state='disabled')
            self.button_2.configure(state='disabled')
        else:
            self.button_1.configure(state='normal')
            self.button_2.configure(state='normal')

class Auto:
    def __init__(self) -> None:
        self.running = False
        self.driver = None
    
    def check_driver_status(self):
        try:
            # 브라우저 창이 열려있는지 확인
            self.driver.current_url
            return True
        except:
            # 브라우저 창이 닫혀있으면 WebDriver 객체를 None으로 설정
            self.driver = None
            return False
        
    def select(self, drop: str, option: str):
        try:
            # 드롭다운 메뉴가 로드되고 선택 가능할 때까지 기다림
            dropdown_menu = WebDriverWait(self.driver, 3000).until(
                EC.presence_of_element_located((By.NAME, f'{drop}'))
            )
            # 옵션 선택
            select = Select(dropdown_menu)
            select.select_by_visible_text(option)
            WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.NAME, f'{drop}'))
            )
            # 버튼이 로드되고 클릭 가능할 때까지 기다림
            submit_button = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))
            )
            # 버튼 클릭
            submit_button.click()
        except TimeoutException:
            print(f"Timeout while trying to select {option} from {drop}")
        except Exception as e:
            print(f"Error selecting {option} from {drop}: {str(e)}")

    def run_script(self, php: str, order: str):
        self.running = True
        options = Options()
        options.add_argument("--remote-debugging-port=9515")
        # Specify the path to chromedriver if it's not in your system PATH
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://www.comcbt.com/cbt/index2.php?hack_number')
        try:
            WebDriverWait(self.driver, 100).until(EC.alert_is_present())
            alert = Alert(self.driver)
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")
        except:
            print("WebDriver error")
        try:
            # More dynamic wait instead of sleep
            WebDriverWait(self.driver, 1500).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'form[action="{php}"] input[value="{order}"]'))).click()
                # Wait for the dropdown to be interactable
            WebDriverWait(self.driver, 1500).until(
                EC.element_to_be_clickable((By.NAME, 'imsidbname'))
            )
            # 드롭다운 메뉴가 로드되고 선택 가능할 때까지 기다림
            WebDriverWait(self.driver, 1500).until(
                EC.presence_of_element_located((By.NAME, 'imsidbname'))
            )
            self.select("imsidbname", "기사")
            self.select("dbname", "정보처리기사")

        except TimeoutException:
            print("요소를 찾는 데 시간이 너무 오래 걸립니다.")

if __name__ == "__main__":
    TK()
    sys.exit()
