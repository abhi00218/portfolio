# Dynamic Portfolio — built on the "personalportfolio-master" UI

This project takes the visual design (colors, fonts, layout, header/footer,
buttons, animations) of **personalportfolio-master** and rebuilds it as a
fully **dynamic Django site** on top of the backend/admin engine from your
**portfolio_project_amazing_ui** upload. Nothing about the look was
redesigned from scratch — every page reuses the original theme's CSS/JS/img
files from `static/master/assets/`.

## What you get

1. **Same UI, now dynamic.** Home, About, Portfolio (list + details), Blog
   (list + details) and Contact pages all use the master theme's markup,
   but every piece of content (profile, skills, projects, experience,
   education, blog posts) is pulled from the database and editable from
   the admin dashboard — nothing is hardcoded in the HTML anymore.

2. **Everything the static template didn't have:**
   - Admin dashboard (`/dashboard/`) to manage Profile, Skills, Projects,
     Experience, Education, Blog Posts and incoming Contact Messages —
     no code editing required to update the site.
   - A working Contact form that saves messages to the database (the
     original template's form posted to a PHP script that doesn't exist
     in a Django app).
   - Slugged, SEO-friendly URLs for projects and blog posts.
   - File uploads: project write-ups (Word/PDF), and a resume/CV on the
     Profile.

3. **The feature you asked for — Gmail-style document preview.**
   Anywhere you see a **"View"** button next to an uploaded Word/PDF file
   (project detail page, project cards, the resume link, and in the admin
   dashboard), clicking it opens the document **in a popup on the same
   page** — just like clicking an attachment in Gmail — with a
   **Download** button and a close (×) button. No page reload, no new tab.
   - `.docx` files are converted to HTML and rendered in-browser using
     mammoth.js (no server round-trip needed beyond fetching the file).
   - `.pdf` files are shown natively in an embedded frame.
   - Other types show a friendly "please download to view" message.
   - Logic lives in `static/js/doc-viewer.js` and
     `portfolio/templates/portfolio/includes/doc_viewer_modal.html`.

4. **Admin dashboard UI** is a separate, clean dark-sidebar interface
   (`static/css/dashboard.css`) — distinct from the public site's theme,
   since an admin panel and a public portfolio don't need to look alike.

## Project structure

```
portfolio_project/
├── manage.py
├── requirements.txt
├── portfolio_project/        # Django settings/urls
├── portfolio/
│   ├── models.py             # Profile, Skill, Project, Experience, Education, BlogPost, ContactMessage
│   ├── views.py              # public site + dashboard views
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       ├── portfolio/        # public site — master theme markup, now dynamic
│       │   ├── base.html
│       │   ├── home.html
│       │   ├── about.html
│       │   ├── project_list.html
│       │   ├── project_detail.html
│       │   ├── blog_list.html
│       │   ├── blog_detail.html
│       │   ├── contact.html
│       │   └── includes/doc_viewer_modal.html
│       └── dashboard/        # admin panel
└── static/
    ├── master/assets/        # original personalportfolio-master theme (css/js/img/fonts), untouched
    ├── css/dynamic.css       # only new CSS: doc viewer modal, skill bars, timeline
    ├── css/dashboard.css     # admin panel styling
    └── js/doc-viewer.js      # Gmail-style document preview logic
```

## Running it locally

```bash
cd portfolio_project
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --username admin  # for /dashboard/ login
python manage.py runserver
```

- Public site: http://127.0.0.1:8000/
- Admin dashboard: http://127.0.0.1:8000/dashboard/  (log in with the
  superuser you just created)
- Django admin (optional, for raw model editing): http://127.0.0.1:8000/admin/

The first time you open the site, add your Profile, Skills, Projects,
Experience, Education and Blog posts from `/dashboard/` — the public pages
will fill in automatically and show friendly "nothing added yet" messages
until you do.

## Notes

- `document_file` on a Project and `resume_file` on the Profile both accept
  `.pdf`, `.docx`, `.doc` and a few other types — the **View** button
  adapts automatically based on the file extension.
- The site currently uses SQLite (zero setup). Swap the `DATABASES` setting
  in `portfolio_project/settings.py` for Postgres/MySQL when you deploy.
- Before deploying: set `DEBUG = False`, fill in `ALLOWED_HOSTS`, and run
  `python manage.py collectstatic`.
