import datetime
import time

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from user.models import UserProfile


class MovieCategory(models.Model):
    category = models.CharField(max_length=100, default='', verbose_name='电影类型')
    movienum = models.IntegerField(default=0, verbose_name='电影数量')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = '电影类型'
        verbose_name_plural = verbose_name


class MovieInfo(models.Model):
    RATING_RANGE = (
        MaxValueValidator(5),
        MinValueValidator(0)
    )
    moviename = models.CharField(max_length=1000, default='', verbose_name='电影名称')
    releasedate = models.DateField(default=datetime.datetime.now, verbose_name='上映年份', null=True, blank=True)
    nation = models.CharField(max_length=255, default='', verbose_name='国家', null=True, blank=True)
    directors = models.CharField(max_length=1000, default='', verbose_name='导演', null=True, blank=True)
    leadactors = models.CharField(max_length=1000, default='', verbose_name='主演', null=True, blank=True)
    editors = models.CharField(max_length=255, default='', verbose_name='编剧', null=True, blank=True)
    picture = models.CharField(max_length=1000, verbose_name='缩略图', null=True, blank=True,default='/static/images/m16.jpg')
    averating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分(0-5)', null=True, blank=True)
#     /*proccess*/
    if averating>models.FloatField(0) and averating<models.FloatField(1):
        rating = "rating05"
    elif averating>models.FloatField(1) and averating<models.FloatField(2):
        rating = "rating15"
    elif averating>models.FloatField(2) and averating<models.FloatField(3):
        rating = "rating25"
    elif averating>models.FloatField(3) and averating<models.FloatField(4):
        rating = "rating35"
    elif averating>models.FloatField(4) and averating<models.FloatField(5):
        rating = "rating45"
    else:
        rating = "rating"+str(averating)+str(0)
    
    numrating = models.IntegerField(default=0, verbose_name='评分人数', null=True, blank=True)
    description = models.TextField(default='', verbose_name='简介', null=True, blank=True)
    typelist = models.ManyToManyField(MovieCategory, verbose_name='类型')
    backpost = models.CharField(max_length=3000, verbose_name='详情页海报',null=True, blank=True ,default='/static/images/2.jpg')

    def __str__(self):
        return '%s - %s - %s - %s - %lf - %s' % (self.directors, self.moviename, self.nation, self.releasedate, self.averating, self.picture)

    class Meta:
        verbose_name = '电影信息'
        verbose_name_plural = verbose_name


class MovieSimilar(models.Model):
    item1 = models.IntegerField(default=0, verbose_name='电影id')
    item2 = models.IntegerField(default=0, verbose_name='电影id')

    # item1 = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    # item2 = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    similar = models.FloatField(default=0, verbose_name='相似度')

    def __str__(self):
        return '%d - %d - %lf' % (self.item1, self.item2, self.similar)

    class Meta:
        verbose_name = '电影相似度信息'
        verbose_name_plural = verbose_name

# mch 使用spark计算的相似度
class MovieSimilar_FromSpark(models.Model):
    item1 = models.IntegerField(default=0, verbose_name='电影id')
    item2 = models.IntegerField(default=0, verbose_name='电影id')

    similar = models.FloatField(default=0, verbose_name='相似度')

    def __str__(self):
        return '%d - %d - %lf' % (self.item1, self.item2, self.similar)

    class Meta:
        verbose_name = '电影相似度_spark计算'
        verbose_name_plural = verbose_name



