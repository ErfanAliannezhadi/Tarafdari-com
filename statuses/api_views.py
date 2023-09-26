from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import BlockModel
from .models import StatusModel, StatusCommentModel, StatusLikeModel
from .serializers import StatusSerializer, StatusCommentSerializer, StatusLikeSerializer
from .permissions import UnBlockedPermission, PublicProfileOrFollowingPermission


class UserStatusesListView(APIView):
    permission_classes = [IsAuthenticated, UnBlockedPermission, PublicProfileOrFollowingPermission]

    def get(self, request, pk):
        statuses = StatusModel.objects.filter(from_user_id=pk, to_user_id=pk)
        self.check_object_permissions(request, statuses)
        ser_data = StatusSerializer(instance=statuses, many=True)
        return Response(ser_data.data)


class UserDeliverMessageListView(APIView):
    permission_classes = [IsAuthenticated, UnBlockedPermission, PublicProfileOrFollowingPermission]

    def get(self, request, pk):
        statuses = StatusModel.objects.filter(from_user_id=pk)
        self.check_object_permissions(request, statuses)
        ser_data = StatusSerializer(instance=statuses, many=True)
        return Response(ser_data.data)


class UserReceiverMessageListView(APIView):
    permission_classes = [IsAuthenticated, UnBlockedPermission, PublicProfileOrFollowingPermission]

    def get(self, request, pk):
        statuses = StatusModel.objects.filter(to_user_id=pk)
        self.check_object_permissions(request, statuses)
        ser_data = StatusSerializer(instance=statuses, many=True)
        return Response(ser_data.data)


class CreateStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['from_user'] = request.user
        if BlockModel.objects.filter(from_user=request.data['from_user'], to_user=request.data['to_user']).exists():
            return Response({'message': 'you blocked this user, you cant send any message to him'})
        if BlockModel.objects.filter(from_user=request.data['to_user'], to_user=request.data['from_user']).exists():
            return Response({'message': 'This user blocked you, you cant send any message to him'})

        ser_data = StatusSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class UpdateStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        status = StatusModel.objects.get(pk=pk)
        if status.from_user != request.user:
            return Response({'message': 'this status doesnt belong to you'})
        ser_data = StatusSerializer(instance=status, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class DeleteStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        status = StatusModel.objects.get(pk=pk)
        if status.from_user != request.user:
            return Response({'message': 'this status doesnt belong to you'})
        status.delete()
        return Response({'message': 'status is deleted'})


class RetrieveStatusView(APIView):
    permission_classes = [IsAuthenticated, UnBlockedPermission, PublicProfileOrFollowingPermission]

    def get(self, request, pk):
        status = StatusModel.objects.get(pk=pk)
        self.check_object_permissions(request, status)
        return Response(StatusSerializer(instance=status))


class StatusCommentsListView(APIView):
    permission_classes = [IsAuthenticated, UnBlockedPermission, PublicProfileOrFollowingPermission]

    def get(self, request, pk):
        status = StatusModel.objects.get(pk=pk)
        comments = StatusCommentModel.objects.filter(status=status)
        self.check_object_permissions(request, status)
        return Response(StatusCommentSerializer(instance=comments, many=True))


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated, UnBlockedPermission, PublicProfileOrFollowingPermission]

    def post(self, request, pk):
        status = StatusModel.objects.get(pk=pk)
        self.check_object_permissions(request, status)
        request.data['status'] = status
        ser_data = StatusCommentSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        comment = StatusCommentModel.objects.get(pk=pk)
        if comment.user != request.user:
            return Response({'message': 'this comment doesnt belong to you'})
        comment.delete()
        return Response({'message': 'the comment is deleted'})


class StatusLikeView(APIView):
    permission_classes = [IsAuthenticated, UnBlockedPermission, PublicProfileOrFollowingPermission]

    def get(self, request, pk):
        status = StatusModel.objects.get(pk=pk)
        self.check_object_permissions(request, status)
        StatusLikeModel.objects.create(user=request.user, status=status)
        return Response({'message': 'you liked this status'})


class StatusUnlikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        StatusLikeModel.objects.get(user=request.user, status_id=pk).delete()
        return Response({'message': 'you unliked this status'})
