from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, View
from .models import PostModel, PostCommentModel, CommentEmojiModel, PostEmojiModel
from .forms import PostCommentForm, CreatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'posts/post_detail.html'
    model = PostModel
    pk_url_kwarg = 'pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = context['post'].comments.filter(is_reply=False)
        context['comment_create_form'] = PostCommentForm()
        return context


class CreateCommentView(LoginRequiredMixin, FormView):
    form_class = PostCommentForm

    def form_valid(self, form):
        PostCommentModel.objects.create(user=self.request.user, content=form.cleaned_data['content'],
                                        post_id=self.kwargs['pk'], reply=None, is_reply=False)
        return redirect('posts:post_detail', self.kwargs['pk'])


class PostEmojiPackageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        emoji_package = PostEmojiModel.objects.get(user=request.user, post_id=kwargs['pk'])
        emoji_request = request.GET.get('emoji')
        match emoji_request:
            case 'like':
                emoji_package.reverse_like()
            case 'dislike':
                emoji_package.reverse_dislike()
            case 'heart':
                emoji_package.reverse_heart()
            case _:
                pass
        return redirect('posts:post_detail', pk=kwargs['pk'])


class CommentEmojiPackageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comment = PostCommentModel.objects.get(pk=kwargs['pk'])
        emoji_package = CommentEmojiModel.objects.get(user=request.user, comment=comment)
        emoji_request = request.GET.get('emoji')
        match emoji_request:
            case 'like':
                emoji_package.reverse_like()
            case 'dislike':
                emoji_package.reverse_dislike()
            case _:
                pass
        return redirect('posts:post_detail', pk=comment.post.pk)


class CommentReplyView(LoginRequiredMixin, FormView):
    template_name = 'posts/comment_reply.html'
    form_class = PostCommentForm

    def form_valid(self, form):
        comment = PostCommentModel.objects.get(pk=self.kwargs['pk'])
        PostCommentModel.objects.create(post=comment.post, user=self.request.user, content=form.cleaned_data['content'],
                                        reply=comment, is_reply=True)
        return redirect('posts:post_detail', comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = PostCommentModel.objects.get(pk=self.kwargs['pk'])
        return context


class CreatePostView(LoginRequiredMixin, FormView):
    form_class = CreatePostForm
    template_name = 'posts/create_post.html'

    def form_valid(self, form):
        post = PostModel.objects.create(title=form.cleaned_data['title'], file=form.cleaned_data['file'],
                                        content=form.cleaned_data['content'], tags=form.cleaned_data['tags'],
                                        auther=self.request.user, is_news=False)
        return redirect(post.get_absolute_url())
