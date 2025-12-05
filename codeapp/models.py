from django.db import models
from django.contrib.auth.models import User

# ------------------------
# Language Choices
# ------------------------
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

# Mapping language → file extension
LANGUAGE_EXTENSIONS = {
    'python': 'py',
    'java': 'java',
    'cpp': 'cpp',
    'javascript': 'js',
    'c': 'c',
    'html': 'html',
    'css': 'css',
    'dart': 'dart',
}

# ------------------------
# CodeSnippet Model
# ------------------------
class CodeSnippet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)

    code = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="snippets/", blank=True, null=True)

    # Stores filename for pasted code (.py, .java, etc.)
    generated_filename = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Soft delete
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codesnippets')

    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    reports_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.language})"

    @property
    def extension(self):
        """Returns the correct file extension based on language."""
        return LANGUAGE_EXTENSIONS.get(self.language, "txt")


# ------------------------
# Report Model
# ------------------------
class Report(models.Model):
    snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)  
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.snippet.title} by {self.reported_by.username}"


# ------------------------
# Notification Model
# ------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"


# ------------------------
# UserStats Model
# ------------------------
class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deleted_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.user.username}"
