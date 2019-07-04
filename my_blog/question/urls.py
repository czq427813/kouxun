from django.urls import path
from . import views
# 正在部署的应用的名称
app_name = 'question'

urlpatterns = [
    path('question-list/', views.question_list, name='question_list'),
    path('question-detail/<id>/', views.question_detail, name='question_detail'),
    # 删除文章
    path('question-delete/<id>/', views.question_delete, name='question_delete'),
    # 更新文章
    path('question-update/<id>/', views.question_update, name='question_update'),
]