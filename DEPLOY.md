# Deployment Guide — Event Management System (Django + MySQL)

This is a documentation-only guide. Nothing in the codebase has been changed to
implement these steps — follow them yourself (or ask for help implementing
each one) before putting this app on the public internet.

## 0. Urgent: rotate the exposed database password first

`event_management_system/settings.py` currently has a real-looking MySQL root
password committed in plaintext, in the very first git commit. Anyone with
read access to this repository (or its history, forever) has that password.

- Change the MySQL root password now, regardless of deployment timeline.
- Do this before anything else below — a new `SECRET_KEY` and env vars won't
  matter if the DB credential is still valid and public.

## 1. Add a dependency manifest

There is currently no `requirements.txt`. Create one with (at minimum):

```
Django>=4.2,<5
pymysql
gunicorn
whitenoise
python-decouple
```

(The project's `event_management_system/__init__.py` already does
`import pymysql; pymysql.install_as_MySQLdb()`, so `pymysql` — not
`mysqlclient` — is the driver actually in use.)

Generate the exact pinned versions from your working environment with:

```bash
pip freeze > requirements.txt
```

## 2. Move secrets/config out of settings.py into environment variables

In `event_management_system/settings.py`, replace the hardcoded values:

- `SECRET_KEY` — currently a hardcoded `django-insecure-...` string. Generate
  a new one (`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
  and read it from an env var, e.g. via `python-decouple`:
  `SECRET_KEY = config('SECRET_KEY')`.
- `DEBUG` — currently hardcoded `True`. Use `DEBUG = config('DEBUG', default=False, cast=bool)`.
- `DATABASES` — currently hardcodes `HOST: 'localhost'`, `USER: 'root'`, and
  a plaintext password. Read all of `NAME`/`USER`/`PASSWORD`/`HOST`/`PORT`
  from env vars instead.
- `ALLOWED_HOSTS` — currently `[]`, which rejects every request once
  `DEBUG=False`. Set it to your deployed domain(s), e.g.
  `ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')`.

Create a local `.env` file (never commit it — see step 6) for local dev with
these values, and set the same variables in your hosting platform's
dashboard/CLI for production.

## 3. Set up the production MySQL database

Since this project stays on MySQL, you need a host that offers managed MySQL,
for example:
- **PythonAnywhere** — has first-class MySQL support out of the box, simplest
  option for a Django+MySQL app like this one.
- **Railway** or **Render** — can attach a MySQL plugin/service (check current
  free-tier availability, it varies).
- Any VPS (DigitalOcean, Linode, etc.) with MySQL installed yourself.

Once the database exists:

```bash
python manage.py migrate
python manage.py createsuperuser
```

The `db.sqlite3` file committed in this repo is stale (settings.py points at
MySQL, not sqlite) — it can be ignored/removed, it's not part of the real data
path.

## 4. Serve static files

`STATIC_ROOT` and `STATICFILES_DIRS` are already configured in settings.py,
and `collectstatic` has already been run once (the `staticfiles/` folder
exists). But Django itself does not serve static files in production, and no
static-file server (like WhiteNoise) is wired into `MIDDLEWARE` yet.

Add WhiteNoise:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # add this line, right after SecurityMiddleware
    ...
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

Then run `python manage.py collectstatic` as part of your deploy step.

## 5. Process/start command

Add a `Procfile` (needed for Heroku-style platforms; Railway/Render can also
use a custom start command directly in their dashboard instead):

```
web: gunicorn event_management_system.wsgi --log-file -
```

`gunicorn` needs to be in `requirements.txt` (see step 1).

## 6. Add a `.gitignore`

There currently is none, which is why `db.sqlite3`, every `__pycache__/`
directory, and the entire `staticfiles/` build output are committed. Add:

```
__pycache__/
*.pyc
db.sqlite3
.env
staticfiles/
```

Note: adding `.gitignore` now does **not** remove these files (or the leaked
MySQL password) from git history — they're already permanently recorded in
past commits. If that matters (public repo, sensitive data), a history
rewrite (`git filter-repo` or the BFG Repo-Cleaner) is the only real fix, run
as a separate, deliberate step — not done as part of this guide.

## 7. Production security settings

Once the app is live behind HTTPS, add to `settings.py` (env-gated so local
dev over plain HTTP still works):

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
```

## 8. Deploy checklist summary

1. Rotate the exposed MySQL password.
2. Add `requirements.txt`.
3. Move `SECRET_KEY` / `DEBUG` / `DATABASES` / `ALLOWED_HOSTS` to env vars.
4. Provision a managed MySQL database on your chosen host; run `migrate`.
5. Add WhiteNoise middleware + storage config; run `collectstatic`.
6. Add a `Procfile` (`web: gunicorn event_management_system.wsgi`).
7. Add `.gitignore`; stop committing `db.sqlite3`/`staticfiles/`/`__pycache__/`.
8. Turn on `SECURE_SSL_REDIRECT`/`SESSION_COOKIE_SECURE`/`CSRF_COOKIE_SECURE` once HTTPS is confirmed working.

## Also worth knowing before you go live

This deploy guide only covers *getting the app running* on a host. It does
not cover application-level security gaps found during the audit (e.g. the
`edit_event` view currently has no login/staff check at all, ticket
registration has no capacity limit, etc.) — those are separate fixes, not a
deployment concern, and should be addressed before this app handles real
user data.
