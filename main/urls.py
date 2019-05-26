from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'post/<int:pk>/', views.post, name='post'),
    path(r'post/comment/<int:pk>/', views.comment, name='comment'),
    path(r'post/deletePost/<int:pk>', views.deletePost, name='deletePost'),
    path(r'post/editPost/<int:pk>', views.editPost, name='editPost'),
    path(r'post/deleteComment/<int:cPK>/<int:pPK>', views.deleteComment, name='deleteComment'),
    path(r'search/', views.search, name='search'),
    path(r'gallery/', views.gallery, name='gallery'),
    path(r'documents/', views.documents, name='documents'),
    path(r'admin/', views.admin, name='admin'),
    path(r'adminLogin/', views.adminLogin, name='adminLogin'),
    path(r'addPicture/', views.addPicture, name='addPicture'),
    path(r'gallery/deletePicture/<int:pk>', views.deletePicture, name='deletePicture'),
    path(r'adminLogout/', views.adminLogout, name='adminLogout'),
    path(r'addPost/', views.addPost, name='addPost'),
    path(r'applyPostChanges/<int:pk>', views.applyPostChanges, name='applyPostChanges'),
    path(r'changeMe/', views.changeMe, name='changeMe'),
]
