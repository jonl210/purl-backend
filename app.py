from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/preview")
def preview():
    link = request.args.get("link")
    r = requests.get(link)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    # page title
    # soup.title.string
    print(soup.title.string)
    return "", 200