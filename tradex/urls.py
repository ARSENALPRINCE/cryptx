from django.urls import path
from django.contrib.auth.models import User
from .views import homePage,getspecificAsset,updateSpecificAsset,signupview,aboutPage,contactPage,loginview,walletView,logoutview,createWalletView,fundWalletview,buyAssetview,offerview

urlpatterns = [
    path('',homePage,name='tradex-home-page'),
    path('about/',aboutPage,name='tradex-home-page'),
    path('contact/',contactPage,name='tradex-home-page'),
    path('asset/',getspecificAsset,name='tradex-get-specific-asset'),
    path('asset-update/',updateSpecificAsset, name='tradex-update-specific-asset'),
    path('signup/',signupview, name='tradex-signup-page'),
    path('login/',loginview,name="tradex-login-page"),
    path('wallet/',walletView, name="tradex-wallet-page"),
    path('wallet/create',createWalletView, name='tradex-create-wallet'),
    path('fund/',fundWalletview, name='tradex-fund-wallet'),
    path('logout/',logoutview, name='tradex-logout-page'),
    path('buy-Asset/<int:pk>',buyAssetview, name='buy-asset-page'),
    path('sell-asset/<int:pk>',offerview, name ='tradex-sell-asset-page'),
    path('escrow')
 ]
#127.0.0:1:8000/tradex/home