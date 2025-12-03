from django.db import models
from django.contrib.auth.models import User

LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('cpp', 'C++'),
    ('javascript', 'JavaScript'),
    ('c', 'C'),
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('dart', 'Dart'),
]

class CodeSnippet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)

    code = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="snippets/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Soft delete system
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codesnippets')

  
    views = models.PositiveIntegerField(default=0)        
    downloads = models.PositiveIntegerField(default=0)    
    reports_count = models.PositiveIntegerField(default=0) 
    likes = models.PositiveIntegerField(default=0)        

    def __str__(self):
        return f"{self.title} ({self.language})"


class Report(models.Model):
    snippet = models.ForeignKey('codeapp.CodeSnippet', on_delete=models.CASCADE, related_name="reports")
    reason = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for {self.snippet.title}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notif → {self.user.username}"


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uploads_count = models.IntegerField(default=0)
    deleted_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.user.username}"



