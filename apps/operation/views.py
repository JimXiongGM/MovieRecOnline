import datetime
import random
from django.shortcuts import render
from .models import MovieInfo
# Create your views here.
from django.views import View

from operation.models import Default5Recommend, Top5Recommend,Review
from user.models import UserProfile
from movies.models import MovieSimilar, MovieInfo
from django.db.models import Q

def random_choie(in_movies):
    try:
        user_recommend_movies = random.sample(in_movies, 8)
    except ValueError:
        user_recommend_movies = in_movies
    return user_recommend_movies

def recommendForUser(request):
    """
    向用户进行top5推荐。将会显示在电影详情页右侧。
            如果用户已经登陆， 从default和top中进行混合随机推荐
            如果用户没有登陆， 从default中进行推荐
    :param request:
    :return:
    """
    user = request.user
    user_recommend_movies = None
    default_recommend_movies = Default5Recommend.objects.all()
   
    if user.is_authenticated :
        # 如果用户已经登陆
        user_recommend_movies = Top5Recommend.objects.filter(user_id=user.id)
        # defautl和recommend随机选取5个， 同时避免了recommend不足5个的情况 
        # 如果是新用户，则推荐默认的8部电影
        if user_recommend_movies.count() < 8:
            user_recommend_movies = default_recommend_movies
    else:
        # 如果用户没有登陆
        user_recommend_movies = default_recommend_movies
    return user_recommend_movies


class IndexView(View):
    def get(self, request):
        user = request.user
        userid = user.id
        user_recommend_movie = recommendForUser(request=request)
        all_movieinfo = MovieInfo.objects.all().order_by('-releasedate')
        movieinfo = all_movieinfo[1:9]
        movietitle = all_movieinfo[1]
        movielatest = all_movieinfo[9:18]
        return render(request, 'index.html', {
            "moiveinfo": movieinfo,
            "movietitle": movietitle,
            "movielatest": movielatest,
            "commend_movie": user_recommend_movie,
        })
    

    
### WeiSG

'''
# 对每个用户进行基于评价历史的推荐
'''
# re-calculate recommendations for every user
def calTop8RecommendationsForEveryUser():
    from user.models import UserProfile
    user_id_all = UserProfile.objects.values_list('id', flat = True)
    
    for current_user_id in user_id_all:
        calTop8FavorateMoviesForCurrentUser(current_user_id)


# re-calculate recommendations for current user
# 根据review表，统计每个user最喜欢的8部电影（评价数量》=8），匹配similarity表，得到8部相似度最高的电影，将推荐结果top8存进Top8Recommend表。
# 若评价数量小于8， 
def sortThird(val):
    return val[2]
    
def calTop8FavorateMoviesForCurrentUser(current_user_id):
    
    # 遍历review表，提取current user的前8个最近评价的电影。
    reviews_descend = Review.objects.all().filter(user_id=current_user_id).order_by('-reviewtime')
    
   
    # 取前8个最近的评价
    if len(reviews_descend) > 50:
        
        #top_list.append(reviews_descend[i].movie_id)
        reviews_descend = reviews_descend[0: 25]
    
    
    # 对前8个最近的评价按star排序
    
    # convert query to list
    tuple_list = []
    for review in reviews_descend:
        tuple_ = (review.user_id, review.movie_id, review.star)
        tuple_list.append(tuple_)
        
    tuple_list.sort(key = sortThird, reverse = True)
    
    if len(tuple_list) > 8:
        tuple_list = tuple_list[0: 8]
        
    # 取Movie_id
    top_list = []
    for review in tuple_list:
        top_list.append(review[1])

    # 每个movie_id对应取得similar movie 的个数
    try :
        num_every_top = (8 / len(top_list)) + 1
    except :
        num_every_top = 1
    # 对多个高分评价电影，遍历similarity表，匹配最相似的电影，存储进Top8Recommend表。

    # 8个相似推荐
    recommend_list = []
    for i in range(len(top_list)):
        recommend_queryset = MovieSimilar.objects.filter( Q(item1__in=[top_list[i]]) | Q(item2__in=[top_list[i]]) ).order_by('-similar')[: num_every_top]
        for item in recommend_queryset:

            # 只推荐8个
            if len(recommend_list) == 8:
                break

            if (item.item1 == top_list[i]) and (item.item2 not in recommend_list):
                recommend_list.append(item.item2)
            if (item.item2 == top_list[i]) and (item.item1 not in recommend_list):
                recommend_list.append(item.item1)
        # 只推荐8个
        if len(recommend_list) == 8:
            break
    
    '''
    # 新用户，个性推荐不足8个
    if len(recommend_list) < 8:
        queryset = Default5Recommend.objects.all()
        for movie in queryset:
            if len(recommend_list) < 8 and movie.movie_id not in recommend_list:
                recommend_list.append(movie.movie_id)
   '''
    
    #将当前用户的往期相似推荐删除
    Top5Recommend.objects.filter(user_id=current_user_id).delete()

    # 将recommend_list 存进 Top8Recommend
    #print ('****------*******\n recommend_list : ',recommend_list)
    for movie_id in recommend_list:
        top5recommend = Top5Recommend()
        movie = MovieInfo.objects.get(id = movie_id)
        user = UserProfile.objects.get(id = current_user_id)
        top5recommend.movie = movie
        top5recommend.user = user
        top5recommend.save()


