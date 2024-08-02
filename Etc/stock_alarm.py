import yfinance as yf
import time
from win10toast import ToastNotifier
import ctypes

class StockAlert:
    def __init__(self, alert_price: float):
        """
        주식 알림 클래스 초기화
        :param alert_price: 알림을 보낼 가격
        """
        self.ticker = "NVDA"
        self.alert_price = alert_price
        self.notifier = ToastNotifier()

    def get_current_price(self) -> float:
        """
        현재 주식 가격을 가져오는 메소드
        :return: 현재 주식 가격
        """
        stock_data = yf.Ticker(self.ticker)
        current_price = stock_data.history(period="1d")['Close'].iloc[-1]
        return current_price

    def send_notification(self, current_price: float):
        """
        가격 도달 시 알림을 보내는 메소드
        :param current_price: 현재 주식 가격
        """
        # 알림을 중요 알림으로 설정
        ctypes.windll.user32.MessageBoxW(0, f"{self.ticker} 주식 가격이 {current_price} 달러에 도달했습니다!", "주식 알림", 0x40 | 0x1)

        # 추가로 토스트 알림 표시
        self.notifier.show_toast(
            "주식 알림",
            f"{self.ticker} 주식 가격이 {current_price} 달러에 도달했습니다!",
            duration=10  # 알림이 10초 동안 표시됨
        )

    def start_monitoring(self):
        """
        주식 가격을 모니터링하는 메소드
        """
        while True:
            current_price = self.get_current_price()

            if current_price <= self.alert_price:
                self.send_notification(current_price)
                break

if __name__ == "__main__":
    alert_price = 100.0
    stock_alert = StockAlert(alert_price)
    stock_alert.start_monitoring()
