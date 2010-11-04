""":mod:`apollo.handler` --- Request handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


class take_application(object):
    """A decorator that makes ``function`` to take an
    :class:`~apollo.wsgi.Application` instance as its first argument.
    
    ::

        from apollo.handler import take_application
        from apollo.wsgi import Application

        @take_application
        def handle(application, request):
            '''Handle requests.'''
            assert isinstance(application, Application)
            return "response"

    :param function: a function to make to take an application instance as
                     its first argument.
    :type function: callable object
    :param application: an optional application to bind
    :type application: :class:`~apollo.wsgi.Application`

    """

    __slots__ = "function", "application"

    def __init__(self, function, application=None):
        from apollo.wsgi import Application
        if not callable(function):
            raise TypeError("function must be callable, but {0!r} "
                            "passed".format(function))
        elif not (application is None or isinstance(application, Application)):
            raise TypeError("application must be an apollo.wsgi.Application "
                            "instance, not " + repr(application))
        self.function = function
        self.application = application

    def bind(self, application):
        """Returns a application-bound function.

        .. sourcecode:: pycon

           >>> @take_application
           ... def handle(application, request):
           ...     pass
           ...
           >>> handle.application
           >>> from apollo.wsgi import Application
           >>> handle.bind(Application()).application  # doctest: +ELLIPSIS
           <apollo.wsgi.Application object at ...>

        :param application: an application to bind
        :type application: :class:`~apollo.wsgi.Application`

        """
        return type(self)(self.function, application)

    def __call__(self, *args, **kwargs):
        if self.application:
            return self.function(self.application, *args, **kwargs)
        return self.function(*args, **kwargs)

