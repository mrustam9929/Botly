from django import forms
from django.contrib import admin

from apps.companies.models import Company, CompanyBot

class CompanyBotForm(forms.ModelForm):
    token = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text="Введите токен, если хотите его изменить. "
                  "Текущий токен не отображается по соображениям безопасности.",
    )

    class Meta:
        model = CompanyBot
        fields = ["company", "bot_module", "name", "token"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        token = self.cleaned_data.get("token")
        if token:  # только если ввели новый токен
            instance.token = token
        if commit:
            instance.save()
        return instance


@admin.register(CompanyBot)
class CompanyBotAdmin(admin.ModelAdmin):
    form = CompanyBotForm
    list_display = ("id", "company", "bot_module", "name", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def get_fields(self, request, obj=None):
        """Определяем поля, чтобы не показывать _token"""
        return ["company", "bot_module", "name", "token", "created_at", "updated_at"]

    def get_readonly_fields(self, request, obj=None):
        """При редактировании токен не обязателен, его можно только обновить"""
        ro_fields = list(super().get_readonly_fields(request, obj))
        return ro_fields

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


