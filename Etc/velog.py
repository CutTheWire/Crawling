import tkinter as tk
from tkinter import font
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import sys
import time

class TK:
    def __init__(self) -> None:
        self.a = Auto()
        self.root = tk.Tk()
        self.root.title("Website Auto")
        self.root.geometry("300x100")
        self.root.resizable(False, False)

        self.start_label_style = {
            'bg_1': '#35B558',
            'bg_2': '#B53538',
            'fg': 'white',
            'font': font.Font(family="Helvetica", size=15)
        }

        self.button_1 = tk.Button(self.root, text="시작", command=self.start_script)
        self.button_1.configure(bg=self.start_label_style['bg_1'], fg=self.start_label_style['fg'], font=self.start_label_style['font'])
        self.button_1.pack(fill=tk.BOTH, expand=True)

        self.button_2 = tk.Button(self.root, text="종료", command=self.stop_script)
        self.button_2.configure(bg=self.start_label_style['bg_2'], fg=self.start_label_style['fg'], font=self.start_label_style['font'])
        self.button_2.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    def start_script(self):
        threading.Thread(target=self.a.run_script).start()

    def stop_script(self):
        self.a.stop_script()

class Auto:
    def __init__(self) -> None:
        self.running = False
        self.driver = None
    
    def run_script(self):
        self.running = True
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        while self.running:
            self.driver.get('https://velog.io/@saeon/OpenCV-Seed-Counter') # 조회수를 올리고 싶은 웹사이트
            time.sleep(1)  # 웹사이트가 로드되는 시간 동안 대기, 실제로는 사이트 로딩 시간에 따라 조정해야 할 수 있음 
        if self.driver:
            self.driver.quit()
        else:
            pass

if __name__ == "__main__":
    TK()
    sys.exit()
