from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.contrib.admin.views.decorators import staff_member_required

from .models import CodeSnippet, Comment, Report, Notification
from .forms import CodeSnippetForm, RegisterForm, CommentForm, ReportForm


# ------------------------ HOME PAGE -------------------------
def home(request):
    q = request.GET.get('q', '')
    language = request.GET.get('language', '')

    snippets = CodeSnippet.objects.filter(is_deleted=False).order_by('-created_at')

    if q:
        snippets = snippets.filter(title__icontains=q)

    if language:
        snippets = snippets.filter(language=language)

    return render(request, 'codeapp/home.html', {
        'snippets': snippets,
        'q': q,
        'language': language,
    })


# ------------------------ SNIPPET DETAIL -------------------------
def detail(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, is_deleted=False)

    return render(request, 'codeapp/detail.html', {
        'snippet': snippet,
        'comment_form': CommentForm(),
        'report_form': ReportForm(),
    })


# ------------------------ COMMENTS -------------------------
@login_required
def add_comment(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, is_deleted=False)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.snippet = snippet
        comment.save()

    return redirect('detail', pk=pk)


# ------------------------ REPORTING -------------------------
@login_required
def report_snippet(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, is_deleted=False)

    form = ReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        report.snippet = snippet
        report.user = request.user
        report.save()

    return redirect('detail', pk=pk)


# ------------------------ UPLOAD CODE -------------------------
@login_required
def upload_code(request):
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST, request.FILES)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            return redirect('home')
    else:
        form = CodeSnippetForm()

    return render(request, 'codeapp/upload.html', {'form': form})


# ------------------------ DOWNLOAD CODE -------------------------
@login_required
def download_code(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk)

    # prevent non-authors downloading if needed
    if snippet.is_deleted:
        return HttpResponse("This file is removed by admin.")

    if not snippet.file:
        return HttpResponse("No file available.")

    extension = snippet.file.name.split('.')[-1]
    filename = f"{snippet.title}.{extension}"

    return FileResponse(open(snippet.file.path, 'rb'), as_attachment=True, filename=filename)


# ------------------------ USER AUTH -------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'codeapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'codeapp/login.html', {'error': 'Invalid credentials'})

    return render(request, 'codeapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ------------------------ USER DASHBOARD -------------------------
@login_required
def user_dashboard(request):
    snippets = CodeSnippet.objects.filter(author=request.user)
    notifications = Notification.objects.filter(user=request.user, is_seen=False)

    return render(request, 'codeapp/dashboard.html', {
        'snippets': snippets,
        'notifications': notifications.count(),
    })


# ------------------------ NOTIFICATIONS -------------------------
@login_required
def user_notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')

    # mark as seen
    notes.update(is_seen=True)

    return render(request, 'codeapp/notifications.html', {'notes': notes})


# ------------------------ ADMIN DASHBOARD -------------------------
@staff_member_required
def admin_dashboard(request):
    total_projects = CodeSnippet.objects.count()
    total_reports = Report.objects.count()
    pending_reports = Report.objects.filter(is_reviewed=False).count()

    return render(request, 'codeapp/admin_dashboard.html', {
        'total_projects': total_projects,
        'total_reports': total_reports,
        'pending': pending_reports,
    })
