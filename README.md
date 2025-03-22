# Django Password Manager

A basic and secure password manager app build with Django, HTML, CSS, and JavaScript

### Screenshot

![](https://i.ibb.co/prZzH5v/Django-Password-Manager.png)

# AutoDjango

A Simple Python Script To Automate The Creation Of Virtual Environment And Django Project.

## Features

- Create virtual environment
- Install Django packages
- Convert HTML template into Django application

## Note

This works when you want to create a new Django project, it won't work if you're willing to update your old Django project.

### Requirements:

- Python

### Installation:

```
$ git clone https://github.com/SelmiAbderrahim/AutoDjango.git

```

### Usage:

- To create a virtual environment and activate it:

```
$ python AutoDjango.py --venv

```

or

```
$ python AutoDjango/AutoDjango.py --venv

```

- To install only Django:

```
$ python AutoDjango.py --django --project PROJECTNAME --app APPNAME

```

or

```
$ python AutoDjango/AutoDjango.py --django --project PROJECTNAME --app APPNAME

```

- To install only Django plus the usual configuration (static, templates and pther settings):

```
$ python AutoDjango.py --django --project PROJECTNAME --app APPNAME --config-media-static-templates

```

or

```
$ python AutoDjango/AutoDjango.py --django --project PROJECTNAME --app APPNAME --config-media-static-templates

```

- To enable and configure media files:

```
$ python AutoDjango.py --django --project PROJECTNAME --app APPNAME --config-media-static-templates --media

```

or

```
$ python AutoDjango/AutoDjango.py --django --project PROJECTNAME --app APPNAME --config-media-static-templates --media

```

- To install a django package:

```
$ python AutoDjango.py --django --project PROJECTNAME --app APPNAME --config-media-static-templates --media  --install-package django-unicorn django-cors-headers djangorestframework

```

or

```
$ python AutoDjango/AutoDjango.py --django --project PROJECTNAME --app APPNAME --config-media-static-templates --media  --install-package django-unicorn django-cors-headers djangorestframework

```

### Start the project:

- First we have to CD to the Main and then

```
$ python manage.py runserver
```

And create an admin user we can use

```
python manage.py createsuperuser

```
