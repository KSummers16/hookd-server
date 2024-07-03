from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.urls import re_path
from hookdapi.models import *
from hookdapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"rtsproducts", RTSProductsView, "rtsproducts")
router.register(r"cusproducts", CusProductView, "cusproducts")
router.register(r"colors", ColorView, "colors")
router.register(r"eyes", EyesView, "eyes")
router.register(r"orders", OrdersView, "orders")
router.register(r"category", CategoriesView, "category")
router.register(r"cartitem", CartItem, "cartitem")
router.register(r"customer", CustomersView, "customer")
router.register(r"cart", CartView, "cart")
# router.register(r"payments", create_payment, "payments")
router.register(r"cusrequests", CusRequestView, "cusrequests")


urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r"^.*", TemplateView.as_view(template_name="index.html"), name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
