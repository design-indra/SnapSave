from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_tiktok_data(link):
    # Membersihkan link dari parameter pelacakan (?is_from_webapp=1...)
    clean_link = link.split("?")[0]
    
    # Menggunakan API TikWM yang sangat stabil untuk TikTok
    api_url = "https://www.tikwm.com/api/web/info"
    
    try:
        # Melakukan request ke API TikWM
        response = requests.get(api_url, params={'url': clean_link}, timeout=15)
        data = response.json()
        
        # TikWM mengembalikan 'code': 0 jika berhasil
        if data.get('code') == 0 and data.get('data'):
            item = data['data']
            
            # Mengambil data video (Tanpa Watermark) dan Cover
            return {
                'video': item.get('play'),        # URL Video Tanpa Watermark
                'cover': item.get('cover'),       # Gambar Preview
                'title': item.get('title', 'TikTok Video') # Judul/Caption Video
            }
        return None
    except Exception as e:
        print(f"Error pada API TikTok: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        input_link = request.form.get('url')
        
        # Validasi link TikTok
        if not input_link or "tiktok.com" not in input_link:
            error = "Mohon masukkan tautan TikTok yang valid."
        else:
            result = get_tiktok_data(input_link)
            if not result:
                error = "Gagal mengambil video. Pastikan link benar dan video tidak dihapus."
            
    return render_template('index.html', result=result, error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)
