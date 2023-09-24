from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserModel, FollowModel, FollowRequestModel, BlockModel, EmojiPackageModel
from .serializers import UserSerializer, AuthTokenSerializer, EmojiPackageSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class RegisterUserUserView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class ListUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ser_data = UserSerializer(instance=UserModel.objects.all(), many=True)
        return Response(ser_data.data)


class UserDetailsView(APIView):
    def get(self, request, pk):
        ser_data = UserSerializer(instance=UserModel.objects.get(pk=pk))
        return Response(ser_data.data)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = UserSerializer(instance=request.user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response({'message': 'profile is updated'})
        return Response(ser_data.errors)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.delete()
        return Response({'message': 'user is deleted'})


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = UserModel.objects.get(pk=pk)
        if BlockModel.objects.filter(from_user=request.user, to_user=user).exists():
            return Response({'message': 'you cant follow this user, you have blocked this user.'})
        if BlockModel.objects.filter(from_user=user, to_user=request.user).exists():
            return Response({'message': 'you cant follow this user, this user have blocked you.'})
        if user.is_private:
            FollowRequestModel.objects.get_or_create(from_user=request.user, to_user=user)
            return Response({'message': ' you have follow requested this user'})
        FollowModel.objects.get_or_create(from_user=request.user, to_user=user)
        return Response({'message': ' you have followed this user'})


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = UserModel.objects.get(pk=pk)
        if FollowModel.objects.filter(from_user=request.user, to_user=user).exists():
            FollowModel.objects.get(from_user=request.user, to_user=user).delete()
            return Response({'message': 'you unfollowed the user'})
        if FollowRequestModel.objects.filter(from_user=request.user, to_user=user).exists():
            FollowRequestModel.objects.get(from_user=request.user, to_user=user).delete()
            return Response({'message': 'you unfollowed request the user'})
        return Response({'message': 'there is no follow '})


class DecisionFollowRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        decision = request.GET['decision']
        fr = FollowRequestModel.objects.get(pk=pk)
        if fr.to_user != request.user:
            return Response({'message': 'this item doesnt belong to you'})
        match decision:
            case 'accept':
                fr.accept()
                return Response({'message': 'follow request is accepted'})
            case 'reject':
                fr.reject()
                return Response({'message': 'follow request is rejected'})


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        BlockModel.objects.create(from_user=request.user, to_user_id=pk)
        return Response({'message': 'you blocked this user'})


class UnblockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        BlockModel.objects.get(from_user=request.user, to_user_id=pk).delete()
        return Response({'message': 'you unblocked this user'})


class UserEmojisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        emoji_package = EmojiPackageModel.objects.get(from_user=request.user, to_user_id=pk)
        ser_data = EmojiPackageSerializer(instance=emoji_package, data=request.GET, partial=True)
        ser_data.save()
        return Response({'message': 'emojis are updated now'})
