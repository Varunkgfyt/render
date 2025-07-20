from flask import Flask, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time, os

app = Flask(__name__)

@app.route('/screenshot')
def screenshot():
    url = request.args.get('url')
    if not url:
        return {"error": "Missing URL"}, 400

    filename = f"shot_{int(time.time())}.png"
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,1024")
    # Optional: add Indian proxy later:
    # options.add_argument("--proxy-server=http://YOUR_INDIA_PROXY:PORT")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(2)  # Let page load fully
    driver.save_screenshot(filename)
    driver.quit()

    sent = send_file(filename, mimetype='image/png')
    os.remove(filename)
    return sent

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
