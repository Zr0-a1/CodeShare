from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import CodeSnippet, Report



# ------------------------- REGISTER FORM -------------------------
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = None
        self.fields["password"].help_text = None
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# ------------------------- EDIT PROFILE FORM -------------------------
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]  # ✅ no password
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = None 

# ------------------------- PASSWORD CHANGE FORM -------------------------
class DashboardPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})


# ------------------------- SNIPPET UPLOAD FORM -------------------------
class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ["title", "language", "description", "code", "file"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control form-dark",
                "placeholder": "Enter snippet title"
            }),
            "language": forms.Select(attrs={"class": "form-select form-dark"}),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control form-dark",
                "placeholder": "Brief description of your snippet"
            }),
            "code": forms.Textarea(attrs={
                "rows": 10,
                "class": "form-control form-dark",
                "placeholder": "Paste your code here..."
            }),
            "file": forms.ClearableFileInput(attrs={"class": "form-control form-dark"}),
        }

# ------------------------- REPORT FORM -------------------------
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason"]   
        widgets = {
            "reason": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Describe the issue..."
            })
        }

