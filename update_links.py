import requests
import base64

# Конфиги: что откуда берем и куда сохраняем
SOURCES = {
    "pc_configs.txt": [
        "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt"
    ],
    "mobile_configs.txt": [
        "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt"
    ],
    "whitelist_configs.txt": [
        "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
        "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt"
    ]
}

def fetch_and_save():
    for filename, urls in SOURCES.items():
        combined_content = ""
        for url in urls:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    combined_content += r.text + "\n"
            except:
                print(f"Ошибка при загрузке {url}")
        
        # Чистим пустые строки
        lines = [line.strip() for line in combined_content.split('\n') if line.strip()]
        final_text = "\n".join(lines)
        
        # Кодируем в Base64 (стандарт для v2ray/v2raytun)
        b64_content = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
        
        with open(filename, "w") as f:
            f.write(b64_content)
        print(f"Файл {filename} обновлен")

if __name__ == "__main__":
    fetch_and_save()
