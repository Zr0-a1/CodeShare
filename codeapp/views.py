from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.paginator import Paginator

from .models import CodeSnippet, Report, Notification, UserStats
from .forms import (
    CodeSnippetForm,
    RegisterForm,
    ReportForm,
    DashboardPasswordChangeForm,
    EditProfileForm
)

# ------------------------ ALGORITHMS -------------------------
from .algorithms.popularity import rank_snippets, calculate_popularity
from .algorithms.similarity import is_duplicate

# ------------------------ HOME -------------------------
def home(request):
    q = request.GET.get('q', '')
    language = request.GET.get('language', '')

    snippets = CodeSnippet.objects.filter(is_deleted=False).order_by('-created_at')
    if q:
        snippets = snippets.filter(title__icontains=q)
    if language:
        snippets = snippets.filter(language=language)

    all_snippets = list(CodeSnippet.objects.filter(is_deleted=False))
    featured_snippets = rank_snippets(all_snippets)[:6]

    recent_uploads = CodeSnippet.objects.order_by('-created_at')[:6]

    contributors = User.objects.annotate(
        snippet_count=Count('codesnippets'),
        download_count=Sum('codesnippets__downloads'),
        report_count=Sum('codesnippets__reports_count')
    ).order_by('-snippet_count', '-download_count')[:6]

    form = CodeSnippetForm()

    return render(request, 'codeapp/home.html', {
        'snippets': snippets,
        'q': q,
        'language': language,
        'featured_snippets': featured_snippets,
        'recent_uploads': recent_uploads,
        'contributors': contributors,
        'form': form,
    })


# ------------------------ BROWSE -------------------------
@login_required
def browse(request):
    search_query = request.GET.get('search', '')
    selected_languages = request.GET.getlist('language')
    sort_by = request.GET.get('sort', 'newest')

    snippets = CodeSnippet.objects.filter(is_deleted=False)

    if search_query:
        snippets = snippets.filter(title__icontains=search_query)

    if selected_languages:
        snippets = snippets.filter(language__in=selected_languages)

    if sort_by == 'views':
        snippets = snippets.order_by('-views')
    else:
        snippets = snippets.order_by('-created_at')

    paginator = Paginator(snippets, 8)  # 8 snippets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    languages = CodeSnippet.objects.values_list('language', flat=True).distinct()

    return render(request, 'codeapp/browse.html', {
        'snippets': page_obj,
        'search_query': search_query,
        'languages': languages,
        'selected_languages': selected_languages,
        'sort_by': sort_by,
    })


# ------------------------ SNIPPET DETAIL -------------------------
def detail(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, is_deleted=False)
    snippet.views += 1
    snippet.save(update_fields=['views'])

    file_content = None
    if snippet.file:
        try:
            with open(snippet.file.path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            file_content = f"Error reading file: {e}"

    if not file_content:
        file_content = snippet.code
        
    report_form = ReportForm(request.POST or None)

    return render(request, "codeapp/detail.html", {
        "snippet": snippet,
        "file_content": file_content,
        "report_form": report_form,
    })


# ------------------------ REPORT SNIPPET -------------------------
@login_required
def report_snippet(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, is_deleted=False)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.snippet = snippet
            report.reported_by = request.user
            report.resolved = False
            report.save()

            Notification.objects.create(
                user=snippet.author,
                message=f"Your snippet '{snippet.title}' has been reported. Reason: {report.reason}"
            )

            admins = User.objects.filter(is_staff=True).exclude(id=snippet.author.id)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    message=f"Snippet '{snippet.title}' was reported by {request.user.username}. Reason: {report.reason}"
                )

            messages.success(request, "Snippet reported successfully.")
            return redirect("detail", pk=pk)

        messages.error(request, "There was a problem with your report.")
    return redirect("detail", pk=pk)


