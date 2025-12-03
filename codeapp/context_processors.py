from .forms import CodeSnippetForm
from .models import Notification

def upload_form(request):
    """
    Makes the CodeSnippetForm available globally (e.g. in base.html upload modal).
    """
    return {'form': CodeSnippetForm()}


def notifications(request):
    """
    Provides unread notifications count and list for the logged-in user.
    """
    if request.user.is_authenticated:
        notes = Notification.objects.filter(user=request.user, is_read=False)
        return {
            'notifications_count': notes.count(),
            'notes': notes
        }
    return {
        'notifications_count': 0,
        'notes': []
    }
