# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
from kodi import logger, Plugin
import filmix
from datetime import datetime, timedelta

def main(plugin):

    # Поиск
    searchurl = plugin.make_url({'screen': 'search'})
    plugin.add_screen_directory('[COLOR FFFFD700]Поиск[/COLOR]', searchurl)

    # Расширенный поиск
    searchurl = plugin.make_url({'screen': 'advanced_search'})
    plugin.add_screen_directory('[COLOR FFFFD700]Расширенный поиск[/COLOR]', searchurl)

    # Фильмы
    searchurl = plugin.make_url({'screen': 'list', 'category': 'movies'})
    plugin.add_screen_directory('[COLOR FFFFD700]Фильмы[/COLOR]', searchurl)

    # Сериалы
    searchurl = plugin.make_url({'screen': 'list', 'category': 'series'})
    plugin.add_screen_directory('[COLOR FFFFD700]Сериалы[/COLOR]', searchurl)

    # Мультфильмы
    searchurl = plugin.make_url({'screen': 'list', 'category': 'cartoons'})
    plugin.add_screen_directory('[COLOR FFFFD700]Мультфильмы[/COLOR]', searchurl)

    # Избранное
    searchurl = plugin.make_url({'screen': 'list', 'category': 'favorites'})
    plugin.add_screen_directory('[COLOR FFFFD700]Избранное[/COLOR]', searchurl)

    # Недавно просмотренное

    """
        Можно:
            - очистить весь список
            - удалить запись
            - добавить из списка в избранное
    """
    searchurl = plugin.make_url({'screen': 'list', 'category': 'history'})
    plugin.add_screen_directory('[COLOR FFFFD700]Недавно просмотренное[/COLOR]', searchurl)

    plugin.publish_screen(True)

def list(plugin):
    category = plugin.args.get('category')

    {
        'movies': list_movies

     }[category](plugin)

def list_movies(plugin):
    page = plugin.args.get('page')

    for item in filmix.movies_list():
        url = plugin.make_url({
            'screen': 'movie',
            'url': 'sdlfksdjflsd'
        })

        name = '{0} [COLOR FFFFD700]{1}[/COLOR]'.format(
            item['title'],
            '22'
        )

        plugin.add_screen_item(name, url,
            thumb=item['thumb'],
            folder=False,
            media='video',
            info={
                'Title': item['title'],
                'OriginalTitle': item['originaltitle'],
                'Year': item['year'],
                'plot': item['plot'],
                'Duration': item['duration'],
                'Genre': item['genre'],
                'UserRating': item['rating'],
                'cast': item['cast']
            }
        )

    # li = xbmcgui.ListItem(name)
    # # if thumb is not None:
    # #     li.setArt(thumb)
    # #     # it is sayed that both of these methods are deprecated
    # #     # see: http://kodi.wiki/view/Jarvis_API_changes
    # #     # but only these methods actually works with Jarvis
    # #     li.setIconImage(thumb)
    # #     li.setThumbnailImage(thumb)
    #
    #
    # li.setProperty('IsPlayable', 'true')
    # ret = xbmcplugin.addDirectoryItem(self._handler, url, li, False)
    # if not ret:
    #     logger.error('failed to add {0} playable item'.format(name))




    # for i in filmix.movies_list(page):

    # for i in seasonvar.day_items(date):
    #     url = plugin.make_url({
    #         'screen': 'episodes',
    #         'url': i['url'],
    #     })
    #     name = '{0} [COLOR FFFFD700]{1}[/COLOR]'.format(
    #             i['name'], i['changes'])
    #     plugin.add_screen_directory(name, url,
    #                                 thumb=seasonvar.thumb_url(i['url']))
    plugin.publish_screen(True)



def render(plugin):
    screen = plugin.args.get('screen')
    if screen is None:
        screen = 'main'
    try:
        if 'play' in plugin.args:
            play(plugin)
            return
        if 'q' in plugin.args:
            direct_search(plugin)
            return
        {
            'main': main,
            'list': list,
            'movies': list_movies,

            'week': week,
            'day': day,
            'episodes': episodes,
            'seasons': seasons,
            'translations': translations,

            'search': search,
            'advanced_search': search,
        }[screen](plugin)
    except KeyError:
        logger.error('unexpected screen "{0}"'.format(screen))
    except filmix.NetworkError:
        logger.error('NetworkError')
        plugin.show_notification(
            'Network error',
            'Check your connection')
    except filmix.HTTPError:
        logger.error('HTTPError')
        plugin.show_notification(
            'HTTP error',
            'Something goes wrong. Please, send your logs to addon author')


"""
    Seasonvar
"""


def week(plugin):
    date = datetime.today()
    for date_offset in range(7):
        datestr = date.strftime('%d.%m.%Y')
        dayurl = plugin.make_url({
            'screen': 'day',
            'date': datestr,
        })
        plugin.add_screen_directory(datestr, dayurl)
        date -= timedelta(days=1)

    searchurl = plugin.make_url({'screen': 'search'})
    plugin.add_screen_directory('[COLOR FFFFD700]Поиск[/COLOR]', searchurl)

    plugin.publish_screen(True)


def day(plugin):
    date = plugin.args.get('date')
    if date is None:
        logger.error('{0}: "date" arg is missing or malformed: {0}'.format(
            'screen "day"', plugin.args))
        plugin.publish_screen(False)
        return
    for i in seasonvar.day_items(date):
        url = plugin.make_url({
            'screen': 'episodes',
            'url': i['url'],
        })
        name = '{0} [COLOR FFFFD700]{1}[/COLOR]'.format(
                i['name'], i['changes'])
        plugin.add_screen_directory(name, url,
                                    thumb=seasonvar.thumb_url(i['url']))
    plugin.publish_screen(True)


