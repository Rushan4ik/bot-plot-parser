import difflib
import json
from urllib import parse

import requests
import bs4

BEATPORT_CONSTANTS = {
    "way_for_search": "https://www.beatport.com/search?"
}
SRC_NOT_FOUND = "NONE"
SRC_RE_PARSING = "RE-PARSING"


def parse_track(search_query):
    res = dict()
    str_search_url = prepare_str_for_url(search_query)
    str_search_for_similar = prepare_str_for_check_similar(search_query)
    req_url = get_url_search_track(str_search_url)
    res['srch'] = str_search_for_similar
    res['url'] = SRC_NOT_FOUND
    res['smlr'] = ''
    res['perc'] = ''
    res_page = None
    try:
        res_page = requests.get(req_url)
    except Exception as e:
        res['url'] = SRC_RE_PARSING

    if not res_page:
        return res

    html_script = bs4.BeautifulSoup(res_page.text, 'html.parser')
    html_script = html_script.find('script', id='data-objects')

    js_script = html_script.contents[0]

    js_script = js_script[js_script.find('window.Playables'):]
    js_script = js_script[js_script.find('{'):]
    js_script = js_script[:js_script.find(']};')+2]

    data = json.loads(js_script)

    if not data['tracks']:
        return res

    similar_tracks = list()
    for i, track in enumerate(data['tracks']):
        if track['component'] == "Search Result - Tracks":
            str_res_for_similar = prepare_res_arr_for_check_similar(track)
            str_res_for_similar, percent = get_most_similar_track_name(str_search_for_similar, str_res_for_similar)
            similar_tracks.append([i, str_res_for_similar, percent])

    similar_tracks.sort(key=lambda row: row[2], reverse=True)
    res['smlr'] = similar_tracks[0][1]
    res['perc'] = similar_tracks[0][2]
    res['url'] = data['tracks'][similar_tracks[0][0]]['preview']['mp3']['url']

    return res


def get_url_search_track(search_url):
    return BEATPORT_CONSTANTS['way_for_search'] + search_url


def prepare_str_for_url(s: str):
    s = s.strip()
    return parse.urlencode({'q': s})


def prepare_str_for_check_similar(s: str):
    for garbage in '-,&()':
        s = s.replace(garbage, '')
    return s.replace('  ', ' ').lower()


def prepare_res_arr_for_check_similar(arr):
    res = dict()
    res['name'] = arr['name']
    res['mix'] = arr['mix']
    res['artists'] = [artist['name'] for artist in arr['artists']]

    return res


def get_most_similar_track_name(str_search, arr_track):
    artists = []
    res = []
    sim = []
    str_track = arr_track['name'] + " " + arr_track['mix']

    artists.append(' '.join(arr_track['artists']))
    artists.append(' '.join(reversed(arr_track['artists'])))

    res.append(prepare_str_for_check_similar(artists[0] + ' ' + str_track))
    res.append(get_similar_perc(str_search, res[0]))

    sim.append((prepare_str_for_check_similar(artists[1] + " " + str_track)))
    sim.append(get_similar_perc(str_search, sim[0]))

    if res[1] < sim[1]:
        res = sim

    return res


def get_similar_perc(str_search, str_track):
    matcher = difflib.SequenceMatcher(None, str_search, str_track)
    return matcher.ratio() * 100

