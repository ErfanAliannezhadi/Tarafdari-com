from django.contrib import admin
from statuses.models import StatusModel, StatusLikeModel, StatusCommentModel

admin.site.register(StatusModel)
admin.site.register(StatusLikeModel)
admin.site.register(StatusCommentModel)
