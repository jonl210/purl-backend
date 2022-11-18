from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/preview")
def preview():
    json=request.get_json(force=True)

    if not json: return 
    if 'url' not in json: return 

    try: link=requests.get(json['url'])
    except: return

    soup = BeautifulSoup(link.text, "html.parser")
    if 'youtube' in json['url'].replace('.','')[:20]:
        return __process_youtube_link(soup), 200
    elif 'google' in json['url'][:20]:
        return __process_google_link(soup), 200
    else:
        return {
            'title': soup.title.string if soup.title else '',
            'image':'image',
            'icon':__get_favicon(soup)
        }, 200


def __process_youtube_link(soup):
    result = {
        'title':soup.title.string,
        'image':__get_youtube_thumbnail(soup),
        'icon':__get_favicon(soup)
    }
    return result


def __get_favicon(soup):
    return [link.attrs['href'] for link in soup.find_all('link') if 'rel' in link.attrs and 'icon' in link.attrs['rel']]

def __process_google_link(soup):
    return {
        'title':soup.title.string,
        'image':'https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png',
        'icon':'https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png'
    }


def __get_youtube_thumbnail(soup):
    for link in soup.find_all('link'):
        if 'rel' in link.attrs and 'image_src' in link.attrs['rel']:
            result = link.attrs['href']
    return result