import schedule
import time
import datetime
import requests
from bs4 import BeautifulSoup
import bs4
from urllib.parse import urljoin
import re
import numpy as np
import pandas as pd
import pymysql



def scraping():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    date = yesterday.strftime('%Y%m%d')

    main_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + date

    movie_list = []
    # for i in [1, 2, 4, 5, 6, 7, 11, 13, 15, 16, 18, 19]:

    for page_num in [1, 2]:
        movie_genre_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + str(date) + '&tg=' + str(
            1) + '&page=' + str(page_num)
        html = requests.get(movie_genre_url).text
        soup = BeautifulSoup(html, 'html.parser')

        a_tag_list = soup.select('div .tit5 a[href*="basic.nhn"]')

        for idx, a_tag in enumerate(a_tag_list, 1):
            if idx > 50:
                break
            movie_dict = {}
            title = a_tag.text.strip()
            link = urljoin(main_url, a_tag['href'])

            movie_dict['genre_code'] = 1
            movie_dict['id'] = idx
            movie_dict['title'] = title
            movie_dict['url'] = link
            # scorre_url 은 평점을 스크래핑하기 위한 페이지
            movie_dict['score_url'] = link.replace('basic', 'pointWriteFormList')
            movie_list.append(movie_dict)
            # print(idx, title, link)

    print(len(movie_list))
    movie_list

    # In[64]:

    movie_code_list = []
    # for i in [1, 2, 4, 5, 6, 7, 11, 13, 15, 16, 18, 19]:
    for page_num in [1, 2]:
        movie_genre_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=' + str(date) + '&tg=' + str(
            1) + '&page=' + str(page_num)
        html = requests.get(movie_genre_url).text
        soup = BeautifulSoup(html, 'html.parser')

        a_tag_list = soup.select('div .tit5 a[href*="basic.nhn"]')

        for idx, a_tag in enumerate(a_tag_list, 1):
            if idx > 50:
                break
            movie_code = re.findall("\d+", a_tag['href'])

            for movie in movie_code:
                movie_code_list.append(movie)

    print(len(movie_code_list))
    movie_code_list

    # In[65]:

    movie_info_lists = []

    for movie in movie_list:
        html = requests.get(movie['url']).text
        soup = BeautifulSoup(html, 'html.parser')

        movie_info_dict = {}

        # 타이틀
        title = soup.select_one('h3.h_movie a[href*="basic.nhn"]')
        if title == None:
            movie_info_dict['title'] = None
        else:
            movie_info_dict['title'] = title.text.strip().replace(',', '')

        # 네티즌 평점
        score = soup.select_one('div.netizen_score .star_score em')
        if score == None:
            movie_info_dict['score'] = None
        else:
            movie_info_dict['score'] = score.text.strip()

        # 개봉국가
        nation = soup.select_one('dl.info_spec span a[href*="nation"]')
        if nation == None:
            movie_info_dict['nation'] = None
        else:
            movie_info_dict['nation'] = nation.text.strip()

        # 감독
        director = soup.select_one('dl.info_spec a[href*="code"]')
        if director == None:
            movie_info_dict['director'] = None
        else:
            movie_info_dict['director'] = director.text.strip()

        # 누적관객수
        audience = soup.select_one('p.count')
        if audience == None:
            movie_info_dict['audience'] = None
        else:
            movie_info_dict['audience'] = re.sub(r"(명)\([^()]*\)", "", audience.text.strip()).replace(',', '')

        # 관람객 평점 건수
        comment_count = soup.select_one('div.netizen_score .user_count em')
        if comment_count == None:
            movie_info_dict['comment_count'] = None
        else:
            movie_info_dict['comment_count'] = comment_count.text.strip().replace(',', '')

        # 개봉일자
        release_year = soup.select_one('dl.info_spec a[href*="open"]')
        if release_year == None:
            movie_info_dict['release_year'] = None
        else:
            movie_info_dict['release_year'] = release_year.text.strip()

        # 평점
        movie_info_dict['score_sum'] = 0

        # 줄거리
        plot = soup.select_one('.con_tx')
        if plot == None:
            movie_info_dict['plot'] = None
        else:
            movie_plot = " ".join(re.sub('|  |\t|\r|\n|', '', plot.text).split())
            movie_info_dict['plot'] = movie_plot.replace(',', "")

        movie_info_lists.append(movie_info_dict)

    print(len(movie_info_lists))
    print(movie_info_lists)

    # ## 2.1. movieapp_movie 테이블

    # In[67]:

    data_df = pd.DataFrame(
        columns=['title', 'score', 'nation', 'director', 'audience', 'plot', 'score_sum', 'comment_count',
                 'release_year'])

    for data in movie_info_lists:
        series_obj = pd.Series(data)
        data_df = data_df.append(series_obj, ignore_index=True)

    # 인덱스를 1부터 시작하는 방법
    data_df.index = np.arange(1, len(data_df) + 1)

    data_df
    data_df.to_csv('C:/mypython/test/testcomplete.csv', index=True, header=False, encoding='utf-8-sig')

    save_data()


def save_data():
    connection = pymysql.connect(host='localhost', user='young', password='1234', db='recommend_db', local_infile=True);

    try:
        with connection.cursor() as cursor:
            cursor.execute("create Table temp_movie like movieapp_movie;")
            cursor.execute("set foreign_key_checks = 0;")
            cursor.execute("LOAD DATA LOCAL INFILE 'C:/mypython/test/testcomplete.csv' INTO TABLE temp_movie FIELDS TERMINATED BY ','")
            cursor.execute("INSERT INTO movieapp_movie SELECT temp_movie.* FROM temp_movie where title not in (select title from movieapp_movie);")
            cursor.execute("drop table temp_movie;")
            cursor.execute("set foreign_key_checks = 1;")
            connection.commit()

    finally:
        connection.close()


schedule.every(1).minutes.do(scraping)


while True:
    schedule.run_pending()
    time.sleep(1)
