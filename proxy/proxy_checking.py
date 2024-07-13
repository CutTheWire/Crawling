import requests
import json

class ProxyChecker:
    def __init__(self, file_path, google_url):
        self.file_path = file_path
        self.google_url = google_url
        self.proxy_data = self.load_proxy_data()
        self.proxy_types = ['HTTP', 'HTTP (Miktotik)', 'SOCKS5', 'HTTP (Squid)', 'HTTPS (Squid)', 'HTTPS (Miktotik)']

    def load_proxy_data(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def get_proxies(self, proxy_type, proxy_address):
        if proxy_type in ['HTTP', 'HTTP (Miktotik)', 'HTTP (Squid)']:
            return {
                'http': f'http://{proxy_address}',
                'https': f'http://{proxy_address}'
            }
        elif proxy_type in ['HTTPS', 'HTTPS (Miktotik)', 'HTTPS (Squid)']:
            return {
                'http': f'http://{proxy_address}',
                'https': f'https://{proxy_address}'
            }
        elif proxy_type == 'SOCKS5':
            return {
                'http': f'socks5://{proxy_address}',
                'https': f'socks5://{proxy_address}'
            }
        else:
            return None

    def check_proxy(self, proxy):
        proxy_address = proxy['Proxy address:port']
        proxies = self.get_proxies(proxy['Proxy type'], proxy_address)
        
        try:
            response = requests.get(self.google_url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                print(f"Proxy {proxy['Index']} ({proxy_address}) is working!✅")
            else:
                print(f"Proxy {proxy['Index']} ({proxy_address}) is not working.❌")
        except:
            print(f"Proxy {proxy['Index']} ({proxy_address}) is not working.❌")

    def check_proxies_by_type(self, proxy_type):
        print(f"Checking {proxy_type} proxies:")
        proxies = [p for p in self.proxy_data if p['Proxy type'] == proxy_type]
        for proxy in proxies:
            self.check_proxy(proxy)

    def run(self):
            for proxy_type in self.proxy_types:
                self.check_proxies_by_type(proxy_type)


if __name__ == "__main__":
    proxy_checker = ProxyChecker('proxy/proxy_list.json', 'https://www.google.com')
    proxy_checker.run()
