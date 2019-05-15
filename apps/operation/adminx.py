#!/usr/bin/python
# -*- coding:utf-8 _*-

import xadmin
from operation.models import Review, Rating, Default5Recommend, Top5Recommend
from user.models import UserProfile
from user.adminx import UserProfileAdmin

class ReviewAdmin(object):
    list_display = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
    search_fields = ['id', 'user', 'movie', 'content', 'star']
    list_filter = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
    list_editable = ['user', 'movie', 'content', 'star']
    ordering = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']

class Default5RecommendAdmin(object):
    list_display = ['id', 'movie', 'redate']
    search_fields = ['id', 'movie']
    list_filter = ['id', 'movie', 'redate']
    ordering = ['id', 'movie', 'redate']

class Top5RecommendAdmin(object):
    list_display = ['id', 'user', 'movie']
    search_fields = ['id', 'userid', 'movie']
    list_filter = ['id', 'user', 'movie']
    ordering = ['id', 'user', 'movie']
    
#xadmin.site.unregister(UserProfile)
#xadmin.site.register(UserProfile, UserProfileAdmin)

xadmin.site.register(Review, ReviewAdmin)
xadmin.site.register(Default5Recommend, Default5RecommendAdmin)
xadmin.site.register(Top5Recommend, Top5RecommendAdmin)



