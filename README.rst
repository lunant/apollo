Apollo, an yet another web framework
====================================

**Apollo** is an yet another Python_ web framework based on Werkzeug_ and
Jinja2_, made by and for Lunant_.

There are good microframeworks also based on Werkzeug and Jinja2 like
Flask_ already, but Apollo is not much influenced from Flask. It's intended
to be a highly configurable and strongly integrated web framework for larger
web applications rather than a microframework for smaller web applications.

.. _Python: http://python.org/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/
.. _Lunant: http://lunant.com/
.. _Flask: http://flask.pocoo.org/


Key features
------------

- Interface similar to Tornado_/Google App Engine webapp_
- Werkzeug-powered rich HTTP/WSGI utilities
- Jinja2-powered expressive HTML/XML templating (autoescaping_ by default)
- Highly-integrated components

.. _Tornado: http://www.tornadoweb.org/
.. _webapp: http://code.google.com/appengine/docs/python/tools/webapp/
.. _autoescaping: http://jinja.pocoo.org/api/#autoescaping


Getting Started
---------------

You can install its bleeding edge version from Git repository via pip_::

    $ pip install git+http://github.com/lunant/apollo.git

It heavily depends on Werkzeug_ and Jinja2_, but no problem. pip_ resolves
its dependencies automatically also.

.. _pip: http://pip.openplans.org/

