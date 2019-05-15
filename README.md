# MovieRecOnline

本小组项目实现在线电影推荐系统的前后端开发，使用Django2.2+MySQL+spark。其中MySQL部分支持在线计算，spark支持离线计算。基于[MovieSizer](https://github.com/NanceEvan/MovieSizer)，本项目精简美化，实现了新的功能。


## 小组成员

**感谢每位组员的辛勤付出！**

@[CaoH](https://github.com/Jacylike)  @[CuiPZ](https://github.com/cuipz)  @[GongRY](https://github.com/GRY123456)  @[LinS](https://github.com/linsen-yeguiren)  @[LiuYL](https://github.com/lyl0724)  @[MeiCH](https://github.com/meichuhe)  @[MengSM](#)  @[TongQ](https://github.com/TerrenceTong)  @[WeiSG](#) 

## 目录

- [安装指南](#1)
- [数据导入](#2)
- [算法说明](#3)

## <p id=1>安装指南

### 环境配置

本项目基于ubuntu18.04运行。

如下安装好Django2.0+和最新的xadmin
```bash
pip3 install --upgrade pip;
pip3 install git+git://github.com/sshwsfc/xadmin.git@django2;
pip3 install django;
pip3 install Pillow;
pip3 show xadmin;
pip3 show django;
```

还需要安装MySQL8.0+，具体过程可参考[MySQL8.0环境搭建](https://github.com/JimXiongGM/BigDataProject/blob/master/Documentations/MySql_8.0.md)

### 项目清理

Django框架需要通过migrate命令自动构建数据库，但是会生成相应的缓存文件，这里清空所有的缓存文件并保留应有的结构。

```bash
cd MovieRecOnline;
rm -r ./apps/movies/__pycache__
rm -r ./apps/operation/__pycache__
rm -r ./MovieSizer/__pycache__

rm -r ./apps/movies/migrations/*
rm -r ./apps/user/migrations/*;
rm -r ./apps/operation/migrations/*;

touch ./apps/movies/migrations/__init__.py
touch ./apps/user/migrations/__init__.py
touch ./apps/operation/migrations/__init__.py
```

### 配置MySQL数据库

首先修改`MovieRecOnline/MovieSizer/settings.py`文件的mysql数据库连接：

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MovieSizer',
        'USER': 'root',
        'PASSWORD': '你的密码',
        'HOST': 'master',
        'PORT': '3306'
    }
}
```

然后在MySQL shell中建立数据库`MovieSizer`

`mysql -u root -p`
```sql
use mysql;
create database MovieSizer;
```

### 启动项目

执行`migrate`自动建表：
```bash
cd MovieRecOnline;
chmod +x manage.py;
python3 manage.py makemigrations;
python3 manage.py migrate;
```

输出如下
```
Migrations for 'operation':
  MovieSizer-final/apps/operation/migrations/0001_initial.py
    - Create model Top5Recommend_2
    - Create model Top5Recommend
    - Create model Review
    - Create model Rating
    - Create model Default5Recommend
.
.
.
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, movies, operation, sessions, user, xadmin
Running migrations:
  Applying operation.0001_initial... OK
.
.
.
```

最后创建管理员用户
```bash
python3 manage.py createsuperuser
```

启动项目
```bash
python3 manage.py runserver 0.0.0.0:8000
```
成功则输出如下
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 15, 2019 - 00:47:32
Django version 2.2, using settings 'MovieSizer.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
[15/May/2019 00:47:37] "GET /movieinfo/7641 HTTP/1.1" 200 47740
^C
```

## <p id=2>数据导入

本项目提供爬取的猫眼电影网站数据作为DEMO，共1000条，字段对应`movies_movieinfo`表，[点击这里](./movies_movieinfo_DEMO.sql)可以看到该SQL文件，复制到MySQL shell中即可插入数据。

接着使用我们编写的`cal_similar_gry.py`文件计算电影相似度，存入`movies_moviesimilar`表。注意需要使用`pip3 install distance`安装依赖，并将MySQL账号密码的参数设置正确。

到这里我们已经计算好了`movies_movieinfo`表和`movies_moviesimilar`表，主页已经能显示。

## <p id=3>算法说明