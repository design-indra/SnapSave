export default async function handler(req, res) {
  const { url } = req.query;

  if (!url) {
    return res.status(400).json({ error: "Missing URL" });
  }

  try {
    const response = await fetch(
      `https://www.tikwm.com/api/web/info?url=${encodeURIComponent(url)}`,
      {
        method: "GET",
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
          "Accept": "application/json",
          "Referer": "https://www.tikwm.com/"
        }
      }
    );

    const text = await response.text();

    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Content-Type", "application/json");

    return res.status(200).send(text);

  } catch (error) {
    return res.status(500).json({ error: "API request failed", detail: error.message });
  }
}
