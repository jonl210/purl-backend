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
    elif 'facebook' in json['url'][:20]:
        return __process_facebook_link(soup), 200
    elif 'spotify' in json['url'][:20]:
        return __process_spotify_link(soup), 200
    else:
        return __process_default_link(soup), 200

###### Default #####
def __process_default_link(soup):
    return {
        'title': soup.title.string if soup.title else '',
        'image': 'image',
        'icon': __get_favicon(soup)
    }

###### Google ######
def __process_google_link(soup):
    return {
        'title': soup.title.string,
        'image': 'https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png',
        'icon': 'https://www.google.com/images/branding/googleg/1x/googleg_standard_color_128dp.png'
    }

###### Youtube ######
def __process_youtube_link(soup):
    image=__get_og_image(soup)
    return {
        'title': soup.title.string,
        'image': image if image else 'default',
        'icon': __get_favicon(soup)
    }

###### Facebook ######
def __process_facebook_link(soup):
    image=__get_og_image(soup)
    return {
        'title': soup.title.string,
        'image': image if image else 'default',
        'icon': __get_favicon(soup)
    }

##### Spotify #####
def __process_spotify_link(soup):
    # Find spotify album meta
    image=__get_og_image(soup)
    return {
        'title': soup.title.string,
        'image': image if image else 'default',
        'icon': __get_favicon(soup)
    }


##### Private Helper Functions #####

## Iterates through all 'link' elements with hrefs and returns the url ending in '.ico'
def __get_favicon(soup):
    for link in soup.find_all('link'):
        if 'rel' in link.attrs and 'icon' in link.attrs['rel']:
            if link.attrs['href'][-3:].lower() == 'ico':
                return link.attrs['href']

## Gets 'meta' element with 'og:image' property returns 'content' property 
def __get_og_image(soup):
    for meta in soup.find_all('meta'):
        if 'property' in meta.attrs and meta.attrs['property'].lower()=='og:image':
            return meta.attrs['content']
