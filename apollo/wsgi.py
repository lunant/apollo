""":mod:`apollo.wsgi` --- WSGI application interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import os.path
import werkzeug.wrappers
import werkzeug.routing
import werkzeug.utils
import werkzeug.exceptions
import jinja2
import apollo.routing
import apollo.handler
import apollo.template


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

    @werkzeug.utils.cached_property
    def template_environment(self):
        """:class:`jinja2.Environment` instance.

        .. todo:: To be more documented.

        """
        return jinja2.Environment(loader=self.template_loader)

    @werkzeug.utils.cached_property
    def template_loader(self):
        """:class:`jinja2.Loader` instance.
        
        .. todo:: To be more documented.

        """
        return jinja2.FileSystemLoader(self.template_path)

    @werkzeug.utils.cached_property
    def template_path(self):
        """The path of the directory that contains template files.

        .. todo:: To be documented.

        """
        mod = type(self).__module__
        if mod in ("__main__", __name__):
            return "templates"
        mod = reduce(getattr, mod.split("."), __import__(mod))
        return os.path.join(os.path.dirname(mod.__file__), "templates")

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
                if isinstance(response, apollo.template.TemplateResult):
                    template = self.template_environment.get_template(
                        response.template_name + ".html",
                        globals=dict(__context__=context)
                    )
                    response = Response(template.generate(response),
                                        content_type="text/html")
                elif not isinstance(response, werkzeug.wrappers.BaseResponse):
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

