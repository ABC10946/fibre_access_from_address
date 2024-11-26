from flask import Flask, request, jsonify, send_from_directory
from selenium import webdriver
from auto_address import autoAddress
from auto_flets import autoFlets
import urllib

app = Flask(__name__)
app.json.ensure_ascii = False


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/search', methods=['POST'])
def search():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "address parameter is required"}), 400

    chrome_options = webdriver.ChromeOptions()

    try:
        # addressはURLエンコードされている日本語なのでデコードする
        
        print(address)

        address = urllib.parse.unquote(address)
        driver = webdriver.Remote(
            command_executor='http://selenium.k8s.local/wd/hub',
            options=chrome_options
        )

        zipCode1, zipCode2, chome, banti, go = autoAddress(driver, address)

        chome = chome.translate(str.maketrans('0123456789', '０１２３４５６７８９'))
        chome = chome + "丁目"

        driver = webdriver.Remote(
            command_executor='http://selenium.k8s.local/wd/hub',
            options=chrome_options
        )

        fibreType = autoFlets(driver, zipCode1, zipCode2, chome, banti, go, True, "１０１号")

        return jsonify({"fibreType": fibreType})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)