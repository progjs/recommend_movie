import pymysql
from krwordrank.hangle import normalize
from krwordrank.word import KRWordRank
# % matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from palettable.colorbrewer.qualitative import Dark2_8
import random
from wordcloud import WordCloud

icon = Image.open("movieapp/update_data/cloud2.png")
mask = Image.new("RGB", icon.size, (255, 255, 255))
mask.paste(icon, icon)
mask = np.array(mask)
font_path = "movieapp/update_data/BMJUA_ttf.ttf"

exclude_set = {'영화', '평점' '많은', '많이', '너무', '정말', '진짜', '그리고', '가장', '제일', '이런', '하는', '엄청', '조금', '완전', '계속', '할때',
               '있어', '있는', '있었던', '어떤', '이런', '않고', '보다', '그래도', '봤는데', '보는', '어느', '하고', '하지만', '이렇게', '있다', '있어서',
               '이렇게', '봤습니다', '봤음', '이게', '아니라', \
               '대한', '한다', '하지', '동안', '것이', '보고', '있고', '얼마나', '봐도', '이거', '그냥', '것을', '특히', '이거', '재밌', '좋은', '내가',
               '보면', '나를', '좋고', '아니', '지금', '무서', '봐야', '봤다', '봤으니', '봤다는데', '합니다', '않은', '했던', '봤어요', '별점', '아주'}


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Dark2_8.colors[random.randint(0, 7)])


def print_set():
    print(exclude_set)


# 1
def load_movie():
    # db = pymysql.connect(host='localhost', port=3306, db='project_db', user='python', passwd='python', charset='utf8')
    db = pymysql.connect(host='localhost', port=3306, db='recommend_db', user='young', passwd='1234', charset='utf8')
    query = 'select distinct movie_id, count(id) from movieapp_comment group by movie_id'

    try:
        # select, update
        with db.cursor() as cursor:
            cursor.execute(query)
            movie_id_list = cursor.fetchall()  # cursor()의 값을 가져온다.
    finally:
        db.close()

    movie_id_list = [m[0] for m in movie_id_list]
    print(len(movie_id_list))
    return movie_id_list


# 2 댓글 조회
def load_comments(movie_id_list):
    ### 모든 영화의 댓글 저장
    comments_list = []

    # 모든 댓글 영화id별로 database에서 호출
    for idx in movie_id_list[:]:
        # db = pymysql.connect(host='localhost', port=3306, db='project_db', user='python', passwd='python',
        #                      charset='utf8')
        db = pymysql.connect(host='localhost', port=3306, db='recommend_db', user='young', passwd='1234',
                             charset='utf8')

        query = 'select comment from movieapp_comment where movie_id={}'.format(idx)

        try:
            # select, update
            with db.cursor() as cursor:
                cursor.execute(query)
                result_list = cursor.fetchall()  # cursor()의 값을 가져온다.
        finally:
            db.close()

        texts = [row[0] for row in result_list]
        # 영어, 한글, 숫자만
        texts = [normalize(text, english=True, number=True) for text in texts]
        comments_list.append(texts)
    print('comments_list 개수: ', len(comments_list))
    return comments_list


def make_wordcloud(movie_id_list, comments_list):
    ### 단어 빈도수 keyword dict로 만들고 워드클라우드 생성 후 저장
    for idx, texts in enumerate(comments_list):
        wordrank_extractor = KRWordRank(
            min_count=2,  # 단어의 최소 출현 빈도수 (그래프 생성 시)
            max_length=6,  # 단어의 최대 길이
            verbose=True
        )

        beta = 0.85  # PageRank의 decaying factor beta
        max_iter = 6
        keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
        keywords = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:min(len(keywords.keys()), 610)])

        # 필요없는 단어 삭제
        key_set = set(keywords.keys())
        for w in exclude_set & key_set:
            keywords.pop(w)

        wordcloud = WordCloud(
            font_path=font_path,
            width=900,
            height=300,
            background_color="white",
            mask=mask
        )

        wordcloud = wordcloud.generate_from_frequencies(keywords)
        wordcloud.recolor(color_func=color_func, random_state=1)

        #     plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        # plt.show()
        wordcloud.to_file("movieapp/static/movieapp/img/wordcloud/{}.png".format(movie_id_list[idx]))
        print('{}번 완료'.format(movie_id_list[idx]))


def main_cloud():
    movie_id_list = load_movie()
    comments_list = load_comments(movie_id_list)
    make_wordcloud(movie_id_list, comments_list)
