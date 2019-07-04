from django.urls import path
from . import views
# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<id>/', views.article_detail, name='article_detail'),
    # 删除文章
    path('article-delete/<id>/', views.article_delete, name='article_delete'),
    # 更新文章
    path('article-update/<id>/', views.article_update, name='article_update'),
]