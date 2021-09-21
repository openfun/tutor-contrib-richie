from django.apps import AppConfig
from edx_django_utils.plugins.constants import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType


class RichieAppConfig(AppConfig):
    name = "richie"
    verbose_name = "Richie course catalog connector"

    # Open edX plugin docs: https://github.com/edx/edx-django-utils/blob/master/edx_django_utils/plugins/README.rst
    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: "richie",
                PluginURLs.REGEX: r"^richie/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: "settings.lms",
                },
            },
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: "settings.cms",
                },
            },
        },
    }

    def ready(self):
        """
        Connect signal handlers.
        """
        # pylint: disable=unused-import
        from . import signals
