from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

def env_bool(name, default=False):
    return str(os.environ.get(name, str(default))).lower() in {"1", "true", "yes", "on"}

def env_list(name, default=""):
    return [v.strip() for v in os.environ.get(name, default).split(",") if v.strip()]

_env_file = BASE_DIR / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

DEBUG = env_bool("DEBUG", not bool(os.environ.get("RENDER_EXTERNAL_HOSTNAME")))
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-this-key")
if not DEBUG and SECRET_KEY == "dev-only-change-this-key":
    raise RuntimeError("Set SECRET_KEY in the production environment.")
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1")
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")
if _render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_render_host}")
SITE_URL = os.environ.get("SITE_URL", "http://localhost:8000")
MEDIA_STORAGE = os.environ.get("MEDIA_STORAGE", "filesystem").strip().lower()

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "apps.core", "apps.accounts", "apps.products", "apps.cart", "apps.orders",
    "apps.payments", "apps.notifications", "store",
]
if MEDIA_STORAGE == "s3":
    INSTALLED_APPS.append("storages")
elif MEDIA_STORAGE != "filesystem":
    raise RuntimeError("MEDIA_STORAGE must be either 'filesystem' or 's3'.")
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True, "OPTIONS": {"context_processors": [
    "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages", "apps.core.context_processors.site",
]}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default": dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600)}
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = ["apps.accounts.backends.EmailOrUsernameBackend"]
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media"))).expanduser().resolve()
IS_RENDER = bool(_render_host)
WHITENOISE_AUTOREFRESH = not IS_RENDER
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage" if IS_RENDER and not DEBUG else "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
if MEDIA_STORAGE == "s3":
    bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME", "").strip()
    if not bucket_name:
        raise RuntimeError("Set AWS_STORAGE_BUCKET_NAME when MEDIA_STORAGE=s3.")
    media_options = {
        "bucket_name": bucket_name,
        "querystring_auth": env_bool("AWS_QUERYSTRING_AUTH", True),
        "file_overwrite": True,
    }
    for option, variable in (
        ("access_key", "AWS_ACCESS_KEY_ID"),
        ("secret_key", "AWS_SECRET_ACCESS_KEY"),
        ("region_name", "AWS_S3_REGION_NAME"),
        ("endpoint_url", "AWS_S3_ENDPOINT_URL"),
    ):
        value = os.environ.get(variable, "").strip()
        if value:
            media_options[option] = value
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": media_options,
    }
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", not DEBUG and IS_RENDER)
SESSION_COOKIE_SECURE = not DEBUG and IS_RENDER
CSRF_COOKIE_SECURE = not DEBUG and IS_RENDER
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000" if IS_RENDER and not DEBUG else "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = IS_RENDER and not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_TRUSTED_ORIGINS += [f"https://{host}" for host in ALLOWED_HOSTS if host not in {"localhost", "127.0.0.1"}]
OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 300
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_COOLDOWN_SECONDS = 30
OTP_MAX_SENDS_PER_HOUR = 5
ORDER_OTP_STAGE = os.environ.get("ORDER_OTP_STAGE", "before_payment")
LOGIN_MAX_FAILED_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 900
FREE_SHIPPING_THRESHOLD = 0
FLAT_SHIPPING_CHARGE = 0
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "")
WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_PROVIDER_NUMBER = os.environ.get("WHATSAPP_PROVIDER_NUMBER", "")
EMAIL_API_KEY = os.environ.get("EMAIL_API_KEY", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "EL MITO <no-reply@localhost>")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend" if EMAIL_HOST else "django.core.mail.backends.console.EmailBackend")







