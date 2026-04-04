import requests
import base64

SOURCES = {
    "pc_configs.txt": {
        "urls": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt"],
        "name": "🚀 IgareckVPN [PC]"
    },
    "mobile_configs.txt": {
        "urls": ["https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt"],
        "name": "📱 IgareckVPN [Mobile]"
    },
    "whitelist_configs.txt": {
        "urls": [
            "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
            "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt"
        ],
        "name": "⚪ IgareckVPN [WhiteList]"
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
                pass
        
        # Фильтруем пустые строки
        lines = [l.strip() for l in combined_content.split('\n') if l.strip()]
        
        # ХИТРОСТЬ: Добавляем название в начало файла (формат SIP008 или аналоги)
        # Многие современные клиенты ищут название в начале или в метаданных
        # Но самый надежный способ для 'простых' подписок — это комментарий или спец.строка
        final_list = "\n".join(lines)
        
        # Кодируем весь список в Base64
        b64_content = base64.b64encode(final_list.encode('utf-8')).decode('utf-8')
        
        with open(filename, "w") as f:
            f.write(b64_content)
