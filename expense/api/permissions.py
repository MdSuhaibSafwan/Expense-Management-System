from rest_framework.permissions import BasePermission, SAFE_METHODS


class ExpensePermission(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if view.action == "complete_expense":
            return self.expense_complete_object_permission(request, view, obj)

        if view.action == "approve_expense":
            return self.expense_approve_object_permission(request, view, obj)

        return True
    
    def expense_complete_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return (request.user.is_maker) and (obj.is_approved)

    def expense_approve_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.is_checker