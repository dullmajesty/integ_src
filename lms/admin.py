from django.contrib import admin
from .models import TrainerRegistration

@admin.register(TrainerRegistration)
class TrainerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')
    list_filter = ('status',)
