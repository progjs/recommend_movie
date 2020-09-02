import datetime

import pymysql
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import numpy as np
import pandas as pd
from urllib.request import urlretrieve


def get_date():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    date = yesterday.strftime('%Y%m%d')
    return date


def get_movie_url():
    main_url = 'https:/"/movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + get_date

    movie_list = []
    for i in [1, 2, 4, 5, 6, 7, 11, 13, 15, 16, 18, 19]:

        for page_num in [1, 2]:
            movie_genre_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + str(
                get_date) + '&tg=' + str(
                i) + '&page=' + str(page_num)
            html = requests.get(movie_genre_url).text
            soup = BeautifulSoup(html, 'html.parser')

            a_tag_list = soup.select('div .tit5 a[href*=basic.nhn]')

            for idx, a_tag in enumerate(a_tag_list, 1):
                if idx > 50:
                    break
                movie_dict = {}
                title = a_tag.text.strip()
                link = urljoin(main_url, a_tag['href'])

                movie_dict['genre_code'] = i
                movie_dict['id'] = idx
                movie_dict['title'] = title
                movie_dict['url'] = link
                # scorre_url 은 평점을 스크래핑하기 위한 페이지
                movie_dict['score_url'] = link.replace('basic', 'pointWriteFormList')
                movie_list.append(movie_dict)
                # print(idx, title, link)

    return movie_list


def get_movie_id():
    movie_code_list = []

    for i in [1, 2, 4, 5, 6, 7, 11, 13, 15, 16, 18, 19]:
        for page_num in [1, 2]:
            movie_genre_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + str(
                get_date) + '&tg=' + str(
                i) + '&page=' + str(page_num)
            html = requests.get(movie_genre_url).text
            soup = BeautifulSoup(html, 'html.parser')

            a_tag_list = soup.select('div .tit5 a[href*="basic.nhn"]')

            for idx, a_tag in enumerate(a_tag_list, 1):
                if idx > 50:
                    break
                movie_code = re.findall("\d+", a_tag['href'])

                for movie in movie_code:
                    movie_code_list.append(movie)

    # movie_code_list = temp_movie_code_list
    return movie_code_list


def get_movie_detail(movie_list):
    movie_info_lists = []

    for movie in movie_list:
        html = requests.get(movie['url']).text
        soup = BeautifulSoup(html, 'html.parser')

        movie_info_dict = {}

        # 타이틀
        title = soup.select_one('h3.h_movie a[href*="basic.nhn"]')
        if title is None:
            movie_info_dict['title'] = None
        else:
            movie_info_dict['title'] = title.text.strip().replace(',', '')

        # 네티즌 평점
        score = soup.select_one('div.netizen_score .star_score em')
        if score is None:
            movie_info_dict['score'] = None
        else:
            movie_info_dict['score'] = score.text.strip()

        # 개봉국가
        nation = soup.select_one('dl.info_spec span a[href*="nation"]')
        if nation is None:
            movie_info_dict['nation'] = None
        else:
            movie_info_dict['nation'] = nation.text.strip()

        # 감독
        director = soup.select_one('dl.info_spec a[href*="code"]')
        if director is None:
            movie_info_dict['director'] = None
        else:
            movie_info_dict['director'] = director.text.strip()

        # 누적관객수
        audience = soup.select_one('p.count')
        if audience is None:
            movie_info_dict['audience'] = None
        else:
            movie_info_dict['audience'] = re.sub(r"(명)\([^()]*\)", "", audience.text.strip()).replace(',', '')

        # 관람객 평점 건수
        comment_count = soup.select_one('div.netizen_score .user_count em')
        if comment_count is None:
            movie_info_dict['comment_count'] = None
        else:
            movie_info_dict['comment_count'] = comment_count.text.strip().replace(',', '')

        for num in range(9, 0, -2):
            release_year = soup.select_one('dl.info_spec span:nth-of-type(4) a:nth-of-type(%d)' % num)
            if release_year is not None:
                movie_info_dict['release_year'] = release_year.text.strip()
                break
            else:
                movie_info_dict['release_year'] = None

        # 평점
        movie_info_dict['score_sum'] = 0

        # 줄거리
        plot = soup.select_one('.con_tx')
        if plot is None:
            movie_info_dict['plot'] = None
        else:
            movie_plot = " ".join(re.sub('|  |\t|\r|\n|,|\'|', '', plot.text).split())
            movie_info_dict['plot'] = movie_plot

        movie_info_lists.append(movie_info_dict)

        data_df = pd.DataFrame(
            columns=['title', 'score', 'nation', 'director', 'audience', 'plot', 'score_sum', 'comment_count',
                     'release_year'])

        for data in movie_info_lists:
            series_obj = pd.Series(data)
            data_df = data_df.append(series_obj, ignore_index=True)

        # 인덱스를 1부터 시작하는 방법
        data_df.index = np.arange(1, len(data_df) + 1)

        data_df.to_csv('C:/mypython/project_test/movieapp_movie.csv', index=True, header=False, encoding='utf-8-sig')


