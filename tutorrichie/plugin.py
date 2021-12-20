from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename("tutorrichie", "templates")

config = {
    "add": {
        "HOOK_SECRET": "{{ 20|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "MYSQL_PASSWORD": "{{ 12|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-richie:{{ RICHIE_VERSION }}",
        "RELEASE_VERSION": "v2.9.1",
        "HOST": "courses.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "richie",
        "MYSQL_USERNAME": "richie",
        "ELASTICSEARCH_INDICES_PREFIX": "richie",
    },
}

hooks = {
    "build-image": {"richie": "{{ RICHIE_DOCKER_IMAGE }}"},
    "remote-image": {"richie": "{{ RICHIE_DOCKER_IMAGE }}"},
    "init": ["mysql", "richie", "richie-openedx"],
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename("tutorrichie", "patches")
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
