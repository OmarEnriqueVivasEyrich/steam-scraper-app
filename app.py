from flask import Flask, render_template, Response
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def generar_urls():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")
    browser = Chrome(service=service, options=options)

    URLs = []

    try:
        browser.get('https://store.steampowered.com/?l=spanish')
        yield "Conectado a Steam...\n"
        time.sleep(2)

        browser.find_element(By.XPATH, "//div[@class='tab_content' and text()='Lo más vendido']").click()
        time.sleep(2)

        browser.find_element(By.XPATH, "//span[text()='Lo más vendido']").click()
        time.sleep(2)

        browser.find_element(By.ID, "sort_by_trigger").click()
        time.sleep(1)
        browser.find_element(By.ID, "Reviews_DESC").click()
        time.sleep(2)

        cantidad_de_juegos = 10
        for i in range(cantidad_de_juegos):
            juegos = browser.find_elements(By.CLASS_NAME, 'search_result_row.ds_collapse_flag')
            if i >= len(juegos):
                break
            juego = juegos[i]
            url = juego.get_attribute('href')
            URLs.append(url)
            yield f"URL extraída ({i+1}): {url}\n"
            time.sleep(1)

    except Exception as e:
        yield f"Error: {e}\n"

    finally:
        browser.quit()
        yield "Proceso completado.\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    return Response(generar_urls(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