# def movie_detail_dataframe():
#     data_df = pd.DataFrame(
#         columns=['title', 'score', 'nation', 'director', 'audience', 'plot', 'score_sum', 'comment_count',
#                  'release_year'])
#
#     for data in movie_info_lists:
#         series_obj = pd.Series(data)
#         data_df = data_df.append(series_obj, ignore_index=True)
#
#     # 인덱스를 1부터 시작하는 방법
#     data_df.index = np.arange(1, len(data_df) + 1)


def get_genre_by_movie(movie_list):
    movie_genre_lists = []

    for movie in movie_list:
        movie_genre_dict = {}

        html = requests.get(movie['url']).text
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.select_one('h3.h_movie a[href*="basic.nhn"]')
        if title is None:
            movie_genre_dict['title'] = None
        else:
            movie_genre_dict['title'] = soup.select_one('h3.h_movie a[href*="basic.nhn"]').text.strip().replace(',', '')

        genre = soup.select_one('dl.info_spec span')
        if genre == None:
            movie_genre_dict['genre'] = None
        else:
            movie_genre_dict['genre'] = re.sub(r"\s+", "", genre.text.strip())

        movie_genre_lists.append(movie_genre_dict)

    print(len(movie_genre_lists))

    for movie_genre in movie_genre_lists:
        print(movie_genre)

    final_genre_list = []

    for idx, movie_genre in enumerate(movie_genre_lists, 1):
        if movie_genre['genre'] is None:
            movie_genre['genre'] = '로그인 필요(19금)'
        else:
            genres = movie_genre['genre'].split(',')

        for genre in genres:
            genre_dict = {'movie_id': idx, 'genre': genre}
            final_genre_list.append(genre_dict)

    genre_data_df = pd.DataFrame(columns=['genre', 'movie_id'])
    for final_genre in final_genre_list:
        series_obj = pd.Series(final_genre)
        genre_data_df = genre_data_df.append(series_obj, ignore_index=True)

    # 인덱스를 1부터 시작하는 방법
    genre_data_df.index = np.arange(1, len(genre_data_df) + 1)
    genre_data_df.to_csv('C:/mypython/project_test/movieapp_genre.csv', index=True, header=False, encoding='utf-8-sig')


def get_actor_by_movie(movie_list):
    movie_actor_list = []

    for movie in movie_list:
        movie_actor_dict = {}
        # print(movie)
        html = requests.get(movie['url']).text
        soup = BeautifulSoup(html, 'html.parser')

        actor = soup.find('dl', attrs={"class": "info_spec"})
        if actor is None:
            movie_actor_dict['actor'] = None
        else:
            movie_actor_dict['actor'] = re.sub(r'\([^)]*\)', '', actor.find_all("dd")[2].text.replace('더보기', ''))

        movie_actor_list.append(movie_actor_dict)

    print(len(movie_actor_list))

    for movie_actor in movie_actor_list:
        print(movie_actor)

    final_actor_list = []

    for idx, movie_actor in enumerate(movie_actor_list, 1):
        if movie_actor['actor'] is None:
            movie_actor['actor'] = None
        else:
            actors = movie_actor['actor'].split(', ')

        for actor in actors:
            actor_dict = {'movie_id': idx, 'actor': actor}
            final_actor_list.append(actor_dict)

    actor_data_df = pd.DataFrame(columns=['actor', 'movie_id'])
    for final_actor in final_actor_list:
        series_obj = pd.Series(final_actor)
        actor_data_df = actor_data_df.append(series_obj, ignore_index=True)

    # 인덱스를 1부터 시작하는 방법
    # 인덱스 값 변겅
    actor_data_df.index = np.arange(1, len(actor_data_df) + 1)
    actor_data_df.to_csv('C:/mypython/project_test/movieapp_actor.csv', index=True, header=False, encoding='utf-8-sig')


#
# def get_actor_df():
#     actor_data_df = pd.DataFrame(columns=['actor', 'movie_id'])
#     for final_actor in final_actor_list:
#         series_obj = pd.Series(final_actor)
#         actor_data_df = actor_data_df.append(series_obj, ignore_index=True)
#
#     # 인덱스를 1부터 시작하는 방법
#     # 인덱스 값 변겅
#     actor_data_df.index = np.arange(1, len(actor_data_df) + 1)
#     actor_data_df


