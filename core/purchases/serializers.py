#rest framework
from rest_framework import *
from rest_framework.serializers import *

#local
from core.models import *
from core.items.serializers import *

class PurchaseSerializer(ModelSerializer):
	class Meta:
		model = Purchase
		fields = "__all__"
		read_only_fields = ['createdDate','lastModifiedDate','isDelete']

class RespPurchaseSerializer(ModelSerializer):
	itemId = ItemSerializer()
	totalPrice = serializers.SerializerMethodField(read_only=True)

	def get_totalPrice(self, obj):
		return obj.itemId.itemPrice*obj.purchaseQuantity

	class Meta:
		model = Purchase
		fields = "__all__"
		read_only_fields = ['createdDate','lastModifiedDate','isDelete']