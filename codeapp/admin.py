from django.contrib import admin
from django.utils import timezone
from .models import CodeSnippet, Report, Notification, UserStats


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'author', 'created_at', 'is_deleted')
    list_filter = ('language', 'is_deleted')
    search_fields = ('title', 'description', 'author__username')
    actions = ['mark_deleted', 'restore_snippet']

    def mark_deleted(self, request, queryset):
        for s in queryset:
            Notification.objects.create(
                user=s.author,
                message=f"Your snippet '{s.title}' was removed by admin."
            )
            s.is_deleted = True
            s.deleted_at = timezone.now()
            s.save()
    mark_deleted.short_description = "Mark selected snippets as deleted (notify author)"

    def restore_snippet(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
    restore_snippet.short_description = "Restore selected snippets"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('snippet', 'reported_by', 'reason', 'resolved', 'created_at')
    list_filter = ('resolved', 'created_at')
    search_fields = ('snippet__title', 'reported_by__username', 'reason')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'deleted_count')
    search_fields = ('user__username',)
