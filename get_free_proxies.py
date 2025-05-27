import requests
from bs4 import BeautifulSoup

def fetch_proxies():
    urls = [
        "https://free-proxy-list.net/",
        "https://www.us-proxy.org/"
    ]
    proxies = []
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            status_code = response.status_code
            html_content = response.text
        
            filename = url.replace("https://", "").replace("/", "_") + '.html'
            # with open(filename, 'w', encoding='utf-8') as file:
            #     file.write(html_content)
                
            print(f"Successfully fetched proxies from {url} with status code {status_code}")
            
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', {'class': 'table table-striped table-bordered'})
            if not table:
                print("Proxy table not found.")
                continue 
            
            rows = table.tbody.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxy = f"{ip}:{port}"
                proxies.append(proxy)

        except requests.RequestException as e:
            print(f"Error fetching proxies from {url}: {e}")
    return proxies
proxy_list = fetch_proxies()
print(f"Total proxies fetched: {len(proxy_list)}")
with open('free_proxies.csv', 'w', encoding='utf-8') as file:
    for proxy in proxy_list:
        file.write(proxy + '\n')
def test_proxies(proxies):
    test_url = "http://httpbin.org/ip"
    for proxy in proxies:
        try:
            response = requests.get(test_url, proxies={"https": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                print(f"Proxy {proxy} is working.")
            else:
                print(f"Proxy {proxy} failed with status code {response.status_code}.")
        except requests.RequestException as e:
            print(f"Proxy {proxy} failed: {e}")
test_proxies(proxy_list)