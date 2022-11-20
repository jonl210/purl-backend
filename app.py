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

    og_compatible_sites=['youtube', 'facebook', 'spotify']
    for site in og_compatible_sites:
        if site in json['url'].replace('.', '')[:20]:
            return __process_og_compatible_link(soup)

    if 'google' in json['url'][:20]:
        return __process_google_link(soup), 200
    else:
        return __process_default_link(soup), 200


###### og Compatible ######
def __process_og_compatible_link(soup):
    return {
        'title': __get_content_for_og('title', soup),
        'image': __get_content_for_og('image', soup),
        'icon': __get_favicon(soup)
    }

###### Default ######
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

###### Private Helper Functions ######

## Iterates through all 'link' elements with hrefs and returns the url ending in '.ico'
def __get_favicon(soup):
    for link in soup.find_all('link'):
        if 'rel' in link.attrs and 'icon' in link.attrs['rel']:
            if link.attrs['href'][-3:].lower() == 'ico':
                return link.attrs['href']

## Searches through 'meta' elements for property matching the og parameter, returns 'content'
def __get_content_for_og(og, soup):
    for meta in soup.find_all('meta'):
        if 'property' in meta.attrs and meta.attrs['property'].lower()==f'og:{og.lower()}':
            return meta.attrs['content']