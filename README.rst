Small playground project created at DjangoCon Europe 2015 in Cardiff.

Basically, it shows how Swampdragon adds the "real-time" element to a progressbar that originally used polling to get
the progress on a Celery task.

Installation
============

1. Navigate to the location where you want to place your project.

2. Get the code::

    $ git clone ssh://git@github.com/joeribekker/celeryswamp-demo
    $ cd celeryswamp-demo

3. Create virtual environment, install requirements and setup database::

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py migrate

4. Power it up::

    $ python manage.py runserver
    $ python server.py

