from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder="../templates")

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
    except:
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    if not url or "tiktok.com" not in url:
        return jsonify({"error": "Link tidak valid"}), 400

    result = get_tiktok_data(url)
    if not result:
        return jsonify({"error": "Gagal mengambil video"}), 400

    return jsonify(result)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

def handler(request, context):
    return app(request.environ, lambda status, headers: None)
