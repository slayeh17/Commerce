from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create"),
    path("search_by_core", views.core_list, name="core_list"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist_listings", views.watchlist_listings, name="watchlist_listings"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("closed", views.closed, name="closed"),
]
