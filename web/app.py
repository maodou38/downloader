from flask import Flask, request, jsonify
from flask import render_template
from WebParser import Parser
import json
from m3u8 import Downloader
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

pool = ThreadPoolExecutor(2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    data = json.loads(request.data)
    url = data['url']
    web = data['web']
    name = data['name']
    path = data['path']
    m3u8url = Parser(url, web).parseMayiyingshi()
    downloader = Downloader(m3u8url, path, name)
    ret, pbar = downloader.run()
    pool.submit(downloader.mergeFile, ret, pbar)
    return jsonify("success")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
