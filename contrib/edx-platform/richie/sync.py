import hashlib
import hmac
import json
import logging


from django.conf import settings
import requests
import requests.exceptions
from xmodule.modulestore.django import modulestore

logger = logging.getLogger(__name__)


def sync_all_courses():
    """
    Synchronize all courses with Richie.
    """
    for course in modulestore().get_courses():
        sync_course(course)


def sync_course_from_key(course_key):
    return sync_course(modulestore().get_course(course_key))


def sync_course(course):
    """
    Synchronize an Open edX course with a Richie instance.

    Note that only the course settings are synchronized, and not the actual
    course contents or description. This function always succeeds, even when the
    request fails.
    """
    enrollment_start = course.enrollment_start and course.enrollment_start.isoformat()
    enrollment_end = course.enrollment_end and course.enrollment_end.isoformat()
    data = {
        "resource_link": "{}/courses/{}/course".format(
            settings.LMS_ROOT_URL, course.id
        ),
        "start": course.start and course.start.isoformat(),
        "end": course.end and course.end.isoformat(),
        "enrollment_start": enrollment_start,
        "enrollment_end": enrollment_end,
        "languages": [course.language or settings.LANGUAGE_CODE],
    }

    signature = hmac.new(
        settings.RICHIE_COURSE_HOOK["secret"].encode("utf-8"),
        msg=json.dumps(data).encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    try:
        response = requests.post(
            settings.RICHIE_COURSE_HOOK["url"],
            json=data,
            headers={"Authorization": "SIG-HMAC-SHA256 {:s}".format(signature)},
            timeout=settings.RICHIE_COURSE_HOOK["timeout"],
        )
    except requests.exceptions.Timeout:
        logger.error(
            f"Could not synchronize course {course.id} with Richie. Response timeout"
        )
        return
    if response.status_code >= 400:
        logger.error(
            f"Could not synchronize course {course.id} with Richie. Response: {response.content.decode()}"
        )
    else:
        logger.info(f"Successfuly synchronized course {course.id} with Richie")
