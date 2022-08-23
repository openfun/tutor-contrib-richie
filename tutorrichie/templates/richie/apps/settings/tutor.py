from django.conf import global_settings, settings
from django.utils.translation import gettext_lazy as _

from configurations import values
{% if RICHIE_FACTORY_REPOSITORY %}
from {{ RICHIE_FACTORY_SITE }}.settings import Development, Production
{% else %}
from settings import Development, Production
{% endif %}

supported_languages = [("en", _("English")),]
extra_language_code = "{{ LANGUAGE_CODE }}"
extra_language_code = "es" if extra_language_code == "es-419" else extra_language_code
extra_language = dict(global_settings.LANGUAGES).get(extra_language_code)
if extra_language_code != "en" and extra_language is not None:
    supported_languages.append(
        (
            "{{ LANGUAGE_CODE }}",
            _(extra_language)
        )
    )

class TutorSettingsMixin:
    RICHIE_COURSE_RUN_SYNC_SECRETS = values.ListValue(["{{ RICHIE_HOOK_SECRET }}"])
    # Restore error logging, which is disabled by default
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    }
    LANGUAGE_CODE = "{{ LANGUAGE_CODE }}"
    LANGUAGES = supported_languages
    CMS_LANGUAGES = {
        "default": {
            "public": True,
            "hide_untranslated": False,
            "redirect_on_fallback": False,
            "fallbacks": [language[0] for language in supported_languages],
        },
        1: [
            {
                "public": True,
                "code": language[0],
                "hide_untranslated": False,
                "name": language[1],
                "fallbacks": [supported_languages[0][0]],
                "redirect_on_fallback": False,
            }
            for language in supported_languages
        ]
    }
    PARLER_LANGUAGES = CMS_LANGUAGES

    SESSION_ENGINE = "django.contrib.sessions.backends.db"

    {{ patch("richie-settings-common")|indent(4) }}

class TutorProduction(TutorSettingsMixin, Production):
    """
    Tutor-specific settings for production.
    """
    {% if not ENABLE_HTTPS %}
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SESSION_COOKIE_SECURE = False
    {% endif %}

    CDN_DOMAIN = "{{ RICHIE_HOST }}"
    {{ patch("richie-settings-production")|indent(4) }}


class TutorDevelopment(TutorSettingsMixin, Development):
    """
    Tutor-specific settings for development.
    """
    {{ patch("richie-settings-development")|indent(4) }}
