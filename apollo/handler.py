""":mod:`apollo.handler` --- Request handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import werkzeug.wrappers
import apollo.routing


class Context(collections.namedtuple("Ctx", "request application map_adapter")):
    """The :func:`~collections.namedtuple` type that represents a request
    context.
    
    It has three tuple fields in order: :attr:`request`, :attr:`application`
    and :attr:`map_adapter`::

        assert isinstance(context, Context)
        request, application, map_adapter = context

    :param request: a request object
    :type request: :class:`~apollo.wsgi.Request`,
                   :class:`werkzeug.BaseRequest`
    :param application: an application instance
    :type application: :class:`~apollo.wsgi.Application`
    :param map_adapter: a map adapter instance
    :type map_adapter: :class:`apollo.routing.MapAdapter
                       <werkzeug.routing.MapAdapter>`

    .. attribute:: request

       The instance of :class:`~apollo.wsgi.Request` which is a subclass of
       :class:`werkzeug.BaseRequest`. (The first field of the tuple.)

    .. attribute:: application

       The :class:`~apollo.wsgi.Application` instance. (The second field of
       the tuple.)

    .. attribute:: map_adapter

       The :class:`apollo.routing.MapAdapter <werkzeug.routing.MapAdapter>`
       instance. (The third field of the tuple.)

    """

    def __new__(cls, request, application, map_adapter):
        if not isinstance(request, werkzeug.wrappers.BaseRequest):
            raise TypeError("request must be an instance of apollo.wsgi."
                            "Request or werkzeug.wrappers.BaseRequest object, "
                            "not " + repr(request))
        from apollo.wsgi import Application
        if not isinstance(application, Application):
            raise TypeError("application must be an apollo.wsgi.Application "
                            "instance, not " + repr(application))
        elif not isinstance(map_adapter, apollo.routing.MapAdapter):
            raise TypeError("map_adapter must be an instance of apollo."
                            "routing.MapAdapter (which is werkzeug.routing."
                            "MapAdapter), not " + repr(map_adapter))
        BaseContext = Context.__bases__[0]
        return BaseContext.__new__(cls, request, application, map_adapter)

    @property
    def app(self):
        """Alias of :attr:`application`."""
        return self.application

    @property
    def args(self):
        """Alias of :attr:`request.args <werkzeug.BaseRequest.args>`."""
        return self.request.args

    @property
    def form(self):
        """Alias of :attr:`request.form <werkzeug.BaseRequest.form>`."""
        return self.request.form

    @property
    def values(self):
        """Combined :class:`~werkzeug.ImmutableMultiDict` for :attr:`args`
        and :attr:`form`. Alias of :attr:`request.values
        <werkzeug.wrappers.values>`.

        """
        return self.request.values

