import requests
import base64

# Конфиги: что берем и как называем в приложении
SOURCES = {
    "pc_configs.txt": {
        "urls": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt"],
        "name": "🚀 IgareckVPN [PC]",
        "desc": "Жми 'Тест скорости' -> Выбирай где есть ПИНГ"
    },
    "mobile_configs.txt": {
        "urls": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt"],
        "name": "📱 IgareckVPN [Mobile]",
        "desc": "Если не пашет - обнови подписку!"
    },
    "whitelist_configs.txt": {
        "urls": [
            "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
            "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt"
        ],
        "name": "⚪ IgareckVPN [WhiteList]",
        "desc": "Только для избранных сайтов"
    }
}

def fetch_and_save():
    for filename, info in SOURCES.items():
        combined_content = ""
        for url in info["urls"]:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    combined_content += r.text + "\n"
            except:
                print(f"Ошибка при загрузке {url}")
        
        lines = [line.strip() for line in combined_content.split('\n') if line.strip()]
        final_text = "\n".join(lines)
        
        # Кодируем в Base64
        b64_content = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
        
        with open(filename, "w") as f:
            f.write(b64_content)
        
        print(f"Файл {filename} обновлен")

if __name__ == "__main__":
    fetch_and_save()