def direct_search(plugin):
    term = plugin.args.get('q')
    if term is None:
        logger.error('{0}: "q" arg is missing or malformed: {0}'.format(
            'screen "direct_search"', plugin.args))
        plugin.publish_screen(False)
        return
    for i in seasonvar.search(term):
        if i['url'] is not None:
            season_url = i['url'].encode('utf-8')
            url = plugin.make_url({
                'screen': 'episodes',
                'url': season_url,
            })
            plugin.add_screen_directory(
                    i['name'],
                    url,
                    thumb=seasonvar.thumb_url(season_url)
            )
    plugin.publish_screen(True)


def search(plugin):
    term = plugin.read_input('Что искать?')
    plugin.args["q"] = term
    direct_search(plugin)


def episodes(plugin):
    season_url = plugin.args.get('url')
    if season_url is None:
        logger.error('{0}: "url" arg is missing or malformed: {0}'.format(
            'screen "episodes"', plugin.args))
        plugin.publish_screen(False)
        return
    tr = plugin.args.get('tr')
    thumb = seasonvar.thumb_url(season_url)
    season = seasonvar.season_info(season_url)
    if season is None or len(season) == 0:
        logger.error('{0}: failed to get season info: {0}'.format(
            'screen "episodes"', plugin.args))
        plugin.show_notification(
            'Content is blocked',
            'Or external player is being used')
        plugin.publish_screen(False)
        return
    if season.get('total', 0) > 1:
        url = plugin.make_url({
            'screen': 'seasons',
            'url': season_url,
        })
        name = '[COLOR FFFFD700]сезон[/COLOR]: {0} / {1}'.format(
                season['number'], season['total'])
        plugin.add_screen_directory(name, url)
    if len(season.get('playlist', [])) > 1:
        url = plugin.make_url({
            'screen': 'translations',
            'url': season_url,
            'tr': tr,
        })
        name = '[COLOR FFFFD700]озвучка[/COLOR]: {0}'.format(
                tr if tr is not None else 'Стандартная')
        plugin.add_screen_directory(name, url)
    pl_url = (x['url'] for x in season.get('playlist', []) if x['tr'] == tr)
    for e in (x for url in pl_url for x in seasonvar.episodes(url)):
        url = plugin.make_url({'play': e['url']})
        plugin.add_screen_item(e['name'], url, thumb=thumb)
    plugin.publish_screen(True)


def seasons(plugin):
    season_url = plugin.args.get('url')
    if season_url is None:
        logger.error('{0}: "url" arg is missing or malformed: {0}'.format(
            'screen "seasons"', plugin.args))
        plugin.publish_screen(False)
        return
    num, seasons = seasonvar.seasons(season_url)
    if seasons is None:
        logger.error('{0}: failed to get season info: {0}'.format(
            'screen "seasons"', plugin.args))
        plugin.publish_screen(False)
        return
    for n, s in enumerate(seasons, 1):
        prefix = '* ' if n == num else ''
        name = '{0}сезон {1}'.format(prefix, n)
        url = plugin.make_url({
            'screen': 'episodes',
            'url': s,
        })
        plugin.add_screen_directory(name, url, thumb=seasonvar.thumb_url(s))
    plugin.publish_screen(True)


def translations(plugin):
    season_url = plugin.args.get('url')
    if season_url is None:
        logger.error('{0}: "url" arg is missing or malformed: {0}'.format(
            'screen "translations"', plugin.args))
        plugin.publish_screen(False)
        return
    tr = plugin.args.get('tr')
    thumb = seasonvar.thumb_url(season_url)
    season = seasonvar.season_info(season_url)
    if season is None:
        logger.error('{0}: failed to get season info: {0}'.format(
            'screen "translations"', plugin.args))
        plugin.publish_screen(False)
        return
    for n, pl in enumerate(season['playlist']):
        if tr is None and n == 0 or pl['tr'] == tr:
            prefix = '* '
        else:
            prefix = ''
        url = plugin.make_url({
            'screen': 'episodes',
            'url': season_url,
            'tr': pl['tr'],
        })
        name = '{0}{1}'.format(
                prefix,
                pl['tr'] if pl['tr'] is not None else 'Стандартная')
        plugin.add_screen_directory(name, url, thumb=thumb)
    plugin.publish_screen(True)


def play(plugin):
    play_url = plugin.args.get('play')
    if play_url is None:
        logger.error('{0}: "url" arg is missing or malformed: {0}'.format(
            'play', plugin.args))
        plugin.publish_screen(False)
        return
    plugin.play(play_url)


# def render(plugin):
#     screen = plugin.args.get('screen')
#     if screen is None:
#         screen = 'main'
#     try:
#         if 'play' in plugin.args:
#             play(plugin)
#             return
#         if 'q' in plugin.args:
#             direct_search(plugin)
#             return
#         {
#             'main': main,
#             'movies': list_movies,
#
#             'week': week,
#             'day': day,
#             'episodes': episodes,
#             'seasons': seasons,
#             'translations': translations,
#
#             'search': search,
#             'advanced_search': search,
#         }[screen](plugin)
#     except KeyError:
#         logger.error('unexpected screen "{0}"'.format(screen))
#     except seasonvar.NetworkError:
#         logger.error('NetworkError')
#         plugin.show_notification(
#             'Network error',
#             'Check your connection')
#     except seasonvar.HTTPError:
#         logger.error('HTTPError')
#         plugin.show_notification(
#             'HTTP error',
#             'Something goes wrong. Please, send your logs to addon author')


if __name__ == "__main__":
    import sys
    render(Plugin(*sys.argv))
