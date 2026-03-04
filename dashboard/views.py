import pandas as pd
import json
from django.shortcuts import render

# =========================
# MAIN DASHBOARD VIEW
# =========================
def dashboard_view(request):
    df = pd.read_csv('data/dataset.csv')

    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    total_tracks = int(df.shape[0])
    avg_popularity = float(round(df['popularity'].mean(), 2))
    top_genre = str(df['track_genre'].value_counts().idxmax())
    top_artist = str(df['artists'].value_counts().idxmax())

    top_genres = df['track_genre'].value_counts().head(10)
    genre_labels = [str(x) for x in top_genres.index]
    genre_values = [int(x) for x in top_genres.values]

    explicit_counts = df['explicit'].value_counts()

    explicit_labels = ['Explicit', 'Non-Explicit']
    explicit_values = [
    int(explicit_counts.get(True, 0)),
    int(explicit_counts.get(False, 0))
    ]

    context = {
        'total_tracks': total_tracks,
        'avg_popularity': avg_popularity,
        'top_genre': top_genre,
        'top_artist': top_artist,
        'genre_labels': json.dumps(genre_labels),
        'genre_values': json.dumps(genre_values),
        'explicit_labels': json.dumps(explicit_labels),
        'explicit_values': json.dumps(explicit_values),
    }

    return render(request, 'dashboard/dashboard.html', context)

from .models import FavoriteSong
from django.shortcuts import redirect

def add_to_favorites(request):
    if request.method == "POST":
        track_name = request.POST.get("track_name")
        artist = request.POST.get("artist")
        popularity = request.POST.get("popularity")

        FavoriteSong.objects.create(
            track_name=track_name,
            artist=artist,
            popularity=popularity
        )

    return redirect("/library/")

def popularity_view(request):
    df = pd.read_csv('data/dataset.csv')

    explicit_counts = df['explicit'].value_counts()

    labels = ['Explicit', 'Non-Explicit']
    values = [
        int(explicit_counts.get(True, 0)),
        int(explicit_counts.get(False, 0))
    ]

    context = {
        'labels': json.dumps(labels),
        'values': json.dumps(values)
    }

    return render(request, 'dashboard/popularity.html', context)

def search_view(request):
    query = request.GET.get('q', '')
    df = pd.read_csv('data/dataset.csv')

    results = []

    if query:
        filtered = df[
            df['track_name'].str.contains(query, case=False, na=False) |
            df['artists'].str.contains(query, case=False, na=False)
        ]

        results = filtered[['track_name', 'artists', 'popularity']].head(20).to_dict(orient='records')

    return render(request, 'dashboard/search.html', {
        'query': query,
        'results': results
    })


def artist_detail(request, artist_name):
    df = pd.read_csv('data/dataset.csv')

    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    # Filter songs by artist (contains handles multiple artists)
    artist_df = df[df['artists'].str.contains(artist_name, case=False, na=False)]

    songs = artist_df[['track_name', 'track_genre', 'popularity']].head(20)
    song_list = songs.to_dict(orient='records')

    context = {
        'artist': artist_name,
        'songs': song_list
    }

    return render(request, 'dashboard/artist_detail.html', context)


def my_library(request):
    songs = FavoriteSong.objects.all()

    return render(request, "dashboard/library.html", {
        "songs": songs
    })


# =========================
# GENRE DETAIL VIEW
# =========================
def genre_detail(request, genre_name):
    df = pd.read_csv('data/dataset.csv')

    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    genre_df = df[df['track_genre'] == genre_name]

    songs = genre_df[['track_name', 'artists', 'popularity']].head(20)
    song_list = songs.to_dict(orient='records')

    context = {
        'genre': genre_name,
        'songs': song_list
    }

    return render(request, 'dashboard/genre_detail.html', context)