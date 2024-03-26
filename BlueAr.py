import tkinter as tk
from tkinter import font
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading
import sys
import time 
import psutil

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

        self.button_2 = tk.Button(self.root, text="종료", command=self.a.stop_script)
        self.button_2.configure(bg=self.start_label_style['bg_2'], fg=self.start_label_style['fg'], font=self.start_label_style['font'])
        self.button_2.pack(fill=tk.BOTH, expand=True)

        self.root.mainloop()

    def start_script(self):
        if self.a.check_driver_status():
            print("창이 이미 열려 있습니다.")
        else:
            threading.Thread(target=self.a.run_script).start()

class Auto:
    def __init__(self) -> None:
        self.running = False
        self.driver = None
    
    def check_driver_status(self):
        try:
            self.driver.current_url
            return True
        except:
            self.driver = None
            return False
        
    def get_memory_usage(self):
        """
        Get the total memory usage by all processes with the given name
        """
        total_memory_usage = 0
        for proc in psutil.process_iter(['chrome.exe', 'memory_info']):
            if proc.info['chrome.exe']:
                total_memory_usage += proc.info['memory_info'].rss
        self.memory = total_memory_usage / (1024 * 1024) # Convert bytes to MB

    def run_script(self):
        self.running = True
        options = Options()
        options.add_argument("--remote-debugging-port=9515")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://www.ediya.com/contents/event_bluearchive.html') # 이 부분을 수정했습니다.
        try:
            while self.running:
                WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                alert = Alert(self.driver)
                alert.accept()
                self.driver.refresh()
                # Start a new thread to get memory usage
                memory_thread = threading.Thread(target=self.get_memory_usage, args=())
                memory_thread.start()
                memory_thread.join()  # Wait for the thread to finish

                # Check if memory usage exceeds 500 MB
                if self.memory > 500:
                    raise MemoryError('Memory usage exceeded 500 MB')
                elif not None:
                    print(self.memory)

        except MemoryError as e:
            print(f"{e} - Restarting the script...")
            self.stop_script()
            self.run_script()

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.stop_script()

    def stop_script(self):
        self.running = False
        if self.driver:
            self.driver.quit()
        else:
            pass

if __name__ == "__main__":
    TK()
    sys.exit()