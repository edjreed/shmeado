from django.urls import path
from . import views

urlpatterns = [
    # Stats
    path("player/stats/<str:name>/", views.stats, name="stats"),
    path(
        "player/stats/<str:name>/<str:game>/<str:tab>/",
        views.stats,
        name="stats-custom",
    ),
    # Internal APIs
    path("player/online/<str:uuid>/", views.online, name="online"),
    path("player/guild/<str:uuid>/", views.guild, name="guild"),
    path("player/recent/<str:uuid>/", views.recent, name="recent"),
    # Miscellaneous
    path("about/", views.about, name="about"),
    path("", views.home, name="home"),
]
