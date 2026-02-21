from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder="../templates")


def get_tiktok_data(link):
    clean_link = link.split("?")[0]
    api_url = "https://www.tikwm.com/api/web/info"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": "https://www.tikwm.com/"
    }

    try:
        response = requests.get(
            api_url,
            params={"url": clean_link},
            headers=headers,
            timeout=15
        )

        print("STATUS CODE:", response.status_code)

        if response.status_code != 200:
            print("BAD STATUS:", response.text)
            return None

        data = response.json()
        print("API RESPONSE:", data)

        if data.get("code") == 0 and data.get("data"):
            item = data["data"]
            return {
                "video": item.get("play"),
                "cover": item.get("cover"),
                "title": item.get("title", "TikTok Video")
            }

        return None

    except Exception as e:
        print("ERROR API:", e)
        return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url or "tiktok.com" not in url:
            return jsonify({"error": "Link tidak valid"}), 400

        result = get_tiktok_data(url)

        if not result:
            return jsonify({"error": "Gagal mengambil video"}), 400

        return jsonify(result)

    except Exception as e:
        print("ERROR ROUTE:", e)
        return jsonify({"error": "Server error"}), 500


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")
