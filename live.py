import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_proxy(ip, port):
    try:
        proxies = {
            'http': f'http://{ip}:{port}',
            'https': f'http://{ip}:{port}'
        }
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def main():
    with open('ip.txt', 'r') as file:
        proxies = file.readlines()

    live_proxies = []
    dead_proxies = []

    total_proxies = len(proxies)
    print(f"Verificare a {total_proxies} proxy-uri...")

    with ThreadPoolExecutor(max_workers=200) as executor:
        futures = []
        for proxy in proxies:
            ip, port = proxy.strip().split(':')
            futures.append(executor.submit(check_proxy, ip, port))

        completed = 0
        for future, proxy in zip(as_completed(futures), proxies):
            ip_port = proxy.strip()
            if future.result():
                live_proxies.append(ip_port)
            else:
                dead_proxies.append(ip_port)

            completed += 1
           
            print(".", end="", flush=True)
         
            if completed % 50 == 0:
                print(f" {completed}/{total_proxies}")

    print(f"\nCheck. {len(live_proxies)} proxy LIVE and {len(dead_proxies)} proxy DEAD.")

    with open('OK.txt', 'w') as ok_file:
        for proxy in live_proxies:
            ok_file.write(proxy + '\n')

    with open('d.txt', 'w') as dead_file:
        for proxy in dead_proxies:
            dead_file.write(proxy + '\n')

if __name__ == "__main__":
    main()
