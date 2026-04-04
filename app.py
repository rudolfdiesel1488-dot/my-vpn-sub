from flask import Flask, Response
import os

app = Flask(__name__)

@app.route('/pc')
def pc():
    with open('pc_configs.txt', 'r') as f:
        content = f.read()
    # Вот тут магия! Мы заставляем приложение видеть красивое имя
    return Response(content, mimetype='text/plain', headers={
        'Subscription-Userinfo': 'name=🚀 IgareckVPN [PC]',
        'Content-Disposition': 'inline; filename=pc_configs.txt'
    })

@app.route('/mobile')
def mobile():
    with list_open('mobile_configs.txt', 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/plain', headers={
        'Subscription-Userinfo': 'name=📱 IgareckVPN [Mobile]'
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
