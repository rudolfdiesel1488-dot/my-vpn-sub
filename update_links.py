import requests
import base64
import time
from urllib.parse import urlparse

# Источники
SOURCES = {
    "pc_configs.txt": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt"],
    "mobile_configs.txt": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt"]
}

def check_via_check_host(host, port):
    """Проверка доступности порта через Москву (Check-Host API)"""
    try:
        # 1. Создаем запрос на проверку из Москвы (node=ru1)
        api_url = f"https://check-host.net/check-tcp?host={host}:{port}&node=ru1.check-host.net&max_nodes=1"
        headers = {'Accept': 'application/json'}
        r = requests.get(api_url, headers=headers)
        if r.status_code != 200: return True # Если API упал, лучше оставить сервер
        
        request_id = r.json().get('request_id')
        
        # 2. Ждем 3-5 секунд, пока Москва пропингует сервер
        time.sleep(4)
        
        # 3. Получаем результат
        result_url = f"https://check-host.net/check-result/{request_id}"
        res = requests.get(result_url, headers=headers)
        
        # Парсим ответ от московской ноды
        data = res.json().get('ru1.check-host.net')
        if data and data[0]:
            # Если в ответе есть время отклика (int/float), значит порт открыт
            return data[0].get('time') is not None
        return False
    except Exception as e:
        print(f"Ошибка API для {host}: {e}")
        return True # В случае ошибки API не удаляем сервер на всякий случай

def fetch_and_save():
    for filename, urls in SOURCES.items():
        valid_links = []
        for url in urls:
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    links = [l.strip() for l in res.text.split('\n') if l.startswith('vless://')]
                    print(f"\n--- Проверка {len(links)} серверов для {filename} через МОСКВУ ---")
                    
                    for link in links:
                        try:
                            # Извлекаем хост и порт
                            addr = link.split('@')[1].split('?')[0]
                            host, port = addr.split(':')
                            
                            print(f"Чекаю {host}...", end=" ", flush=True)
                            if check_via_check_host(host, port):
                                valid_links.append(link)
                                print("✅ ЖИВОЙ")
                            else:
                                print("❌ БАН (РКН)")
                            
                            # Небольшая пауза, чтобы API не забанил нас за спам
                            time.sleep(2)
                        except:
                            continue
            except:
                print(f"Ошибка загрузки {url}")

        if valid_links:
            final_content = "\n".join(valid_links)
            b64_data = base64.b64encode(final_content.encode('utf-8')).decode('utf-8')
            with open(filename, "w") as f:
                f.write(b64_data)
            print(f"\nГотово! {filename}: {len(valid_links)} серверов прошли цензуру.")

if __name__ == "__main__":
    fetch_and_save()
