def plugin_settings(settings):
    """Common settings for Richie catalog connector"""
    settings.RICHIE_COURSE_HOOK = {
        "secret": "richiesecret",
        "url": "http://richie:8000/api/v1.0/course-runs-sync/",
        "timeout": 3,
    }
