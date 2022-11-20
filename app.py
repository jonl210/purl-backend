from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route("/preview")
def preview():
    json = request.get_json(force=True)

    if not json: return
    if 'url' not in json: return

    try: link = requests.get(json['url'])
    except: return

    soup = BeautifulSoup(link.text, "html.parser")
    if 'youtube' in json['url'].replace('.', '')[:20]:
        return __process_youtube_link(soup), 200
    elif 'google' in json['url'][:20]:
        return __process_google_link(soup), 200
    elif 'spotify' in json['url'][:20]:
        return __process_spotify_link(soup), 200
    else:
        return {
            'title': soup.title.string if soup.title else '',
            'image': 'image',
            'icon': __get_favicon(soup)
        }, 200


## Iterates through all 'link' elements with hrefs and returns the url ending in '.ico'
def __get_favicon(soup):
    for link in soup.find_all('link'):
        if 'rel' in link.attrs and 'icon' in link.attrs['rel']:
            if link.attrs['href'][-3:].lower() == 'ico':
                return link.attrs['href']


###### Google ######
def __process_google_link(soup):
    return {
        'title': soup.title.string,
        'image': 'https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png',
        'icon': 'https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png'
    }

###### Youtube ######
def __process_youtube_link(soup):
    result = {
        'title': soup.title.string,
        'image': __get_youtube_thumbnail(soup),
        'icon': __get_favicon(soup)
    }
    return result

def __get_youtube_thumbnail(soup):
    result = []
    for link in soup.find_all('link'):
        if 'rel' in link.attrs and 'image_src' in link.attrs['rel']:
            result = link.attrs['href']
    return result


##### Spotify #####
def __process_spotify_link(soup):
    # Find spotify album meta
    image=None
    for meta in soup.find_all('meta'):
        if 'property' in meta.attrs and meta.attrs['property'].lower()=='og:image':
            image=meta.attrs['content']
    result = {
        'title': soup.title.string,
        'image': image,
        'icon': __get_favicon(soup)
    }
    return result