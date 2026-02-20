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
            return {
                'video': data['data']['play'],
                'cover': data['data']['cover']
            }
        return None
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        input_link = request.form.get('url')
        result = get_video_data(input_link)
        if not result:
            error = "Gagal mengambil video. Pastikan link valid."
    return render_template('index.html', result=result, error=error)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')
