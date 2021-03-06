# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#

import filmix.parser as parser
import re
from filmix.requester import Requester, HTTPError, NetworkError



"""
    Seasonvar
"""
def movies_list():
    r = Requester()
    response = r.movies_list()
    return parser.movies_list(response)

def day_items(datestr):
    r = Requester()
    page = r.main_page()
    return parser.main_page_items(page, datestr)


def thumb_url(season_url):
    r = re.compile(r'^(?:http://)?.*?/serial-(\d+)-(?:.+?)'
                   '(?:-\d+-(?:sezon|season))?\.html$')
    for sid in r.findall(season_url):
        return 'http://cdn.seasonvar.ru/oblojka/{0}.jpg'.format(sid)


def seasons(season_url):
    r = Requester()
    p = r.season_page(season_url)
    params = parser.player_params(p)
    if params is None:
        return None, None
    seasons = list(parser.seasons(p))
    snum = [n for n, u in enumerate(seasons, 1) if u == season_url][0]
    return snum, seasons


def season_info(season_url):
    r = Requester()
    p = r.season_page(season_url)
    params = parser.player_params(p)
    if params is None:
        return {}
    seasons = list(parser.seasons(p))
    snum = [n for n, u in enumerate(seasons, 1) if u == season_url][0]
    p = r.player(season_url, params)
    if p is not None:
        return {
            'number': snum,
            'total': len(seasons),
            'playlist': list(parser.playlists(p)),
        }


def episodes(playlist_url):
    r = Requester()
    p = r.playlist(playlist_url)
    return list(parser.episodes(p))


def search(term):
    if term is not None:
        r = Requester()
        response = r.search(term)
        return parser.search_items(response)
