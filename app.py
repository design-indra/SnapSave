from flask import Flask, render_template, request
import requests
import os

# Pastikan Flask tahu lokasi folder templates
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

def get_tiktok_data(link):
    clean_link = link.split("?")[0]
    api_url = "https://www.tikwm.com/api/web/info"
    try:
        response = requests.get(api_url, params={'url': clean_link}, timeout=15)
        data = response.json()
        if data.get('code') == 0 and data.get('data'):
            item = data['data']
            return {
                'video': item.get('play'),
                'cover': item.get('cover'),
                'title': item.get('title', 'TikTok Video')
            }
        return None
    except Exception as e:
        print(f"Error TikTok: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        input_link = request.form.get('url')
        if not input_link or "tiktok.com" not in input_link:
            error = "Masukkan link TikTok yang valid!"
        else:
            result = get_tiktok_data(input_link)
            if not result:
                error = "Gagal mengambil video TikTok."
    return render_template('index.html', result=result, error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)
