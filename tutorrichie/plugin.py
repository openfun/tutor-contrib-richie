from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__

templates = pkg_resources.resource_filename("tutorrichie", "templates")

config = {
    "unique": {
        "HOOK_SECRET": "{{ 20|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "MYSQL_PASSWORD": "{{ 12|random_string }}",
        "COURSE_RUN_SYNC_SECRETS": "{{ 12|random_string }}"
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}fundocker/openedx-richie:{{ RICHIE_VERSION }}",
        "RELEASE_VERSION": "v2.9.1",
        "HOST": "courses.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "richie",
        "MYSQL_USERNAME": "richie",
        "BUCKET_NAME": "richieuploads",
        "MEDIA_BUCKET_NAME": "production-richie-media",
        "ELASTICSEARCH_INDICES_PREFIX": "richie",
        "DJANGO_SETTINGS_MODULE": "settings.production",
        "DJANGO_CONFIGURATION": "Production",
        "AWS_DEFAULT_ACL": "public-read",
        "AWS_S3_SIGNATURE_VERSION": "s3v4",
        "AWS_REGION": "us-east-1",
        "AWS_QUERYSTRING_AUTH": "false",
    },
}

hooks.Filters.CLI_DO_INIT_TASKS.add_item((
    "mysql",
    ("richie", "tasks", "richie-openedx", "init"),
))

hooks.Filters.IMAGES_BUILD.add_item((
    "richie",
    ("plugins", "richie", "build", "richie"),
    "{{ RICHIE_DOCKER_IMAGE }}",
    (),
))

hooks.Filters.IMAGES_PULL.add_item((
    "richie",
    "{{ RICHIE_DOCKER_IMAGE }}",
))

hooks.Filters.IMAGES_PUSH.add_item((
    "richie",
    "{{ RICHIE_DOCKER_IMAGE }}",
))


# Add the "templates" folder as a template root
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorrichie", "templates")
)
# Render the "build" and "apps" folders
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("richie/build", "plugins"),
        ("richie/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorrichie", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
# Add configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"RICHIE_{key}", value)
        for key, value in config.get("defaults", {}).items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"RICHIE_{key}", value)
        for key, value in config.get("unique", {}).items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)
