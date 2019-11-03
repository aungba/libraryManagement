from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('main', views.main, name='main'),
    path('book',views.book_add, name='book'),
    path('',views.book_list, name='bookList'),
    path('edit/<int:pk>', views.book_edit,name='book_view'),
    path('delete/<int:pk>', views.book_delete.as_view(),name='book_delete'),
    path('borrow/<int:pk>', views.book_borrow, name='borrow'),
    path('test', views.bookList.as_view(), name='bookListView'),
    path('return/<int:bookId>', views.bookReturn.as_view(), name='bookReturn'),
    path('category', views.categoryList, name='categoryList'),
    path('category/<int:pk>', views.category_edit, name='categoryEdit'),
    path('add/category', views.categoryCreateView.as_view(), name="categoryCreate"),
    path('check/<username>/', views.check_user.as_view(), name='check_user'),
    path('logout', views.logout_view, name='logout')
]