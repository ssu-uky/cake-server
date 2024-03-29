from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.TableShowView.as_view()),
    path("new/", views.NewTableView.as_view()),
    
    path("<str:pk>/", views.UserTableView.as_view()),
    path("<str:pk>/cake/", views.VisitorView.as_view(), name="visitor"), # 방문자용
    
    path("<str:pk>/<int:visitor_pk>/", views.LetterView.as_view()),
]
