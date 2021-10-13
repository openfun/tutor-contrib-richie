Richie plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================

This is a plugin to integrate `Richie <https://richie.education/>`__, the learning portal CMS, with `Open edX <https://open.edx.org>`__. The integration takes the form of a `Tutor <https://docs.tutor.overhang.io>`__ plugin.

Installation
------------

::

    pip install tutor-richie
    tutor plugins enable richie

Running the Richie plugin will require that you rebuild the "openedx" Docker image::

    tutor config save
    tutor images build openedx

This step is necessary to install the Richie connector app in edx-platform.

Then, the platform can be launched as usual with::

    tutor local quickstart

You will be able to access your course catalog at http(s)://courses.LMS_HOST. In development, this url will be http://courses.local.overhang.io.

Gettting started
----------------

Once your Richie platform is up and running, you will quickly realize that your learning portal is empty. This is because you should first create the corresponding courses and organizations from inside Richie. To do so, start by creating a super user::

    tutor local run richie ./sandbox/manage.py createsuperuser

You can then use the credentials you just created at http(s)://yourrichiehost/admin. In development, this is http://courses.local.overhang.io/admin.

Then, refer to the official `Richie documentation <https://richie.education/docs/quick-start>`__ to learn how to create courses and organizations.

You may also want to fill your learning portal with a demo site -- but be careful not to run this command in production, as it will be difficult to get rid of the demo site afterwards::

    # WARNING: do not attempt this in production!
    tutor local run richie ./sandbox/manage.py create_demo_site --force

Configuration
-------------

This Tutor plugin comes with a few configuration settings:

- ``RICHIE_RELEASE_VERSION`` (default: ``"v2.8.2"``)
- ``RICHIE_HOST`` (default: ``"courses.{{ LMS_HOST }}"``)
- ``RICHIE_MYSQL_DATABASE`` (default: ``"richie"``)
- ``RICHIE_MYSQL_USERNAME`` (default: ``"richie"``)
- ``RICHIE_ELASTICSEARCH_INDICES_PREFIX`` (default: ``"richie"``)

These defaults should be enough for most users. To modify any one of them, run::

    tutor config save --set RICHIE_SETTING_NAME=myvalue

For instance, to customize the domain name at which Richie will run::

    tutor config save --set "RICHIE_HOST=mysubdomain.{{ LMS_HOST }}"

Development
-----------

Bind-mount volume::

    tutor dev bindmount richie /app/richie

Then, run a development server::

    tutor dev runserver --volume=/app/richie richie

The Richie development server will be available at http://courses.local.overhang.io:8003.

Troubleshooting
---------------

Do you need help with this plugin? Get in touch with the maintainers of Richie by opening a GitHub issue: https://github.com/openfun/richie/issues/

License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__. It was developed and is being actively maintained thanks to the sponsorship of `France Université Numérique <https://github.com/openfun>`__.

.. image:: https://www.fun-mooc.fr/static/richie/images/logo.png
  :alt: France Université Numérique
  :target: https://fun-mooc.fr
