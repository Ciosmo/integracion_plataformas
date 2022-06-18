from base.api import GeneralListAPIView
from products.api.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer


class MeasureUnitListAPIView(GeneralListAPIView):
    serializer_class = MeasureUnitSerializer




class CategoryProductListAPIView(GeneralListAPIView):
    serializer_class = CategoryProductSerializer


     