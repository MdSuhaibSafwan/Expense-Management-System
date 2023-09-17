from .serializers import CategorySerializer, ExpenseSerializer
from ..models import Category, Expense
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from .permissions import ExpensePermission
from rest_framework.response import Response


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.order_by("-date_created")
    permission_classes = [ExpensePermission, ]

    @action(detail=True, url_path="approve", methods=["GET", "POST"])
    def approve_expense(self, request, **kwargs):
        obj = self.get_object()
        if request.method == "POST":
            obj.is_approved = True
            obj.save()
            data = {
                "message": "expense approved"
            }
            return Response(data)

        serializer = ExpenseSerializer(obj)
        return Response(serializer.data)
    

    @action(detail=True, url_path="complete", methods=["GET", "POST"])
    def complete_expense(self, request, **kwargs):
        obj = self.get_object()
        if request.method == "POST":
            obj.is_completed = True
            obj.save()
            data = {
                "message": "expense completed"
            }
            return Response(data)

        serializer = ExpenseSerializer(obj)
        return Response(serializer.data)
