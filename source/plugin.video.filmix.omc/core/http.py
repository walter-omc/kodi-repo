# -*- coding: utf-8 -*-

import os, re, sys, json, urllib, hashlib, traceback,base64
import xbmcup.app, xbmcup.db, xbmcup.system, xbmcup.net, xbmcup.parser, xbmcup.gui
import xbmc, cover, xbmcplugin, xbmcgui
from common import Render
from auth import Auth
from defines import *
import pickle
from pprint import pprint

try:
    cache_minutes = 60*int(xbmcup.app.setting['cache_time'])
except:
    cache_minutes = 0

class HttpData:

    mycookie = None

    def load(self, url):
        try:
            self.auth = Auth()
            self.cookie = self.auth.get_cookies()
            cook = self.mycookie if self.cookie == None else self.cookie
            response = xbmcup.net.http.get(url, cookies=cook, verify=False)
            if(self.cookie == None):
                self.mycookie = response.cookies
        except xbmcup.net.http.exceptions.RequestException:
            print traceback.format_exc()
            return None
        else:
            if(response.status_code == 200):
                if(self.auth.check_auth(response.text) == False):
                    self.auth.autorize()
                return response.text
            return None

    def post(self, url, data):
        try:
            data
        except:
            data = {}
        try:
            self.auth = Auth()
            self.cookie = self.auth.get_cookies()
            cook = self.mycookie if self.cookie == None else self.cookie
            response = xbmcup.net.http.post(url, data, cookies=cook, verify=False)

            if(self.cookie == None):
                self.mycookie = response.cookies

        except xbmcup.net.http.exceptions.RequestException:
            print traceback.format_exc()
            return None
        else:
            if(response.status_code == 200):
                if(self.auth.check_auth(response.text) == False):
                    self.auth.autorize()
                return response.text
            return None


    def ajax(self, url, data={}, referer=False):
        try:
            self.auth = Auth()
            self.cookie = self.auth.get_cookies()
            headers = {
                'X-Requested-With' : 'XMLHttpRequest'
            }
            if(referer):
                headers['Referer'] = referer


            cook = self.mycookie if self.cookie == None else self.cookie
            if(len(data) > 0):
                response = xbmcup.net.http.post(url, data=data, cookies=cook, headers=headers, verify=False)
            else:
                response = xbmcup.net.http.get(url, cookies=cook, headers=headers, verify=False)

            if(self.cookie == None):
                self.mycookie = response.cookies

        except xbmcup.net.http.exceptions.RequestException:
            print traceback.format_exc()
            return None
        else:
            return response.text if response.status_code == 200 else None

    def ajax_modern(self, url, data={}, referer=False):
        try:
            self.auth = Auth()
            self.cookie = self.auth.get_cookies()
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                # 'Cookie': 'sc34-market=f096179b826ae18999aca75bbcbe3a33; FILMIXNET=75ejqnnm5ifjouvg3r4asbeji5; yjkx3PoVDPXGv2R=c0b0ad4bedcdb77866329d99a47a6e609b99269956fb; x424=11644f524674e24b92e83cdde03357be',
                # 'Referer': 'https://filmix.me/search/blade',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }
            
            if(referer):
                headers['Referer'] = referer


            cook = self.mycookie if self.cookie == None else self.cookie
            if(len(data) > 0):
                
                # Get cookie
                response = xbmcup.net.http.get(SITE_URL)
                cook = response.cookies
                cook = {'sc34-market': cook.get('sc34-market'), 'FILMIXNET': cook.get('FILMIXNET')}
                
                #self.dev_log({
                    #'surl': surl, 
                    #'response_status': response.status_code,
                    #'response_cookie': response.cookies
                #})
                
                #s = xbmcup.net.http.Session()
                #req = xbmcup.net.http.Request('POST', url, data=data, cookies=cook, headers=headers)
                #prepped = req.prepare()
                #resp = s.send(prepped)
                
                #self.dev_log({
                    #'url': url, 
                    #'request_headers': resp.request.headers,
                    #'request_body': resp.request.body,
                    #'response_text': resp.text
                #})                

                
                response = xbmcup.net.http.post(url, data=data, cookies=cook, headers=headers, verify=False)
                #self.dev_log({
                    #'url': url, 
                    #'request_headers': response.request.headers,
                    #'request_body': response.request.body,
                    ## 'response_text': response.text
                #})
            else:
                response = xbmcup.net.http.get(url, cookies=cook, headers=headers, verify=False)

            if(self.cookie == None):
                self.mycookie = response.cookies

        except xbmcup.net.http.exceptions.RequestException:
            print traceback.format_exc()
            return None
        else:
            return response.text if response.status_code == 200 else None


    def get_movies(self, url, page, idname='dle-content', nocache=False, search="", itemclassname="shortstory"):
        page = int(page)

        if(page > 0 and search == ''):
            url = SITE_URL+"/"+url.strip('/')+"/page/"+str(page+1)
        else:
            url = SITE_URL+"/"+url.strip('/')

        # print url

        if(search != ''):
            html = self.ajax(url)
        else:
            html = self.load(url)
            
        #self.dev_log({ 'url': url, 'search': search, 'itemclassname': itemclassname, 'html_len': len(html) })
        #self.dev_save_bin(html, 'response.html')

        if not html:
            return None, {'page': {'pagenum' : 0, 'maxpage' : 0}, 'data': [], 'html_state_': 'Empty response'}
        
        result = {'page': {}, 'data': []}
        
        soup = xbmcup.parser.html(self.strip_scripts(html))

        if(search != ''):
            result['page'] = self.get_page_search(soup)
        else:
            result['page'] = self.get_page(soup)

        if(idname != ''):
            center_menu = soup.find('div', id=idname)
        else:
            center_menu = soup

        # self.dev_save_bin(str(center_menu), 'center_menu.html')
            
        try:
            for div in center_menu.find_all('article', class_=itemclassname):
                
                # href = div.find('div', class_='short')#.find('a')
                div_short = div.find('div', class_='short') #.find('a', class_='watch')

                # movie_name = div.find('div', class_='full').find('h3', class_='name').find('a').get_text()
                movie_name = div.find('div', class_='name-block').find('h2', class_='name').find('a').get_text()

                not_movie = True
                info = {}
                movie = {}
                
                try:
                    not_movie_test = div.find('span', class_='not-movie').get_text()
                except:
                    not_movie = False

                try:
                    movie['originaltitle'] = div.find('div', class_='origin-name').get_text()
                except:
                    movie['originaltitle'] = ''
					
                try:
                    quality = div.find('div', class_='full').find('div', class_='quality').get_text().strip()
                except:
                    quality = ''

                dop_information = []
                
                try:
                    year = div.find('div', class_='item year').find('a').get_text().strip()
                    dop_information.append(year)
                    info['year'] = year
                except:
                    info['year'] = ''
                    pass

                try:
                    genre = div.find('div', class_='category').find(class_='item-content').get_text().strip()
                    dop_information.append(genre)
                    info['genre'] = genre
                except:
                    info['genre'] = ''					
                    print traceback.format_exc()
					
					
                try:
                    info['rating' ] = int(div.find('span', class_='like-count-wrap').find('span', class_='count').get_text())
                except:
                    info['rating'] = 0
					
                try:
                    info['plot' ] = div.find('p', attrs={'itemprop' : 'description'}).get_text()
                except:
                    info['plot'] = 'Not Found'

                information = ''
                if(len(dop_information) > 0):
                    information = '[COLOR white]['+', '.join(dop_information)+'][/COLOR]'

                movieposter = div_short.find('img', class_='poster').get('src')
                movieposter = div_short.find('a', class_='fancybox').get('href')				
                movie_url = div_short.find('a', class_='watch').get('href')
                movie_id = re.compile('/([\d]+)-', re.S).findall(movie_url)[0]
                
                if not movieposter.startswith('http'):
                    movieposter = SITE_URL + movieposter

                result['data'].append({
                        'url': movie_url,
                        'id': movie_id,
                        'not_movie': not_movie,
                        'quality': self.format_quality(quality),
						'year': info['year'],
						'genre': info['genre'],
                        #'year': information,
                        'title': movie_name.strip(),
						'originaltitle': movie['originaltitle'],
						'plot': info['plot'],
						'rating': info['rating'],
                        'img': None if not movieposter else movieposter
                    })
        except:
            # self.dev_log({ 'article': '---', 'error': traceback.format_exc() })
            print traceback.format_exc()

        # self.dev_log({'Result' : result})

        if(nocache):
            return None, result
        else:
            return cache_minutes, result

    def get_movies_simple_search(self, url, data={}, nocache=False):
        
        url = SITE_URL + "/" + url.strip('/')

        # html = self.ajax_modern(url, data, SITE_URL + '/search/' + data['story'])
        html = self.ajax_modern(url, data)
        
        # self.dev_log({ 'url': url, 'data': data })
        # self.dev_save_bin(html, 'simple_search_results.html')

        if not html:
            return None, {'page': {'pagenum' : 0, 'maxpage' : 0}, 'data': [], 'html_state_': 'Empty response'}

        data['search_start'] = 0 if data['search_start'] == 1 else data['search_start']
        
        result = {'page': {}, 'data': []}
        
        soup = xbmcup.parser.html(self.strip_scripts(html))

        result['page'] = self.get_page_search(soup)

        center_menu = soup
            
        try:
            for div in center_menu.find_all('article', class_='shortstory'):
                
                div_short = div.find('div', class_='short') #.find('a', class_='watch')
                movie_name = div.find('div', class_='name-block').find('h2', class_='name').find('a').get_text()
                not_movie = True
                
                try:
                    not_movie_test = div.find('span', class_='not-movie').get_text()
                except:
                    not_movie = False

                try:
                    quality = div.find('div', class_='full').find('div', class_='quality').get_text().strip()
                except:
                    quality = ''

                dop_information = []
                
                try:
                    year = div.find('div', class_='item year').find('a').get_text().strip()
                    dop_information.append(year)
                except:
                    pass

                try:
                    genre = div.find('div', class_='category').find(class_='item-content').get_text().strip()
                    dop_information.append(genre)
                except:
                    print traceback.format_exc()

                information = ''
                if(len(dop_information) > 0):
                    information = '[COLOR white]['+', '.join(dop_information)+'][/COLOR]'

                movieposter = div_short.find('img', class_='poster').get('src')
                movie_url = div_short.find('a', class_='watch').get('href')
                movie_id = re.compile('/([\d]+)-', re.S).findall(movie_url)[0]

                result['data'].append({
                        'url': movie_url,
                        'id': movie_id,
                        'not_movie': not_movie,
                        'quality': self.format_quality(quality),
                        'year': information,
                        # 'name': '[' + str(data['search_start']) + ', ' + str(result['page']['pagenum']) + '] ' + movie_name.strip(),
                        'name': movie_name.strip(),
                        'img': None if not movieposter else movieposter
                    })
        except:
            print traceback.format_exc()
            # self.dev_log({ 'err': traceback.format_exc() })

        # self.dev_log({ 'result': result['page'] })
        # nocache = True

        if(nocache):
            return None, result
        else:
            return cache_minutes, result

    def decode_direct_media_url(self, encoded_url, checkhttp=False):
        if(checkhttp == True and (encoded_url.find('http://') != -1 or encoded_url.find('https://') != -1)):
            return False

        ca = 'y5U4ei6d7NJgtG2VlBxfsQ1Hz='
        cb = 'MXwR3m80TauZpDbokYnvIL9Wcr'
        
        for i, c in enumerate(ca):
            encoded_url = encoded_url.replace(c, '___')
            encoded_url = encoded_url.replace(cb[i], c)
            encoded_url = encoded_url.replace('___', cb[i])
            
        return base64.b64decode(encoded_url)

    def format_direct_link(self, source_link, q):
        regex = re.compile("\[([^\]]+)\]", re.IGNORECASE)
        return regex.sub(q, source_link)

    def get_qualitys(self, source_link):
        try:
            avail_quality = re.compile("\[([^\]]+)\]", re.S).findall(source_link)[0]
            return avail_quality.split(',')
        except:
            return '0'.split()

    def get_movie_info(self, url):
        html = self.load(url)

        movieInfo = {}
        movieInfo['no_files'] = None
        movieInfo['episodes'] = True
        movieInfo['movies'] = []
        movieInfo['resolutions'] = []

        # self.dev_log({ 'movie_info_url': url })
        # self.dev_save_bin(html, 'movie_info.html')

        if not html:
            movieInfo['no_files'] = 'HTTP error'
            return movieInfo

        html = html.encode('utf-8')
        soup = xbmcup.parser.html(self.strip_scripts(html))

        try:
            movieInfo['is_proplus'] = len(soup.find('span', class_='proplus'))
        except:
            movieInfo['is_proplus'] = 0

        #print self.strip_scripts(html)
        try:
            try:
                film_id = re.compile('film_id ?= ?([\d]+);', re.S).findall(html)[0].decode('string_escape').decode('utf-8')
                js_string = self.ajax(SITE_URL+'/api/movies/player_data', {'post_id' : film_id, 'show_full': True}, url)
                # self.dev_save_bin(js_string, 'player_data')
                player_data =  json.loads(js_string, 'utf-8')
                player_data = player_data['message']['translations']['flash']
            except:
                # self.dev_log({ 'get_movie_info': '---', 'error': traceback.format_exc() })
                movieInfo['no_files'] = xbmcup.app.lang[34026].encode('utf8')
                raise

            for translate in player_data:
                js_string = self.decode_direct_media_url(player_data[translate], True)
                # self.dev_log({ 'translation-flash as': js_string })
                if(js_string == False):
                    continue
                if(js_string.find('.txt') != -1):
                    playlist = self.decode_direct_media_url(self.load(js_string))
                    
                    # self.dev_log({ 'playlist txt-file': js_string })
                    # self.dev_save_bin(playlist, 'playlist.txt')

                    movies = json.loads(playlist, 'utf-8')
                    for season in movies['playlist']:
                        current_movie = {'folder_title' : season['comment']+' ('+translate+')', 'movies': {}}

                        for movie in season['playlist']:
                            avail_quality = self.get_qualitys(movie['file'])
                            for q in avail_quality:
                                if(q == ''): continue
                                direct_link = self.format_direct_link(movie['file'], q) if q != 0 else movie['file']
                                try:
                                    current_movie['movies'][q].append(direct_link)
                                except:
                                    current_movie['movies'][q] = []
                                    current_movie['movies'][q].append(direct_link)


                        #for resulut in current_movie['movies']:
                        #    current_movie['movies'][resulut] = current_movie['movies'][resulut][0]

                        movieInfo['movies'].append(current_movie)

                elif(js_string.find('http://') != -1 or js_string.find('https://') != -1):
                    avail_quality = self.get_qualitys(js_string)
                    current_movie = {'folder_title' : translate, 'movies': {}}
                    for q in avail_quality:
                        if(q == ''): continue
                        direct_link = self.format_direct_link(js_string, q) if q != 0 else js_string
                        try:
                            current_movie['movies'][q].append(direct_link)
                        except:
                            current_movie['movies'][q] = []
                            current_movie['movies'][q].append(direct_link)

                    movieInfo['movies'].append(current_movie)
                    
             #   break
            #print movieInfo['movies']

            movieInfo['title'] = soup.find('h1', class_='name').get_text()
            try:
                movieInfo['originaltitle'] = soup.find('div', class_='origin-name').get_text().strip()
            except:
                movieInfo['originaltitle'] = ''

            try:
                movieInfo['description'] = soup.find('div', class_='full-story').get_text().strip()
            except:
                movieInfo['description'] = ''

            try:
                movieInfo['fanart'] = SITE_URL+soup.find('ul', class_='frames-list').find('a').get('href')
            except:
                movieInfo['fanart'] = ''
            try:
                movieInfo['cover'] = soup.find('img', class_='poster').get('src')
                movieInfo['cover'] = soup.find('a', class_='fancybox').get('href')
                if not movieInfo['cover'].startswith('http'):
                    movieInfo['cover'] = SITE_URL + movieInfo['cover']
            except:
                movieInfo['cover'] = ''
            


            try:
                movieInfo['genres'] = []
                genres = soup.find('div', class_='category').find_all('a')
                for genre in genres:
                   movieInfo['genres'].append(genre.get_text().strip())
                movieInfo['genres'] = ' / '.join(movieInfo['genres']).encode('utf-8')
            except:
                movieInfo['genres'] = ''

            try:
                movieInfo['year'] = soup.find('div', class_='year').find('a').get_text()
            except:
                movieInfo['year'] = ''

            try:
                movieInfo['durarion'] = soup.find('div', class_='durarion').get('content')
                movieInfo['durarion'] = int(movieInfo['durarion'])*60
            except:
                movieInfo['durarion'] = ''

            try:
                movieInfo['ratingValue'] = float(soup.find(attrs={'itemprop' : 'ratingValue'}).get_text())
            except:
                movieInfo['ratingValue'] = 0

            try:
                movieInfo['ratingCount'] = int(soup.find(attrs={'itemprop' : 'ratingCount'}).get_text())
            except:
                movieInfo['ratingCount'] = 0

            try:
                movieInfo['director'] = []
                directors = soup.find('div', class_='directors').findAll('a')
                for director in directors:
                   movieInfo['director'].append(director.get_text().strip())
                movieInfo['director'] = ', '.join(movieInfo['director']).encode('utf-8')
            except:
                movieInfo['director'] = ''
        except:
            print traceback.format_exc()

        #print movieInfo
        
        # self.dev_log({ 'movieInfo': movieInfo })

        return movieInfo

    def get_modal_info(self, url):
        html = self.load(url)
        movieInfo = {}
        movieInfo['error'] = False
        if not html:
            movieInfo['error'] = True
            return movieInfo

        html = html.encode('utf-8')
        soup = xbmcup.parser.html(self.strip_scripts(html))

        try:
            movieInfo['desc'] = soup.find('div', class_='full-story').get_text().strip()
        except:
            movieInfo['desc'] = ''

        try:
            movieInfo['title'] = soup.find('h1', class_='name').get_text()
        except:
            movieInfo['title'] = ''

        try:
            movieInfo['originaltitle'] = soup.find('div', class_='origin-name').get_text().strip()
        except:
            movieInfo['originaltitle'] = ''

        if(movieInfo['originaltitle'] != ''):
             movieInfo['title'] = '%s / %s' % (movieInfo['title'],  movieInfo['originaltitle'])

        try:
            movieInfo['poster'] = soup.find('img', class_='poster').get('src')
            if not movieInfo['poster'].startswith('http'):
                movieInfo['poster'] = SITE_URL + movieInfo['poster']
        except:
            movieInfo['poster'] = ''

        movieInfo['desc'] = ''
        try:
            infos = soup.find('div', class_='full min').find_all('div', class_="item")
            skip = True
            for div in infos:
                if(skip):
                    skip = False
                    continue
                movieInfo['desc'] += self.format_desc_item(div.get_text().strip())+"\n"
        except:
           movieInfo['desc'] = traceback.format_exc()

        try:
            div = soup.find('div', class_='full-panel').find('span', class_='kinopoisk')
            rvalue = div.find('div', attrs={'itemprop' : 'ratingValue'}).get_text().strip()
            rcount = div.find('div', attrs={'itemprop' : 'ratingCount'}).get_text().strip()
            kp = xbmcup.app.lang[34029] % (self.format_rating(rvalue), rvalue, rcount)
            movieInfo['desc'] += kp+"\n"
        except:
            pass

        try:
            div = soup.find('div', class_='full-panel').find('span', class_='imdb').find_all('div')
            rvalue = div[0].get_text().strip()
            rcount = div[1].get_text().strip()
            kp = xbmcup.app.lang[34030] % (self.format_rating(rvalue), rvalue, rcount)
            movieInfo['desc'] += kp+"\n"
        except:
            pass

        try:
            desc = soup.find('div', class_='full-story').get_text().strip()
            movieInfo['desc'] += '\n[COLOR blue]%s[/COLOR]\n%s' % (xbmcup.app.lang[34027], desc)
        except:
            movieInfo['desc'] = traceback.format_exc()

        try:
            movieInfo['trailer'] = soup.find('li', attrs={'data-id' : "trailers"}).find('a').get('href')
        except:
            movieInfo['trailer'] = False

        return movieInfo

    def my_int(self, str):
        if(str == ''):
            return 0
        return int(str)

    def get_trailer(self, url):
        progress = xbmcgui.DialogProgress()
        progress.create(xbmcup.app.addon['name'])
        progress.update(0)
        html = self.load(url)
        movieInfo = {}
        movieInfo['error'] = False
        if not html:
            xbmcup.gui.message(xbmcup.app.lang[34031].encode('utf8'))
            progress.update(0)
            progress.close()
            return False

        progress.update(50)
        html = html.encode('utf-8')
        soup = xbmcup.parser.html(self.strip_scripts(html))

        link = self.decode_direct_media_url(soup.find('input', id='video-link').get('value'))
        avail_quality = max(map(self.my_int, self.get_qualitys(link)))
        progress.update(100)
        progress.close()
        return self.format_direct_link(link, str(avail_quality))

    def format_desc_item(self, text):
        return re.compile(r'^([^:]+:)', re.S).sub('[COLOR yellow]\\1[/COLOR] ', text)


    def strip_scripts(self, html):
        html = re.compile(r'<head[^>]*>(.*?)</head>', re.S).sub('<head></head>', html)
        #удаляет все теги <script></script> и их содержимое
        #сделал для того, что бы html parser не ломал голову на тегах в js
        return re.compile(r'<script[^>]*>(.*?)</script>', re.S).sub('', html)

    def format_rating(self, rating):
        rating = float(rating)
        if(rating == 0):
            return 'white'
        elif(rating > 7):
            return 'ff59C641'
        elif(rating > 4):
            return 'ffFFB119'
        else:
            return 'ffDE4B64'


    def format_quality(self, quality):
        if(quality == ''): return ''
        if(quality.find('1080') != -1):
            q = 'HD'
        elif(quality.find('720') != -1):
            q = 'HQ'
        elif(quality.find('480') != -1):
            q = 'SQ'
        else:
            q = 'LQ'

        qualitys = {'HD' : 'ff3BADEE', 'HQ' : 'ff59C641', 'SQ' : 'ffFFB119', 'LQ' : 'ffDE4B64'}
        if(q in qualitys):
            return "[COLOR %s][%s][/COLOR]" % (qualitys[q], quality)
        return ("[COLOR ffDE4B64][%s][/COLOR]" % quality if quality != '' else '')


    def get_page(self, soup):
        info = {'pagenum' : 0, 'maxpage' : 0}
        try:
            wrap  = soup.find('div', class_='navigation')
            info['pagenum'] = int(wrap.find('span', class_='').get_text())
            try:
                info['maxpage'] = len(wrap.find('a', class_='next'))
                if(info['maxpage'] > 0):
                    info['maxpage'] = info['pagenum']+1
            except:
                info['maxpage'] = info['pagenum']
                print traceback.format_exc()

        except:
            info['pagenum'] = 1
            info['maxpage'] = 1
            print traceback.format_exc()

        return info


    def get_page_search(self, soup):
        info = {'pagenum' : 0, 'maxpage' : 0}
        try:
            wrap  = soup.find('div', class_='navigation')
            current_page = wrap.find_all('span', class_='')
            info['pagenum'] = 1
            for cpage in current_page:
                if(cpage.get_text().find('...') == -1):
                    info['pagenum'] = int(cpage.get_text())
                    break

            try:
                clicks = wrap.find_all('span', class_='click')
                pages = []
                for page in clicks:
                    pages.append(int(page.get_text()))

                info['maxpage'] = max(pages)
            except:
                info['maxpage'] = info['pagenum']
                print traceback.format_exc()

        except:
            info['pagenum'] = 1
            info['maxpage'] = 1
            print traceback.format_exc()

        return info

    def dev_log(self, obj, filename='dev_log'):
        dname = "/home/osmc/.kodi/addons/plugin.video.filmix.net.dev/debug"
        fname = dname + '/' + filename
        fh = open(fname, 'a')
        # pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)
        pprint(obj, stream=fh)
        
        fh.close()

    def dev_save_bin(self, obj, filename='dev_bin_dump'):
        dname = "/home/osmc/.kodi/addons/plugin.video.filmix.net.dev/debug"
        fname = dname + '/' + filename
        
        with open(fname, 'wb') as fh:
            fh.truncate()
            pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)
