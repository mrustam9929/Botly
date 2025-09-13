from django.contrib import admin

from apps.feedback_bot.models import FbbSettings, FbbUser, UserFeedBack


@admin.register(FbbSettings)
class FbbSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(FbbUser)
class FbbUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserFeedBack)
class UserFeedbackAdmin(admin.ModelAdmin):
    pass