'''
#  默认推荐部分
'''
# all-categories, latest, average-rating highest
# 前num_category个最新最高评价的各类电影，后8 - num_category个最新的各类电影

def sortAverating(val):
    return val[2]

def sortReleasedata(val):
    return val[1]

def calDefault8Recommendations(request):
    from movies.models import MovieCategory
    categories = MovieCategory.objects.all()

    recommend_list = []
    # first part
    num_category = len(categories)
    # 从评价人数最多的100部电影里，选平均评价最高的50部电影，按时间降序排序，取前4部
    most_rated = MovieInfo.objects.order_by('-numrating')[0: 100]   #list
    # convert to tuple_list
    most_rated_tuples = []
    for movie in most_rated:
        tuple_ = (movie.moviename, movie.releasedate, movie.averating)
        most_rated_tuples.append(tuple_)
    # sort by averating
    most_rated_tuples.sort(key = sortAverating, reverse = True)
    highest_rated = most_rated_tuples[0: 50]

    # sort by releasedate
    highest_rated.sort(key = sortReleasedata, reverse = True)
    highest4 = highest_rated[0: 4]
    
    for movie in highest4:
        recommend_list.append(movie[0])

    # scond part
    # 最新的4部电影，注意不要跟前四部有重复的部分
    newest_movies = MovieInfo.objects.order_by('-releasedate')[0: 16]
    for movie in newest_movies:
        if len(recommend_list) == 8:
            break
        if movie.moviename not in recommend_list:
            recommend_list.append(movie.moviename)
    
    #将当前默认推荐删除
    Default5Recommend.objects.filter().delete()

    for moviename in recommend_list:
        default5recommend = Default5Recommend()
        default5recommend.movie = MovieInfo.objects.get(moviename=moviename)
        default5recommend.save()
        

#weisg
#refresh

def refresh(request):
    #用户已经登陆，点击refresh，重新计算该用户的8个推荐；若未登录，不重新计算
    if request.user.is_authenticated :
        current_user_id = request.user.id
        #print('****------*******\n current_user_id = request.user.id')
        calTop8FavorateMoviesForCurrentUser(current_user_id)
    #refresh后，返回给用户的推荐列表，
    #已登录则返回新的8个推荐，未登录则返回新的default8个。
    calDefault8Recommendations(request)
    user_recommend_movies = recommendForUser(request)
    #movies_len = len(user_recommend_movies)
    # print ('****------*******\nrefresh - user_recommend_movies : ',user_recommend_movies)
    return render(request, 'index.html', {'commend_movie': user_recommend_movies})
    


'''
def reCal_spark(request):
    print ('\n\n\n\n\nfrom base.html reCal_spark')
    

def reCal_normal(request):
    print ('from base.html reCal_normal ')
'''

from operation import cal_similar_gry
def reCal_spark(request):
    print ('\n\n\n\n\nfrom base.html reCal_spark')
    cal_similar_gry()
    return refresh(request)

def reCal_normal(request):
    print ('from base.html reCal_normal ')

