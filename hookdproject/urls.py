from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
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


urlpatterns = [
    path("", include(router.urls)),
]
