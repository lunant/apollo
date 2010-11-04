""":mod:`apollo.routing` --- Extended :mod:`werkzeug.routing`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apollo slightly extends Werkzeug_'s :mod:`routing <werkzeug.routing>` module.

.. _Werkzeug: http://werkzeug.pocoo.org/

"""
import werkzeug.routing
import werkzeug.datastructures
from werkzeug.routing import *


DEFAULT_CONVERTERS = {}
DEFAULT_CONVERTERS.update(werkzeug.routing.DEFAULT_CONVERTERS)


class Map(werkzeug.routing.Map):

    __doc__ = werkzeug.routing.Map.__doc__

    default_converters = werkzeug.datastructures \
                                 .ImmutableDict(DEFAULT_CONVERTERS)

