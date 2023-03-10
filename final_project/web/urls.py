from django.urls import path, include

from final_project.web.views import IndexView, BookingAgencyView, ArtistsListView, ArtistsDetailView, \
    ArtistsAddView, ArtistsEditView, ArtistsDeleteView, LabelListView, LabelAddView, LabelDetailView, LabelEditView, \
    LabelDeleteView, StylesListView, GenresListView, ExploreView, SignInView, SignUpView, SignOutView, \
    VinylBuyView, VinylSellView, ProfileView, VinylDetailsView, TestView, BlogView, \
    ArticleDetailView, StylesDetailView, GenresDetailView, VinylEditView, cart, checkout, updateItem, \
    processOrder, vinylstorefbview

urlpatterns = (
    # Home URL
    path('', IndexView.as_view(), name='index'),
    path('sign-up/', SignUpView.as_view(), name='sign up'),
    path('sign-in/', SignInView.as_view(), name='sign in'),
    path('sign-out/', SignOutView.as_view(), name='sign out'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', updateItem, name='update item'),
    path('process_order/', processOrder, name='process order'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('articles/<int:pk>', ArticleDetailView.as_view(), name='article page'),

    # Vinyls URLs
    path('vinyls/', include([
        # path('', VinylStoreView.as_view(), name='vinyls'),
        path('', vinylstorefbview, name='vinyls'),
        path('buy/', VinylBuyView.as_view(), name='buy'),
        path('sell/', VinylSellView.as_view(), name='sell'),
        path('details/<int:pk>', VinylDetailsView.as_view(), name='vinyl page'),
        path('edit/<int:pk>', VinylEditView.as_view(), name='vinyl edit'),
    ])),
    # Explore
    path('explore/', include([
        # Main
        path('', ExploreView.as_view(), name='explore'),
        # Genres
        path('genres/', include([
            path('', GenresListView.as_view, name='genres'),
            path('<str:slug>', GenresDetailView.as_view(), name='genre page'),
        ])),
        # Styles
        path('styles/', include([
            path('', StylesListView.as_view, name='styles'),
            path('<str:slug>', StylesDetailView.as_view(), name='style page'),
        ])),
    ])),
    # Booking agency URLs
    path('booking-agency/', BookingAgencyView.as_view(), name='booking agency'),
    # Artist URLs
    path('artists/', include([
        path('', ArtistsListView.as_view(), name='artists'),
        path('add/', ArtistsAddView.as_view(), name='artist add'),
        path('edit/<slug:slug>/', ArtistsEditView.as_view(), name='artist edit'),
        path('delete/<slug:slug>/', ArtistsDeleteView.as_view(), name='artist edit'),
        path('<str:slug>/', ArtistsDetailView.as_view(), name='artist page')])),

    # Labels URLs
    path('labels/', include([
        path('', LabelListView.as_view(), name='labels'),
        path('add/', LabelAddView.as_view(), name='label add'),
        path('edit/<slug:slug>/', LabelEditView.as_view(), name='label edit'),
        path('delete/<slug:slug>/', LabelDeleteView.as_view(), name='label edit'),
        path('<slug:slug>/', LabelDetailView.as_view(), name='label page')])),

    path('test/', TestView.as_view(), name='test')

)

from .signals import *
