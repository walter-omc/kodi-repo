# coding: utf-8

#
# Copyright © 2017 weirdgiraffe <giraffe@cyberzoo.xyz>
#
# Distributed under terms of the MIT license.
#
import re
import base64

def movies_list(html):

    '''
<article class="shortstory line" itemscope="" itemtype="http://schema.org/Movie" data-pl-id="-1" data-id="124249">
	<div class="short">
		<span class=" like-count-wrap">
						<span class="like" data-id="124249">
				<span class="count red">-2</span>
				<span class="counter">
					<span class="rating">
						<span id="ratig-layer-124249">
							<span class="hand-up icon-like" onclick="doRate(1, '124249', 'cat'); return false;">
								<i title="Отлично" class="fa positive btn-tooltip "></i>
								<span class="rateinf ratePos">0</span>
							</span>
							<span class="hand-down icon-dislike" onclick="doRate(-1, '124249', 'cat'); return false;">
								<i title="Плохо" class="fa negative btn-tooltip "></i>
								<span class="rateinf rateNeg">2</span>
							</span>
						</span>
					</span>
				</span>
			</span>
			<a class="fancybox" href="http://filmix.info/uploads/posters/big/vasha-sulu-2017_124249_0.jpg">
				<img src="/uploads/posters/thumbs/w220/vasha-sulu-2017_124249_0.jpg" itemprop="image" class="poster poster-tooltip" alt="Ваша Сулу, 2017" title="Ваша Сулу">

			</a>
		</span>
		<a class="watch icon-play" itemprop="url" href="http://filmix.info/dramy/124249-vasha-sulu-2017.html" title="Ваша Сулу, 2017 смотреть онлайн">Смотреть онлайн</a>
	</div>
	<div class="full">

		<div class="top-date">
			<div class="quality">WEB-DLRip 720 </div>
			<div class="block-date">

				<time class="date" itemprop="dateCreated" datetime="2018-03-05T09:52:17+02:00">Сегодня, 09:52</time>


			</div>

		</div>
		<div class="name-block">
			<h2 class="name" itemprop="name" content="Ваша Сулу"><a itemprop="url" href="http://filmix.info/dramy/124249-vasha-sulu-2017.html" title="Ваша Сулу" class="btn-tooltip">Ваша Сулу</a></h2>
			<div class="origin-name" itemprop="alternativeHeadline" content="Tumhari Sulu"> Tumhari Sulu </div>
		</div>

		<div class="item category"><span class="lable">Жанр:</span><span class="item-content"><a itemprop="genre" href="http://filmix.info/dramy">Драмы</a>, <a itemprop="genre" href="http://filmix.info/komedii">Комедия</a></span></div>
		<div class="item year"><span class="lable">Год:</span><span class="item-content"><a itemprop="copyrightYear" href="http://filmix.info/films/y2017">2017</a></span>


			</div>
		<div class="item translate"><span class="lable">Перевод:</span><span class="item-content">Любительский, многоголосый</span></div>
		<div class="item actors" hidden=""><span class="lable">Режисер:</span><span class="item-content" itemprop="director">Суреш Тривени</span></div>
		<div class="item actors"><span class="lable">В ролях:</span><span class="item-content"><span>Видья Балан,&nbsp;</span><span>Неха Дхупия,&nbsp;</span><span>Манав Каул,&nbsp;</span><span>Виджай Маурья,&nbsp;</span><span>Santanu Ghatak</span></span></div>
		<p itemprop="description">Обычная домохозяйка Сулочна (Сулу) мечтает о жизни современной работающей женщины, и волею судеб получает работу радиоведущей в полуночной программе «для...</p>
		<div class="close-wrap icon-close"></div>
	</div>
	<div class="panel-wrap">
		<div class="panel">
			<div class="panel_num">
				<div class="comm_num btn-tooltip icon-reviewsNeutral" title="Количество комментариев">
					<span>0</span>
				</div>
			</div>

			<div class="add-watch-later btn-tooltip icon-future " id="future-id-124249" onclick="watch_later('124249', '', 'short'); return false" title="Посмотреть позже"></div>
			<div class="add-favorite btn-tooltip icon-favorite " id="fav-id-124249" onclick="common.doFavorites('124249', '', 0, 'short'); return false;" title="Добавить в закладки"></div>
		</div>
	</div>
</article>
    :param html:
    :return:
    '''

    r = re.compile(r'(<article class="shortstory.*?</article>)', re.DOTALL)
    for article in r.findall(html):
        yield _parse_movie_article(article);


    # r = re.compile(r'<li data-click="translate[^>]*?>([^<]+)</li>[\s\n]*?'
    #                '<script>pl\[\d+\] = "(.*?)";',
    #                re.DOTALL)
    # for name, url in r.findall(translations):
    #     yield {'tr': name.strip() if name != 'Стандартный' else None,
    #            'url': url.strip()}
    #
    # for i in range(0, 15):
    #     item = {
    #         'title': 'Звёздные Войны: Последние джедаи {0}'.format(i),
    #         'originaltitle': 'originaltitle',
    #         'year': '1198',
    #         'duration': 123,
    #         'genre': ['Фантастика'],
    #         'plot': 'Plot',
    #         'rating': 22 + i,
    #         'cast': ['A', 'B'],
    #         'thumb': 'http://filmix.info//uploads/posters/thumbs/w220/zvezdnye-voyny-poslednie-dzhedai-2017_117051_0.jpg'
    #     }
    #     yield item

