from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, DetailView, UpdateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from .forms import StatusCreationForm, StatusCommentForm, StatusEditForm
from .models import StatusModel, StatusLikeModel, StatusCommentModel
from accounts.models import UserModel
from accounts.views import UserProfileView
from utils import ProfileContextMixin, UnBlockedRequiredMixin, PublicUserProfileRequiredMixin


class StatusCreationView(LoginRequiredMixin, FormView):
    form_class = StatusCreationForm

    def form_valid(self, form):
        status = StatusModel(
            from_user=self.request.user,
            to_user=UserModel.objects.get(pk=self.kwargs['pk']),
            content=form.cleaned_data['content'],
            file=form.cleaned_data['file'],
            is_private=form.cleaned_data['is_private']
        )
        status.save()
        return redirect(status.to_user.get_absolute_url())


class StatusLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        StatusLikeModel.objects.create(user=request.user, status_id=kwargs['status_pk'])
        return redirect('statuses:status_detail', pk=kwargs['status_pk'])


class StatusUnlikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        StatusLikeModel.objects.get(user=request.user, status_id=kwargs['status_pk']).delete()
        return redirect('statuses:status_detail', pk=kwargs['status_pk'])


class StatusCommentCreateView(LoginRequiredMixin, FormView):
    form_class = StatusCommentForm

    def form_valid(self, form):
        StatusCommentModel.objects.create(
            user=self.request.user,
            status_id=self.kwargs['status_pk'],
            content=form.cleaned_data['content']
        )
        return redirect('statuses:status_detail', pk=self.kwargs['status_pk'])


class EditStatusView(LoginRequiredMixin, UpdateView):
    model = StatusModel
    form_class = StatusEditForm
    pk_url_kwarg = 'status_pk'
    template_name = 'statuses/status_edit.html'

    def setup(self, request, *args, **kwargs):
        self.status = StatusModel.objects.get(pk=kwargs['status_pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user == self.status.from_user:
            messages.error(request, 'شما نمیتوانید این استتوس را ویرایش کنید')
            return redirect(self.status.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_pk'] = self.kwargs['status_pk']
        context['status_is_message'] = StatusModel.objects.get(pk=self.kwargs['status_pk']).is_message
        return context


class DeleteStatusView(LoginRequiredMixin, ProfileContextMixin, View):
    def setup(self, request, *args, **kwargs):
        self.status = StatusModel.objects.get(pk=kwargs['status_pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user not in {self.status.to_user, self.status.from_user}:
            messages.error(request, 'شما نمیتوانید این استتوس را حذف کنید')
            return redirect(self.status.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.status
        return context

    def get(self, request, *args, **kwargs):
        state = request.GET.get('state')
        if state is None:
            return render(request, 'statuses/status_delete.html', self.get_context_data())
        if state == 'confirm':
            self.status.delete()
            return redirect(self.status.to_user.get_absolute_url())
        if state == 'cancel':
            return redirect(self.status.get_absolute_url())


class PinStatusView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.status = StatusModel.objects.get(pk=kwargs['status_pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user == self.status.from_user or not request.user == self.status.to_user:
            messages.error(request, 'شما نمیتوانید این استتوس را پین کنید')
            return redirect(self.status.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        state = request.GET.get('state')
        if state == 'pin':
            self.status.is_pin = True
        if state == 'unpin':
            self.status.is_pin = False
        self.status.save()
        return redirect(self.status.get_absolute_url())


class StatusDetailView(ProfileContextMixin, LoginRequiredMixin, DetailView):
    template_name = 'statuses/status.html'
    model = StatusModel
    pk_url_kwarg = 'status_pk'
    context_object_name = 'status'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_create_comment_form'] = StatusCommentForm()
        return context


class StatusListView(ProfileContextMixin, LoginRequiredMixin, ListView):
    model = StatusModel
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'
    paginate_by = 5

    def get_queryset(self):
        return StatusModel.objects.filter(from_user_id=self.kwargs['pk'])


class PrivateStatusListView(ProfileContextMixin, LoginRequiredMixin, ListView):
    model = StatusModel
    template_name = 'statuses/private_statuses_list.html'
    context_object_name = 'statuses'
    paginate_by = 5

    def get_queryset(self):
        return StatusModel.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user)).filter(
            is_private=True)
