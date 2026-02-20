from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_video_data(link):
    api_url = "https://www.tikwm.com/api/"
    params = {'url': link}
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        if data.get('code') == 0:
            # Mengambil link video tanpa watermark
            return data['data']['play']
        return None
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    error = None
    if request.method == 'POST':
        input_link = request.form.get('url')
        video_url = get_video_data(input_link)
        if not video_url:
            error = "Gagal mengambil video. Pastikan link valid."
    return render_template('index.html', video_url=video_url, error=error)

# Penting untuk Vercel
app.debug = True
