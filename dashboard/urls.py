from django.urls import path
from .views import (
    dashboard_view,
    genre_detail,
    artist_detail,
    add_to_favorites,
    my_library,
    popularity_view,
    search_view,
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('genre/<str:genre_name>/', genre_detail, name='genre_detail'),
    path('artist/<str:artist_name>/', artist_detail, name='artist_detail'),
    path('add-favorite/', add_to_favorites, name='add_favorite'),
    path('library/', my_library, name='library'),
    path('popularity/', popularity_view, name='popularity'),
    path('search/', search_view, name='search'),
]