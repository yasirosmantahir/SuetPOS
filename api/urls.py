from django.urls import  include, path
from django.views.decorators.csrf import csrf_exempt

from .views import *
#
from rest_framework.routers import DefaultRouter
from .viewsets import CategoryViewSet, SizesViewSet, GroupedSizesViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'sizes', SizesViewSet)
#router.register(r'grouped-sizes', GroupedSizesViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('grouped-sizes/filter_by_category/', GroupedSizesViewSet.as_view({'get': 'filter_by_category'})),
    path('create/', CombinedCreateView.as_view(), name='combined-create'),
]
