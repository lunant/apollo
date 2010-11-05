Getting Started
===============

Requirements
------------

All you need are just Python_ 2.6 (or higher, but 3.x not supported currently)
and pip_. We recommend Python 2.7, the latest version of Python 2.x series.

.. _Python: http://python.org/
.. _pip: http://pip.openplans.org/


Installation
------------

You can install Apollo of bleeding edge version using pip.

.. sourcecode:: bash

   $ pip install git+http://github.com/lunant/apollo.git


Hello world!
------------

Here's a small but complete example application for Apollo (:file:`hello.py`)::

    import apollo.wsgi
    from apollo.routing import Map, Rule

    def greet(context, name=None):
        if name:
            return "Hello, ", name, "."
        return "Hello."

    class HelloApplication(apollo.wsgi.Application):
        rules = Map([
            Rule("/", endpoint=greet),
            Rule("/<name>", endpoint=greet)
        ])

    if __name__ == "__main__":
        from werkzeug.serving import run_simple
        run_simple("", 8080, HelloApplication())

The above small program greets when the user requests the application.

You can run this program directly.

.. sourcecode:: bash

   $ python hello.py
    * Running on http://localhost:8080/

Then go http://localhost:8080/ in your web browser!

