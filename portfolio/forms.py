from django import forms
from .models import (
    Profile, Skill, Project, Experience, Education, BlogPost, ContactMessage
)

# Shared widget styling so every field gets the same clean look
TEXT_CLASS = "form-control"


def styled(widget_cls, **attrs):
    attrs.setdefault("class", TEXT_CLASS)
    return widget_cls(attrs=attrs)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": styled(forms.TextInput, placeholder="Your name"),
            "email": styled(forms.EmailInput, placeholder="Your email"),
            "subject": styled(forms.TextInput, placeholder="Subject"),
            "message": styled(forms.Textarea, placeholder="Your message", rows=5),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = []
        widgets = {
            "full_name": styled(forms.TextInput),
            "tagline": styled(forms.TextInput),
            "bio": styled(forms.Textarea, rows=6),
            "email": styled(forms.EmailInput),
            "phone": styled(forms.TextInput),
            "location": styled(forms.TextInput),
            "github_url": styled(forms.URLInput),
            "linkedin_url": styled(forms.URLInput),
            "twitter_url": styled(forms.URLInput),
            "instagram_url": styled(forms.URLInput),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
        widgets = {
            "name": styled(forms.TextInput),
            "category": styled(forms.Select),
            "proficiency": styled(forms.NumberInput, min=0, max=100),
            "icon_class": styled(forms.TextInput),
            "order": styled(forms.NumberInput),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["slug", "created_at"]
        widgets = {
            "title": styled(forms.TextInput),
            "short_description": styled(forms.TextInput),
            "description": styled(forms.Textarea, rows=5),
            "tech_stack": styled(forms.TextInput, placeholder="Django, React, PostgreSQL"),
            "live_url": styled(forms.URLInput, placeholder="https://your-live-site.com/page"),
            "github_url": styled(forms.URLInput),
            "order": styled(forms.NumberInput),
        }
        help_texts = {
            "live_url": "Paste the link of the website/page where this work can be viewed live.",
            "document_file": "Upload a Word (.doc/.docx) or PDF file describing this project.",
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = "__all__"
        widgets = {
            "role": styled(forms.TextInput),
            "company": styled(forms.TextInput),
            "location": styled(forms.TextInput),
            "start_date": styled(forms.DateInput, type="date"),
            "end_date": styled(forms.DateInput, type="date"),
            "description": styled(forms.Textarea, rows=4),
            "order": styled(forms.NumberInput),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = "__all__"
        widgets = {
            "institution": styled(forms.TextInput),
            "degree": styled(forms.TextInput),
            "field_of_study": styled(forms.TextInput),
            "start_date": styled(forms.DateInput, type="date"),
            "end_date": styled(forms.DateInput, type="date"),
            "description": styled(forms.Textarea, rows=4),
            "order": styled(forms.NumberInput),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ["slug", "created_at"]
        widgets = {
            "title": styled(forms.TextInput),
            "content": styled(forms.Textarea, rows=8),
        }
