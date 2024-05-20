from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from hookdapi.models import *
from hookdapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"rtsproducts", RTSProductsView, "rtsproducts")
router.register(r"cusproducts", CusProductView, "cusproducts")
# router.register(r"cusrequests", CusRequestView, "cusrequests")
router.register(r"colors", ColorView, "colors")
router.register(r"eyes", EyesView, "eyes")
router.register(r"orders", OrdersView, "order")
router.register(r"category", CategoriesView, "category")
router.register(r"cartitem", CartItem, "cartitem")
router.register(r"customer", CustomersView, "customer")
router.register(r"cart", CartView, "cart")
router.register(r"payments", Payments, "payments")
router.register(r"cusrequests", CusRequestView, "cusrequests")


urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