# ------------------------ UPLOAD / DOWNLOAD -------------------------
@login_required
def upload_code(request):
    if request.method == 'POST':
        upload_mode = request.POST.get('upload_mode')
        form = CodeSnippetForm(request.POST, request.FILES)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user

            if upload_mode == 'code' and not snippet.code:
                form.add_error('code', 'Please paste your code.')
            elif upload_mode == 'file' and not snippet.file:
                form.add_error('file', 'Please upload a file.')
            else:
                snippet.save()

                # ✅ Similarity check (same extension/language only)
                all_snippets = CodeSnippet.objects.filter(is_deleted=False).exclude(id=snippet.id)
                duplicate, score, other = is_duplicate(snippet, all_snippets)

                if duplicate:
                    admins = User.objects.filter(is_staff=True)
                    for admin in admins:
                        Report.objects.create(
                            snippet=snippet,
                            reported_by=request.user,
                            reason=f"Similarity algorithm flagged duplicate (score {score:.1f}% with snippet '{other.title}')"
                        )
                        Notification.objects.create(
                            user=admin,
                            message=f"Snippet '{snippet.title}' flagged as duplicate of '{other.title}' (score {score:.1f}%)."
                        )
                    messages.warning(request, "Your snippet was flagged as similar. Admins will review.")

                return redirect('home')
    else:
        form = CodeSnippetForm()
    return render(request, 'codeapp/upload.html', {'form': form})


@login_required
def download_code(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, is_deleted=False)
    if snippet.file:
        return FileResponse(open(snippet.file.path, 'rb'),
                            as_attachment=True,
                            filename=snippet.file.name.split('/')[-1])
    elif snippet.code:
        response = HttpResponse(snippet.code, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{snippet.title}.txt"'
        return response
    return HttpResponse("No downloadable content available.")


# ------------------------ AUTH -------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')
    else:
        form = RegisterForm()
    return render(request, 'codeapp/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect('user_profile')
        return render(request, 'codeapp/login.html', {"error": "Invalid username or password"})
    return render(request, 'codeapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


## ------------------------ PROFILE -------------------------
@login_required
def user_profile(request):
    snippets = CodeSnippet.objects.filter(author=request.user, is_deleted=False)
    recent_snippets = snippets.order_by('-created_at')[:5]
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()

    return render(request, 'codeapp/profile.html', {
        'snippets': snippets,
        'recent_snippets': recent_snippets,
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required
def user_dashboard(request):
    snippets = CodeSnippet.objects.filter(author=request.user, is_deleted=False)
    reports = Report.objects.filter(snippet__author=request.user).order_by('-created_at')
    stats, _ = UserStats.objects.get_or_create(user=request.user)

    total_views = sum(s.views for s in snippets)
    total_downloads = sum(s.downloads for s in snippets)

    # ✅ Popularity algorithm
    top_snippet = None
    top_score = 0
    if snippets:
        ranked = rank_snippets(list(snippets))
        if ranked:
            top_snippet = ranked[0]
            top_score = calculate_popularity(top_snippet)

    return render(request, 'codeapp/dashboard.html', {
        'snippets': snippets,
        'reports': reports,
        'stats': stats,
        'total_views': total_views,
        'total_downloads': total_downloads,
        'top_snippet': top_snippet,
        'top_score': top_score,
    })


# ------------------------ EDIT PROFILE -------------------------
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("user_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "codeapp/edit_profile.html", {"form": form})


# ------------------------ CHANGE PASSWORD -------------------------
@login_required
def change_password_dashboard(request):
    if request.method == "POST":
        form = DashboardPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Your password was changed successfully.")
            return redirect("user_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DashboardPasswordChangeForm(user=request.user)

    return render(request, "codeapp/change_password_dashboard.html", {"form": form})


# ------------------------ DELETE SNIPPET -------------------------
@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, author=request.user)
    snippet.is_deleted = True   # soft delete
    snippet.save(update_fields=["is_deleted"])
    messages.success(request, f"Snippet '{snippet.title}' deleted successfully.")
    return redirect("user_profile")   # redirect back to profile


# ------------------------ DELETE ACCOUNT -------------------------
@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("home")
    return render(request, "codeapp/delete_account.html")

# ------------------------ NOTIFICATIONS -------------------------
@login_required
def user_notifications(request):
    # Mark unread notifications as read when visiting the notifications page
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'codeapp/notifications.html', {'notes': notes})


@login_required
def mark_all_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read.")
    return redirect('user_profile')
