import xadmin
from xadmin import views
from .models import UserProfile

# 开启后台主题样式选择
class BaseSetting(object):
    enable_themes = True
    user_bootswatch = True

# 后台全局设置
class GlobalSettings(object):
    # 后台标签
    site_title = '系统管理'
    # 后台页脚
    site_footer = '电影推荐系统'
    # 菜单风格
    menu_style = "accordion"

class UserProfileAdmin(object):
    # 列表默认显示
    list_display = ['id', 'username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
                    'is_active',
                    'location', 'date_joined']
    # 搜索范围
    search_fields = ['id', 'username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
                     'is_active',
                     'location']
    # 列表过滤
    list_filter = ['id', 'username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
                   'is_active',
                   'location', 'date_joined']
    # 只读
    # readonly_fields = ['is_staff', 'is_active', 'date_joined']
    # 直接编辑
    list_editable = ['username', 'nick_name', 'first_name', 'last_name', 'gender', 'age', 'email', 'is_staff',
                     'is_active', 'location']

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
# UserProfile这个表类 在Django本身的admin注册过，比如创建超级用户
# 所以要先卸载, 再重新注册
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
# xadmin.site.register(RecBaseUserInfo, RecBaseUserInfoAdmin)
