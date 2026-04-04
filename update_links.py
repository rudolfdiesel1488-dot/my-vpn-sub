import requests
import base64
import socket
from urllib.parse import urlparse

# Твои источники
SOURCES = {
    "pc_configs.txt": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt"],
    "mobile_configs.txt": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt"]
}

def is_server_alive(vless_url):
    """Проверяет, открыт ли порт сервера"""
    try:
        # Убираем префикс vless:// и парсим адрес
        parsed = urlparse(vless_url.replace("vless://", "http://"))
        host = parsed.hostname
        port = parsed.port
        
        # Пытаемся подключиться к порту (таймаут 2 секунды)
        with socket.create_connection((host, port), timeout=2):
            return True
    except:
        return False

def fetch_and_save():
    for filename, urls in SOURCES.items():
        all_lines = []
        for url in urls:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    # Разделяем на строки и фильтруем только vless://
                    raw_links = [l.strip() for l in r.text.split('\n') if l.startswith('vless://')]
                    
                    print(f"Проверяю {len(raw_links)} серверов для {filename}...")
                    
                    for link in raw_links:
                        if is_server_alive(link):
                            all_lines.append(link)
                        else:
                            print(f"--- СЕРВЕР МЕРТВ (пропускаю): {link[:30]}...")
            except:
                print(f"Ошибка при загрузке {url}")
        
        if not all_lines:
            print(f"ВНИМАНИЕ: Все сервера для {filename} недоступны!")
            continue

        # Кодируем выжившие серверы
        final_text = "\n".join(all_lines)
        b64_content = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
        
        with open(filename, "w") as f:
            f.write(b64_content)
        print(f"Файл {filename} обновлен. Живых серверов: {len(all_lines)}")

if __name__ == "__main__":
    fetch_and_save()