def _parse_movie_article(html):

    item = {}

    item = {
        'title': 'Звёздные Войны: Последние джедаи',
        'originaltitle': 'originaltitle',
        'year': '1198',
        'duration': 32343,
        'genre': ['Фантастика'],
        'plot': 'Plot',
        'rating': 22,
        'cast': ['A', 'B'],
        'thumb': 'http://filmix.info//uploads/posters/thumbs/w220/zvezdnye-voyny-poslednie-dzhedai-2017_117051_0.jpg'
    }

    '''
    <h2 class="name" itemprop="name" content="Ваша Сулу"><a itemprop="url" href="http://filmix.info/dramy/124249-vasha-sulu-2017.html" title="Ваша Сулу" class="btn-tooltip">Ваша Сулу</a></h2>
                <div class="origin-name" itemprop="alternativeHeadline" content="Tumhari Sulu">
    '''
    # Title
    r = re.compile(# r'<div class="name-block">.*?'
                    r'<h2 class="name".*?content="(.*?)"'
                    r'.*?<a.*?href="(.*?)"'
                    r'.*?</h2>'
                    r'.*?<div class="origin-name".*?content="(.*?)"'
                    # r'</div>'
    )
    m = r.search(html)
    if m:
        item['title'] = m.group(1)
        #item['originaltitle'] = m.group(3)
        item['url'] = m.group(2)

    # Description
    r = re.compile(r'<p itemprop="description">(.*?)</p>')
    m = r.search(html)
    if m:
        item['plot'] = m.group(1)

    return item

"""
    Seasonvar
"""

def main_page_items(main_page_html, datestr):
    '''Collect all dayblock items(i.e episode changes) for a given date
    and yields dict {'url': ..., 'name': ..., 'changes': ...} for each
    episode for that date.

    datestr should be in format 'dd.mm.yyyy'
    '''
    for (date, dayblock) in _main_page_dayblocks(main_page_html):
        if datestr == date:
            for item in _main_page_dayblock_items(dayblock):
                yield item


def search_items(search_response):
    '''yield dict {'name':..., 'url': ...} for items in search_response

    search_response is dict representation of search response
    '''
    try:
        r = re.compile(r'serial-\d+-[^.]+?\.html')
        suggestions = search_response['suggestions']
        data = search_response['data']
        for name, url in zip(suggestions['valu'], data):
            if url and r.match(url) is not None:
                yield {'name': name, 'url': '/' + url}
    except (KeyError, TypeError):
        return


