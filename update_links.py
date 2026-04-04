import requests
import base64
import socket
from urllib.parse import urlparse

# Источники те же
SOURCES = {
    "pc_configs.txt": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt"],
    "mobile_configs.txt": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt"]
}

def check_via_rf(host, port):
    """
    Пытаемся проверить доступность порта. 
    В идеале тут можно добавить запрос к API чек-хоста, 
    но для начала сделаем усиленный сокет-чекинг.
    """
    try:
        # Устанавливаем очень короткий таймаут, чтобы не ждать вечно
        conf = socket.create_connection((host, port), timeout=3)
        conf.close()
        return True
    except:
        return False

def fetch_and_save():
    for filename, urls in SOURCES.items():
        valid_links = []
        for url in urls:
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    links = [l.strip() for l in res.text.split('\n') if l.startswith('vless://')]
                    
                    print(f"--- Проверка {len(links)} серверов для {filename} ---")
                    
                    for link in links:
                        # Парсим хост и порт из vless://
                        # Формат: vless://uuid@host:port?query
                        try:
                            parts = link.split('@')[1].split('?')[0]
                            host = parts.split(':')[0]
                            port = int(parts.split(':')[1])
                            
                            if check_via_rf(host, port):
                                valid_links.append(link)
                                print(f"[OK] {host}")
                            else:
                                print(f"[DEAD] {host} (недоступен)")
                        except:
                            continue
            except:
                print(f"Ошибка загрузки {url}")

        # Сохраняем только живых
        if valid_links:
            final_content = "\n".join(valid_links)
            b64_data = base64.b64encode(final_content.encode('utf-8')).decode('utf-8')
            with open(filename, "w") as f:
                f.write(b64_data)
            print(f"Итог {filename}: {len(valid_links)} живых.")

if __name__ == "__main__":
    fetch_and_save()
