from rest_framework import serializers
from ..models import Expense, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = "__all__"

    def get_total_cost(self, serializer):
        return serializer.cost * serializer.quantity
