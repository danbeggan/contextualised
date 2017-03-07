from django.conf.urls import url
from rest_framework import routers
from core.views import SearchViewSet

router = routers.DefaultRouter()

router.register(r'searches', SearchViewSet, base_name='searches')

urlpatterns = router.urls
