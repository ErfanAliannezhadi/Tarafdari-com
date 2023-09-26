from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserFollowTeamModel


class UserFollowTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        UserFollowTeamModel.objects.create(team_pk=pk, user=request.user)
        return Response({'you followed this teams'})


class UserUnfollowTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        UserFollowTeamModel.objects.get(team_pk=pk, user=request.user).delete()
        return Response({'you unfollowed this teams'})
