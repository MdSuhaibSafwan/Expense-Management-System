from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet

router = DefaultRouter()

router.register("expense", ExpenseViewSet, basename="expense")
router.register("category", CategoryViewSet, basename="category")

urlpatterns = [

] + router.urls
