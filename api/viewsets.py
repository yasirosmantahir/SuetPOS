
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.response import Response

from .serializer import CategorySerializer, SizesSerializer, GroupedSizesSerializer
from store.models import Category, Sizes, GroupedSizes

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SizesViewSet(viewsets.ModelViewSet):
    queryset = Sizes.objects.all()
    serializer_class = SizesSerializer


class GroupedSizesViewSet(viewsets.ViewSet):

    def filter_by_category(self, request):
        category_id = request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = GroupedSizes.objects.filter(category_id=category_id)
            serializer = GroupedSizesSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'category_id parameter is required'}, status=400)