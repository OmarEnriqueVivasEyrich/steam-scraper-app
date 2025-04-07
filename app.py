from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    urls = []

    if request.method == "POST":
        try:
            # Hacemos una petición al sitio de Steam
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            url = "https://store.steampowered.com/search/?filter=topsellers&os=win&supportedlang=spanish"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extraemos los links de los juegos
            resultados = soup.find_all("a", class_="search_result_row")
            for i, a_tag in enumerate(resultados[:10]):  # Solo 10 juegos
                href = a_tag.get("href")
                if href:
                    urls.append(href)

        except Exception as e:
            return f"<h1>Error al hacer scraping</h1><p>{str(e)}</p>"

    return render_template("index.html", urls=urls)

if __name__ == "__main__":
    app.run(debug=True)
