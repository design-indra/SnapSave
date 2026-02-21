from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_insta_data(link):
    # 1. Bersihkan link dari parameter tambahan agar API bekerja maksimal
    # Menghapus bagian setelah tanda tanya (?)
    clean_link = link.split("?")[0]
    
    # 2. URL API BhawaniGarg yang kamu minta
    api_url = f"https://api.bhawanigarg.com/social/instagram/?url={clean_link}"
    
    try:
        # Menambahkan timeout agar website tidak loading selamanya jika API lambat
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        # Berdasarkan struktur API BhawaniGarg:
        # Jika sukses, data biasanya ada di dalam data['data']
        if data.get('success') and data.get('data'):
            item = data['data']
            return {
                'video': item.get('video_url'),
                'cover': item.get('thumbnail')
            }
        return None
    except Exception as e:
        print(f"Error pada API: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        input_link = request.form.get('url')
        
        if not input_link or "instagram.com" not in input_link:
            error = "Mohon masukkan tautan Instagram yang valid."
        else:
            result = get_insta_data(input_link)
            if not result:
                error = "Gagal mengambil data. Pastikan video bukan dari akun privat atau coba lagi nanti."
            
    return render_template('index.html', result=result, error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)
