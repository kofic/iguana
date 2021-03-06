# Iguana
![Test Coverage](https://jenkins.computermokel.de/badges/coverage.svg?maxAge=300)

## Description
Iguana is a mixture of a ticket system, an issue tracker and an issue management system, heavily based on basic functions being easy to use. So Iguana can help you to plan the next schedule and have always a nice overview about your current tasks depending on your needs, especially for working in groups. There is a kanban board to keep an eye on the progress until the end of the next planning stage and also a backlog to have the ability for scheduling of long-terms. In combination with a mechanism to log time spent on different tasks individually those are the essential functionalities.

For more detailed documentation including a list of features see our github documentation page at https://iguana-project.github.io.


## Installation

### Docker
You can use docker to run iguana in production. The docker-compose file comes with automated letsecnrypt certificate generation.
* adapt `docker/settings.json`:
  * SECRET_KEY and HOST/ALLOWED_HOSTS
  * email: either use a sendgrid api key or a normal mail server
* adapt the env variables of the web service in `docker-compose.yml`
* run `sudo docker-compose up`

### Production
To setup Iguana in a production environment you simply have to call:

    make production

This command runs the following Makefile targets:

* `setup-virtualenv`
* `initialize-settings`
* `css`

### Staging
To setup Iguana in a staging environment you simply have to call:

    make staging

This command runs the following Makefile targets:
* `setup-virtualenv stage`
* `initialize-settings`
* `css`

### Development
To setup Iguana in a development you simply have to call:

    make development [<webdriver>]

The `<webdriver>` option the driver for the `setup-webriver` target can be specified. Beside that the following targets are executed:

* `setup-virtualenv dev`
* `initialize-settings dev`
* `css`
* `link-git-hooks`
* `setup-webdriver <webdriver>`
* `migrate`

### Starting Iguana
Currently Iguana supports only [Nginx](https://nginx.org/en/) as web server backend. For configuring Nginx and using [Gunicorn](http://gunicorn.org/) together with Django please stick to the official documentation: https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/gunicorn/

### Starting the local Iguana instance
To start the local Django web server simply run:

    make run

### Using Ansible for deployment
**TODO:** write Ansible instructions


## Makefile targets
These targets can be run with:

    make <target>

### Main targets
* **production**<br />
See subsection *Production*.
* **staging**<br />
See subsection *Staging*.
* **development**<br />
See subsection *Development*.

### Other targets

* **help**<br />
Prints a short description for each Makefile target.

* **setup-virtualenv** `[dev|stage]`<br />
This target prepares the virtual python environment in which this project is executed. The packages for the virtual environment are defined in the file `requirements/production.req`.<br />
If you want to setup the virtualenv for development (`development.req`) or staging (`staging.req`), add `dev` or `stage` option.

* **initialize-settings** `[dev]`<br />
This target sets up the settings for Iguana. By default the production or staging settings are loaded.<br />
If you want to initialize the development settings and generate a sample `SECRET_KEY` for Django, add the `dev` option.<br />
For more information about configuring Iguana see section *Configuration*.

* **css**<br />
See section *Styling*.

* **link-git-hooks**<br />
This target installs the required git hooks for contributing to the development process. The hooks can be found in the `tools/git-hooks` directory.

* **setup-webdriver** `[<webdriver>]`<br />
This target configures the webdriver for the functional tests. You can replace `<webdriver>` with `chrome`, `firefox` or `safari`. If you use this target for the first time and no driver is specified, it uses `chrome` as default. Then if there's no driver supplied, it tries to use the current one.

* **makemigrations**<br />
Create the Django migrations.

* **migrate**<br />
Apply the Django migrations to the database or create the database if no exists.

* **refresh-reqs** `[dev|stage]`<br />
Reinstall all packages in the virtual environment. If `dev` parameter is specified, the development requirements (`requirements/development.req`) will be installed. For `stage` the staging (`requirements/staging.req`) and if no parameter is provided, the production requirements (`requirements/production.req`) are reinstalled.

* **startapp** `<appname>`<br />
Create a new Django application with the specified name.

* **test** `[<appname>]`<br />
Run the Django unit tests. If an application name is provided, only that app is tested. To run the functional tests call `test functional_tests[.appname]`.

* **run**<br />
Run the default django server.

* **make-messages** `<lang-code>`<br />
See section *Translation*.

* **compile-messages**<br />
Compile the Django messages.

* **coverage** `[<appname>]`<br />
Run the coverage tool on the Django tests. To get a better output you can run one of the following commands:
    * **coverage-report**<br />
    Get the coverage in text form.
    * **coverage-html**<br />
    Get the coverage as a html website.
    * **coverage-xml**<br />
    Get the coverage as a xml file.

* **coverage-erase**<br />
Delete the last coverage report.

* **list_bugs**<br />
List all occurrence of the tag `TODO BUG`.

* **list_missing_testcases**<br />
List all occurrence of the tag `TODO TESTCASE`.

* **add_license_header**<br />
Insert the license header into all source files.

* **check_requirements**<br />
Check whether our requirements are up to date or not.


### Styling
Currently the style is stored in `config/scss/style.scss`. To build it run
`make css`. For Selenium tests use `StaticLiveServerTestcase` instead of
`LiveServerTestcase` to make sure static files (like css) are served.

Documentation on Sass and SCSS: http://sass-lang.com/guide

I propose we use SCSS, as it is a superset of CSS and the default Sass syntax.
If we change our mind, there are tools to convert between the two syntaxes.

### Translation
Please use translation hooks in templates (see `\_base.html` for an example)
and code (`ugettext` as `_`).

You can create/update the `*.po` in the locale directory by running `make-messages <lang-code>`. The default language is English (code: en). This file is where the actual translations go. It should be checked
in after updating. This uses the GNU gettext toolset.

For new translations to be usable by django, run `make compilemessages`.

To see a page in a different language, open it with a different language prefix
in the url. For example `/de/login` instead of `/en/login`.


## Configuration
Iguana has a lot of settings that can be changed by the user. The settins files are stored in the `common/settings` package. The package structure is:

```
common/settings
          |- __init__.py
          |- common.py
          |- global_conf.py
          |- local_conf.py
```


#### \_\_init\_\_.py
A default init-file gets created by the Makefile target **initialize-settings** (see section *Makefile targets*).<br />
For the development process this file can contain additional settings that should not be published in the repository. Mainly the Django-`SECRET_KEY = '...'` setting is defined here, when the project is in the development environment.<br />
**Important:** The file must start with the line:

```python
from <site_config> import *
```

You can replace `<site_config>` with (don't forget the '**.**'):
* `.local_conf`: the development settings are loaded
* `.global_conf`: the production and staging settings are loaded

#### common.py
This file contains the basic settings that are the same for the other two configuration files.<br />
**This file should not be changed by the user!** It contains basic settings for the Django framework. Changing these settings without knowing what you do could lead to unexpected behaviour.

#### global_conf.py
Basically this file contains all settings that are required to run Iguana in an staging or production environment.<br />
But the settings that should be changed by the user are loaded from the file `/var/lib/iguana/settings/settings.json`. This file gets created when installing Iguana through Ansible. A template for this file can be found in `ansible/roles/user/files/settings_template.json`.

#### local_conf.py
This file contains all settings that are required to run Iguana in a development environment.<br />
Normally there's no need to change these settings.


## License
Iguana was mainly developed with the Django framework (https://www.djangoproject.com).


### Main license
**Iguana is licensed under the CC-BY-SA license:**
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>. Since we use the version 4 of CC-BY-SA there is not necessarily an incompatibility with GPL - see <a href="https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software">Can I apply a Creative Commons license to software?</a> and <a href="https://wiki.creativecommons.org/wiki/ShareAlike_compatibility:_GPLv3">ShareAlike compatibility: GPLv3</a>. If you see any problems that are caused by that CC-BY-SA license tell us and we might find a solution.

<!-- Header for all source files -->
<!-- Iguana (c) by Marc Ammon, Moritz Fickenscher, Lukas Fridolin,
Michael Gunselmann, Katrin Raab, Christian Strate

Iguana is licensed under a
Creative Commons Attribution-ShareAlike 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>. -->


### Plug-in licenses
Besides the following plug-ins were used:

| Plug-in / Software | License |
| ------------------ | ------- |
| [bleach](https://github.com/mozilla/bleach) | [Apache License 2.0](https://github.com/mozilla/bleach/blob/master/LICENSE) |
| [celery](http://docs.celeryproject.org/en/latest/) | [BSD License](http://docs.celeryproject.org/en/latest/) |
| [chromedriver](https://github.com/enkidulan/chromedriver) | Apache License 2.0 |
| [coverage](https://coverage.readthedocs.io) | [Apache License 2.0](https://github.com/nedbat/coveragepy/blob/master/LICENSE.txt) |
| [Django](https://www.djangoproject.com) | [BSD License](https://github.com/django/django/blob/master/LICENSE) |
| [django-activity-stream](https://django-activity-stream.readthedocs.io) | [BSD License](https://github.com/justquick/django-activity-stream/blob/master/LICENSE.txt) |
| [django-autocomplete-light](https://django-autocomplete-light.readthedocs.io) | [MIT License](https://github.com/yourlabs/django-autocomplete-light/blob/master/LICENSE) |
| [django-bootstrap3](https://django-bootstrap3.readthedocs.io) | [Apache License 2.0](https://github.com/dyve/django-bootstrap3/blob/master/LICENSE) |
| [django-cuser](https://github.com/Alir3z4/django-cuser) | [BSD License](https://github.com/Alir3z4/django-cuser/blob/master/LICENSE) |
| [django-datetime-widget](https://github.com/asaglimbeni/django-datetime-widget) | [BSD License](https://github.com/asaglimbeni/django-datetime-widget/blob/master/LICENSE.txt) |
| [django-extensions](https://django-extensions.readthedocs.io) | [MIT License](https://github.com/django-extensions/django-extensions/blob/master/LICENSE)
| [django-filter](https://github.com/carltongibson/django-filter) | [BSD License](https://github.com/carltongibson/django-filter/blob/develop/LICENSE) |
| [django-pagedown](https://github.com/timmyomahony/django-pagedown) | [BSD License](https://github.com/timmyomahony/django-pagedown/blob/master/LICENSE.txt) |
| [django-redis](https://github.com/niwinz/django-redis) | [BSD License](https://github.com/niwinz/django-redis/blob/master/LICENSE) |
| [djangorestframework](https://github.com/encode/django-rest-framework) | [BSD License](https://github.com/encode/django-rest-framework/blob/master/LICENSE.md) |
| [djangorestframework-jwt](https://github.com/GetBlimp/django-rest-framework-jwt) | [MIT License](https://github.com/GetBlimp/django-rest-framework-jwt/blob/master/LICENSE) |
| [django-sendfile](https://github.com/johnsensible/django-sendfile) | [BSD License](https://github.com/johnsensible/django-sendfile/blob/master/LICENSE) |
| [django-simple-captcha](https://github.com/mbi/django-simple-captcha) | [MIT License](https://github.com/mbi/django-simple-captcha/blob/master/LICENSE) |
| [django-test-without-migrations](https://github.com/henriquebastos/django-test-without-migrations/) | [MIT License](https://github.com/henriquebastos/django-test-without-migrations/blob/master/LICENSE) |
| [GitPython](https://gitpython.readthedocs.io) | [BSD License](https://github.com/gitpython-developers/GitPython/blob/master/LICENSE) |
| [gunicorn](https://gunicorn.org) | [MIT License](https://github.com/benoitc/gunicorn/blob/master/LICENSE) |
| [markdown](https://pythonhosted.org/Markdown/) | [BSD License](https://github.com/waylan/Python-Markdown/blob/master/LICENSE.md) |
| [markdown-urlize](https://github.com/r0wb0t/markdown-urlize) | [BSD License](https://github.com/r0wb0t/markdown-urlize/blob/master/LICENSE) |
| [model-mommy](https://model-mommy.readthedocs.org) | [Apache License 2.0](https://github.com/vandersonmota/model_mommy/blob/master/LICENSE) |
| [pep8](https://pep8.readthedocs.io) | [MIT License](https://github.com/PyCQA/pycodestyle/blob/master/LICENSE) |
| [Pillow](https://python-pillow.org) | [PIL Software License](https://github.com/python-pillow/Pillow/blob/master/LICENSE) |
| [piprot](https://github.com/sesh/piprot) | [MIT License](https://github.com/sesh/piprot/blob/master/LICENCE.txt) |
| [ply](http://www.dabeaz.com/ply/) | BSD License |
| [psycopg2](http://initd.org/psycopg/) | [GNU LGPL v3.0](https://github.com/psycopg/psycopg2/blob/master/LICENSE) |
| [python-dateutil](https://github.com/dateutil/dateutil/) | [BSD License](https://github.com/dateutil/dateutil/blob/master/LICENSE) |
| [pytz](https://github.com/stub42/pytz) | [MIT license](http://pythonhosted.org/pytz/#license) |
| [redis](https://github.com/antirez/redis) | [BSD License](https://github.com/antirez/redis/blob/unstable/COPYING) |
| [requests](http://docs.python-requests.org) | [Apache License 2.0](https://github.com/kennethreitz/requests/blob/master/LICENSE) |
| [selenium](http://www.seleniumhq.org) | [Apache License 2.0](https://github.com/SeleniumHQ/selenium/blob/master/LICENSE)
| [sendgrid-django](https://github.com/elbuo8/sendgrid-django) | [MIT License](https://github.com/elbuo8/sendgrid-django/blob/master/LICENSE) |
| [slackclient](https://github.com/slackapi/python-slackclient) | [MIT License](https://github.com/slackapi/python-slackclient/blob/master/LICENSE) |
