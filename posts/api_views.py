from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, PostEmojiSerializer, CommentEmojiSerializer, PostCommentSerializer
from .models import PostModel, PostEmojiModel, PostCommentModel, CommentEmojiModel


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ser_data = PostSerializer(instance=PostModel.objects.all(), many=True)
        return Response(ser_data.data)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        ser_data = PostSerializer(instance=PostModel.objects.get(pk=pk))
        return Response(ser_data.data)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['user'] = request.user
        ser_data = PostSerializer(data=data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = PostModel.objects.get(pk=pk)
        if post.auther == request.user:
            ser_data = PostSerializer(instance=post, data=request.data, partial=True)
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data)
            return Response(ser_data.errors)
        return Response({'message': 'this post doesnt belong to you.'})


class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = PostModel.objects.get(pk=pk)
        if post.auther == request.user:
            post.delete()
            return Response({'message': 'the post is deleted'})
        return Response({'message': 'this post doesnt belong to you'})


class PostEmojiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pe = PostEmojiModel.objects.get(post_id=pk, user=request.user)
        ser_data = PostEmojiSerializer(instance=pe, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class PostCommentsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        comments = PostCommentModel.objects.filter(post_id=pk)
        return Response(PostCommentSerializer(instance=comments, many=True).data)


class CommentRepliesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        replies = PostCommentModel.objects.filter(is_reply=True, reply_id=pk)
        return Response(PostCommentSerializer(instance=replies, many=True).data)


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = PostCommentSerializer(data=request.data.update({'user': request.user}))
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class UpdateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        comment = PostCommentModel.objects.get(pk=pk)
        if comment.user != request.user:
            return Response({'message': 'this comment doesnt belong to you'})
        ser_data = PostCommentSerializer(instance=comment, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data)
        return Response(ser_data.errors)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        comment = PostCommentModel.objects.get(pk=pk)
        if comment.user != request.user:
            return Response({'message': 'this comment doesnt belong to you'})
        comment.delete()
        return Response({'message': 'comment is deleted'})


class CommentEmojisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        cep = CommentEmojiModel.objects.get(pk=pk)
        ser_data = CommentEmojiSerializer(instance=cep, data=request.GET, partial=True)
        if ser_data.is_valid():
            return Response(ser_data.data)
        return Response(ser_data.errors)
