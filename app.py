from flask import Flask, render_template, request, redirect
import requests
import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.tiktok.com/',
    'Accept': 'application/json'
}

def get_tiktok_via_tikwm(clean_link):
    """API 1: tikwm.com"""
    try:
        r = requests.post(
            "https://www.tikwm.com/api/",
            data={'url': clean_link, 'hd': 1},
            headers=HEADERS,
            timeout=15
        )
        data = r.json()
        if data.get('code') == 0 and data.get('data'):
            item = data['data']
            return {
                'video': item.get('hdplay') or item.get('play'),
                'cover': item.get('cover'),
                'title': item.get('title', 'TikTok Video')
            }
    except Exception as e:
        print(f"tikwm error: {e}")
    return None

def get_tiktok_via_musicaldown(clean_link):
    """API 2: musicaldown.com"""
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        r = session.post(
            "https://musicaldown.com/api/download",
            data={'url': clean_link},
            timeout=15
        )
        data = r.json()
        links = data.get('links', [])
        video_url = None
        cover_url = None
        for item in links:
            if item.get('type') == 'mp4' and 'watermark' not in item.get('name', '').lower():
                video_url = item.get('link')
                break
        if not video_url and links:
            video_url = links[0].get('link')
        if video_url:
            return {
                'video': video_url,
                'cover': data.get('thumbnail', ''),
                'title': data.get('title', 'TikTok Video')
            }
    except Exception as e:
        print(f"musicaldown error: {e}")
    return None

def get_tiktok_via_snaptik(clean_link):
    """API 3: snaptik.app (unofficial)"""
    try:
        r = requests.get(
            "https://api.snaptik.app/tiktok",
            params={'url': clean_link},
            headers=HEADERS,
            timeout=15
        )
        data = r.json()
        if data.get('data'):
            item = data['data']
            return {
                'video': item.get('videoUrl') or item.get('nowm'),
                'cover': item.get('cover', ''),
                'title': item.get('title', 'TikTok Video')
            }
    except Exception as e:
        print(f"snaptik error: {e}")
    return None

def get_tiktok_data(link):
    clean_link = link.split("?")[0]
    
    # Coba API satu per satu
    result = get_tiktok_via_tikwm(clean_link)
    if result and result.get('video'):
        print("Berhasil via tikwm")
        return result
    
    result = get_tiktok_via_snaptik(clean_link)
    if result and result.get('video'):
        print("Berhasil via snaptik")
        return result

    result = get_tiktok_via_musicaldown(clean_link)
    if result and result.get('video'):
        print("Berhasil via musicaldown")
        return result

    print("Semua API gagal")
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
                error = "Gagal mengambil video. Coba beberapa saat lagi."
    return render_template('index.html', result=result, error=error)

# --- ROUTE DOWNLOAD: Redirect langsung ke URL video ---
@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "URL tidak valid", 400
    return redirect(video_url)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)