def get_comment_by_movie(movie_code_list):
    comment_list = []
    data = datetime.datetime.now()
    data.strftime('%Y-%m-%d %H:%M:%S.%f')

    for idx, movie_code in enumerate(movie_code_list, 1):
        comment_url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' + movie_code + '&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page='

        for i in range(1, 11):
            comment_detail_urls = comment_url + str(i)
            html = requests.get(comment_detail_urls).text
            soup = BeautifulSoup(html, 'html.parser')
            comment_tag_list = soup.select('span[id^=_filtered_ment_]')
            # print(comment_tag_list)

            for comment_tag in comment_tag_list:
                if comment_tag is None:
                    continue
                space_comment = comment_tag.text.strip()
                no_space_comment = re.sub('|  |\t|\n|\\|,|', '', space_comment)
                # print(no_space_comment)

                comment_dict = {'movie_id': idx, 'comment': no_space_comment.replace(',', ''),
                                'published_date': data.strftime('%Y-%m-%d %H:%M:%S.%f'), 'comment_score': 0,
                                'user_id': 0}
                comment_list.append(comment_dict)

                if len(comment_tag_list) != 10:
                    break;

    comment_data_df = pd.DataFrame(columns=['comment', 'published_date', 'movie_id', 'comment_score', 'user_id'])
    for comment in comment_list:
        series_obj = pd.Series(comment)
        comment_data_df = comment_data_df.append(series_obj, ignore_index=True)

    # 인덱스를 1부터 시작하는 방법
    # 인덱스 값 변겅
    comment_data_df.index = np.arange(1, len(comment_data_df) + 1)
    comment_data_df.to_csv('C:/mypython/project_test/movieapp_comment.csv', index=True, header=False,
                           encoding='utf-8-sig')


# def get_comment_df():
#     comment_data_df = pd.DataFrame(columns=['comment', 'published_date', 'movie_id', 'comment_score', 'user_id'])
#     for comment in comment_list:
#         series_obj = pd.Series(comment)
#         comment_data_df = comment_data_df.append(series_obj, ignore_index=True)
#
#     # 인덱스를 1부터 시작하는 방법
#     # 인덱스 값 변겅
#     comment_data_df.index = np.arange(1, len(comment_data_df) + 1)
#     comment_data_df

#
#
# def save_csv():
#     data_df.to_csv('C:/mypython/project_test/movieapp_movie.csv', index=True, header=False, encoding='utf-8-sig')
#     genre_data_df.to_csv('C:/mypython/project_test/movieapp_genre.csv', index=True, header=False, encoding='utf-8-sig')
#     actor_data_df.to_csv('C:/mypython/project_test/movieapp_actor.csv', index=True, header=False, encoding='utf-8-sig')
#     comment_data_df.to_csv('C:/mypython/project_test/movieapp_comment.csv', index=True, header=False,
#                            encoding='utf-8-sig')


def save_poster(movie_code_list):
    path = 'C:/mypython/recommend_movie/django_movie/movieapp/static/movieapp/img/poster/'

    for idx, i in enumerate(movie_code_list, 1):
        main_url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + i
        html = requests.get(main_url).text
        soup = BeautifulSoup(html, 'html.parser')

        images = soup.find_all('img')

        for image in images:
            image_url = image.get('src')
            filename = str(idx) + '.jpg'
            urlretrieve(image_url, path + filename)


def save_data():
    connection = pymysql.connect(host='localhost', user='young', password='1234', db='recommend_db', local_infile=True);

    try:
        with connection.cursor() as cursor:
            cursor.execute("create Table temp_movie like movieapp_movie;")
            cursor.execute("set foreign_key_checks = 0;")
            cursor.execute(
                "LOAD DATA LOCAL INFILE 'C:/mypython/test/testcomplete.csv' INTO TABLE temp_movie FIELDS TERMINATED BY ','")
            cursor.execute(
                "INSERT INTO movieapp_movie SELECT temp_movie.* FROM temp_movie where title not in (select title from movieapp_movie);")
            cursor.execute("drop table temp_movie;")
            cursor.execute("set foreign_key_checks = 1;")
            connection.commit()

    finally:
        connection.close()


def main_scraping():
    movie_list = get_movie_url
    movie_code_list = get_movie_id
    get_movie_detail(movie_list)
    get_genre_by_movie(movie_list)
    get_actor_by_movie(movie_list)
    get_comment_by_movie(movie_code_list)
    save_poster(movie_code_list)