def seasons(season_page_html):
    '''takes content of season page and yields
    all seasons for the same show.

    season_page_html should be utf-8 encoded html content
    '''
    r = re.compile(r'<h2>\s*<a\s+href="(/serial-\d+-[^.]+?\.html)"')
    for url in r.findall(season_page_html):
        yield url


def player_params(season_page_html):
    '''extract parameters for player.php to retrieve playlists
    if parameters not found return None
    '''
    sands = _season_and_serial(season_page_html)
    sandt = _secure_and_time(season_page_html)
    if sands and sandt:
        return {
                'id': sands[0],
                'serial': sands[1],
                'secure': sandt[0],
                'time': sandt[1],
                'type': 'html5',
        }


def playlists(player_response_html):
    '''takes response from player.php and yield dict {'tr':..., 'url':...}
    where 'tr' is a translation name and 'url' is a playlist url.
    If no translations found on page, then search for playlist urls only
    will be done. In this case translation names will be None.

    season_page_html should be utf-8 encoded html content
    '''
    r = re.compile(r'var pl = {\'0\': "(.+)"};')
    for url in r.findall(player_response_html):
        yield {'tr': None,
               'url': url.strip()}
    translations = _translate_list(player_response_html)
    if translations is not None:
        r = re.compile(r'<li data-click="translate[^>]*?>([^<]+)</li>[\s\n]*?'
                       '<script>pl\[\d+\] = "(.*?)";',
                       re.DOTALL)
        for name, url in r.findall(translations):
            yield {'tr': name.strip() if name != 'Стандартный' else None,
                   'url': url.strip()}


def episodes(playlist):
    '''yield dict {'name':..., 'url': ...} for items in playlist_dict

    playlist_html is response from requester.playlist()
    '''
    for entry in playlist:
        if 'playlist' in entry:
            for episode in entry['playlist']:
                yield {'url': episode['file'],
                       'name': episode['title'].replace('<br>', ' ')}
        else:
            yield {'url': entry['file'],
                   'name': entry['title'].replace('<br>', ' ')}


def _translate_list(season_page_html):
    r = re.compile(r'<ul class="pgs-trans"(.*?)</ul>', re.DOTALL)
    for b in r.findall(season_page_html):
        return b


def _season_and_serial(season_page_html):
    r = re.compile(r'data-id-season="(\d+)"\s+data-id-serial="(\d+)"')
    match = r.search(season_page_html)
    if match:
        return match.groups()


def _secure_and_time(season_page_html):
    r = re.compile(r"var\s+data4play\s*=\s*{\s*"
                   r"'secureMark'\s*:\s*'([a-f0-9]+)',\s*"
                   r"'time'\s*:\s*([0-9]+)\s*"
                   r"}")
    match = r.search(season_page_html)
    if match:
        return match.groups()


def _main_page_dayblocks(full_page_html):
    '''Collect all dayblocks from full_page_html
    and yield (date, content) for every dayblock'''
    r = re.compile(
        r'<div class="news-head">\s*?(\d{2}\.\d{2}\.\d{4})(.*?)'
        r'(?=<div class="doptxt"|<div class="news")',
        re.DOTALL)
    for group in r.findall(full_page_html):
        d, c = group
        yield group


def _main_page_dayblock_items(dayblock_content):
    '''Collect all series items from dayblock_content
    and for every item yield dict with description'''
    r = re.compile(
        r'<a href="(\/serial-.+?\.html)"[^>]*?>'
        '.*?div.*?<div[^>]*?>(.+?)<\/div>'
        '(.*?)<span[^>]*?>(.+?)<\/span>.*?<\/a>',
        re.DOTALL)
    for (url, name, season, changes) in r.findall(dayblock_content):
        changes = season.strip() + ' ' + changes.strip()
        name = name.replace("<span>", "")
        name = name.replace("</span>", "")
        yield {'url': url,
               'name': name.strip(),
               'changes': changes.strip()}
