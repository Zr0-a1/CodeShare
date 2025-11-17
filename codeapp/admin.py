from django.contrib import admin
from .models import CodeSnippet, Comment, Report, Notification, UserStats
from django.utils import timezone 

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('title','language','author','created_at','is_deleted')
    list_filter = ('language','is_deleted')
    search_fields = ('title','description','author__username')
    actions = ['mark_deleted','restore_snippet']

    def mark_deleted(self, request, queryset):
        for s in queryset:
            # create notification for the author
            from .models import Notification
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

admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Notification)
admin.site.register(UserStats)