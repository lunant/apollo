""":mod:`apollo.wsgi` --- WSGI application interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import werkzeug.wrappers
import werkzeug.routing
import werkzeug.utils
import werkzeug.exceptions
import apollo.routing
import apollo.handler


class Request(werkzeug.wrappers.Request):

    __doc__ = werkzeug.wrappers.Request.__doc__


class Response(werkzeug.wrappers.Response):

    __doc__ = werkzeug.wrappers.Response.__doc__


class Application(object):
    """WSGI application base class to be subclassed. Its instances are
    callable and WSGI compatible. ::

        impprt apollo.wsgi
        from apollo.routing import Map, Rule

        class MyApplication(apollo.wsgi.Application):
            '''My WSGI application.'''

            rules = Map([
                Rule("/")
            ])

    After you instantiate it, its instance can be a WSGI application. ::

        from wsgiref.simple_server import make_server
        application = MyApplication()
        httpd = make_server("", 8080, application)
        httpd.serve_forever()

    :param \*\*extra_options: application specific extra options.


    .. data:: rules

       The sequence of URL rules or a :class:`~apollo.routing.Map` (which is
       subtype of :class:`werkzeug.routing.Map`) of it.

       It can be overridable and should be overridden.

    """

    rules = apollo.routing.Map()

    def __init__(self, **extra_options):
        if isinstance(self.rules, collections.Iterable):
            self.rules = apollo.routing.Map(self.rules)
        elif isinstance(self.rules, werkzeug.routing.Map):
            self.rules = self.rules
        else:
            cls = type(self)
            mod = cls.__module__
            clsname = "" if mod == "__name__" else (mod + ".") \
                    + cls.__name__
            raise TypeError("{0}.rules must be a werkzeug.routing.Map "
                            "instance or an iterable object, not "
                            "{1!r}".format(clsname, self.rules))
        for attr, val in extra_options.iteritems():
            setattr(self, attr, val)

    def __call__(self, environ, start_response):
        adapter = self.rules.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            request = Request(environ)
            context = apollo.handler.Context(request, self, adapter)
            if isinstance(endpoint, basestring):
                endpoint = werkzeug.utils.import_string(endpoint)
            if callable(endpoint):
                response = endpoint(context, **values)
                if not isinstance(response, werkzeug.wrappers.BaseResponse):
                    if not isinstance(response, collections.Iterable):
                        raise TypeError("response must be a werkzeug.wrappers."
                                        "Response instance or an iterable "
                                        "object, not " + repr(response))
                    elif isinstance(response, basestring):
                        response = response,
                    response = Response(response, content_type="text/html")
            else:
                raise TypeError("endpoint must be callable; " + repr(endpoint))
        except werkzeug.exceptions.HTTPException as e:
            response = e
        return response(environ, start_response)

