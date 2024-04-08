from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='student'),
    path('dashboard/', views.search, name='dashboard'),
    path('update/', views.update, name='update'),
    path('update2/<int:pk>/', views.update2, name='update2'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('studentview/', views.studentview, name='studentview'),
    # path('my-view/', views.my_view, name='myview'),
    
]
