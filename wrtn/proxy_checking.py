import requests
import json

# JSON 데이터 로드
with open('wrtn\proxy_list.json', 'r') as file:
    proxy_data = json.load(file)

# Google 주소 테스트
google_url = 'https://www.google.com'

# 프록시 타입별로 체크
proxy_types = ['HTTP', 'HTTP (Miktotik)', 'SOCKS5', 'HTTP (Squid)', 'HTTPS (Squid)', 'HTTPS (Miktotik)']

for proxy_type in proxy_types:
    print(f"Checking {proxy_type} proxies:")
    for proxy in proxy_data:
        if proxy['Proxy type'] == proxy_type:
            proxy_address = proxy['Proxy address:port']
            # 프록시 유형에 따라 프록시 설정 생성
            if proxy_type == 'HTTP (Miktotik)' or 'HTTP (Squid)' or 'HTTP':
                proxies = {
                    'http': f'http://{proxy_address}',
                    'https': f'http://{proxy_address}'
                }
            elif proxy_type == 'HTTPS (Miktotik)' or 'HTTPS (Squid)' or 'HTTPS':
                proxies = {
                    'http': f'https://{proxy_address}',
                    'https': f'https://{proxy_address}'
                }
            elif proxy_type == 'SOCKS5':
                proxies = {
                    'http': f'socks5://{proxy_address}',
                    'https': f'socks5://{proxy_address}'
                }
            else:
                continue  # 지원되지 않는 프록시 유형 건너뛰기

            try:
                # Google 주소 테스트
                response = requests.get(google_url, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    print(f"Proxy {proxy['Index']} ({proxy_address}) is working!✅")
                else:
                    print(f"Proxy {proxy['Index']} ({proxy_address}) is not working.❌")
            except:
                print(f"Proxy {proxy['Index']} ({proxy_address}) is not working.❌")
