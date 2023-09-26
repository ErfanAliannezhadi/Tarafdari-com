from rest_framework.permissions import BasePermission
from accounts.models import BlockModel, FollowModel


class UnBlockedPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        b1 = BlockModel.objects.filter(from_user_id=request.user, to_user_id=obj.from_user)
        b2 = BlockModel.objects.filter(from_user_id=obj.from_user, to_user_id=request.user)
        return not (b1 and b2)


class PublicProfileOrFollowingPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.is_private:
            return FollowModel.objects.filter(from_user=request.user, to_user=obj.from_user).exists()
        else:
            return True
