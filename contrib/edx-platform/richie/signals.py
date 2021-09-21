from django.dispatch import receiver
from xmodule.modulestore.django import SignalHandler

from .sync import sync_course_from_key


@receiver(SignalHandler.course_published, dispatch_uid="update_course_on_publish")
def update_course_on_publish(sender, course_key, **kwargs):
    """
    Synchronize course properties with Richie catalog.
    """
    sync_course_from_key(course_key)
