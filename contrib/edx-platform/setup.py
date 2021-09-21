import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


setup(
    name="richie-edx-platform",
    version="0.0.1",
    url="https://github.com/overhangio/tutor-richie/",
    project_urls={
        "Code": "https://github.com/overhangio/tutor-richie/tree/master/contrib/edx-platform",
        "Issue tracker": "https://github.com/overhangio/tutor-richie/issues",
    },
    license="AGPLv3",
    author="Overhang.IO",
    description="Open edX plugin app for integration with a Richie catalog",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    entry_points={
        "lms.djangoapp": [
            "richie = richie.apps:RichieAppConfig",
        ],
        "cms.djangoapp": [
            "richie = richie.apps:RichieAppConfig",
        ],
    },
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
