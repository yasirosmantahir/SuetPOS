from rest_framework import serializers
from store.models import *
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class SizesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sizes
        fields = '__all__'

class GroupedSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupedSizes
        fields = ['category', 'size']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class SuppliedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliedProduct
        fields = '__all__'

class CombinedSerializer(serializers.Serializer):
    product = ProductSerializer()
    product_detail = ProductDetailSerializer()
    stock = StockSerializer()
    supplied_product = SuppliedProductSerializer()

    def create(self, validated_data):
        print(validated_data)
        product_data = validated_data.pop('product')
        product_detail_data = validated_data.pop('product_detail')
        stock_data = validated_data.pop('stock')
        supplied_product_data = validated_data.pop('supplied_product')

        product_instance = Product.objects.create(**product_data)
        product_detail_instance = ProductDetail.objects.create(product=product_instance, **product_detail_data)
        stock_instance = Stock.objects.create(product_detail=product_detail_instance, **stock_data)
        supplied_product_instance = SuppliedProduct.objects.create(product=product_detail_instance, **supplied_product_data)

        return {
            'product': product_instance,
            'product_detail': product_detail_instance,
            'stock': stock_instance,
            'supplied_product': supplied_product_instance,
        }