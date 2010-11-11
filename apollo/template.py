""":mod:`apollo.template` --- Templating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import werkzeug.datastructures
import jinja2


class Result(werkzeug.datastructures.ImmutableDict):
    """The result dictionary for templating, which is immutable.

    It combines key-value pairs for templating and a single :attr:`value`
    (``__value__``) for serialization formats like JSON_, YAML_.

    .. sourcecode:: pycon

       >>> result = Result(123, a=1, b=2, c=3)
       >>> result
       apollo.template.Result(123, a=1, b=2, c=3)
       >>> result.value
       123

    The argument ``__value__`` of the constructor can be omitted. In these
    case, :attr:`value` returns just itself.

    .. sourcecode:: pycon

       >>> result = Result(a=1, b=2)
       >>> result
       apollo.template.Result({'a': 1, 'b': 2})
       >>> result.value
       apollo.template.Result({'a': 1, 'b': 2})

    :param __value__: A single value for serialization formats, or a mapping
                      object. Default is ``{}``.
    :param \*\*items: Dictionary items.

    .. _JSON: http://www.json.org/
    .. _YAML: http://www.yaml.org/


    .. attribute:: __value__

       Alias of :attr:`value`.

    """

    __slots__ = "_value",

    def __init__(self, __value__={}, **items):
        if isinstance(__value__, Result):
            items.update(__value__)
            __value__ = __value__.value
        try:
            dict.__init__(self, __value__, **items)
        except TypeError:
            dict.__init__(self, **items)
            self._value = __value__

    @property
    def value(self):
        """The value for serialization formats e.g. JSON_, YAML_.

        .. _JSON: http://www.json.org/
        .. _YAML: http://www.yaml.org/

        """
        try:
            return self._value
        except AttributeError:
            return self

    __value__ = value

    def __repr__(self):
        name = object.__repr__(self).split(" ", 1)[0][1:]
        try:
            self._value
        except AttributeError:
            return "{0}({1})".format(name, dict.__repr__(self))
        else:
            if self:
                items = self.items()
                items.sort(key=lambda (k, v): k)
                dictrepr = ", ".join("{0}={1!r}".format(*i) for i in items)
                return "{0}({1!r}, {2})".format(name, self._value, dictrepr)
            return "{0}({1!r})".format(name, self._value)


class TemplateResult(Result):
    """Template-bound result dictionary.
    
    .. todo:: To be more documented.

    """

    __slots__ = "template_name",

    def __init__(self, __template__, __value__={}, **items):
        Result.__init__(self, __value__, **items)
        self.template_name = __template__

    def __repr__(self):
        name = object.__repr__(self).split(" ", 1)[0][1:]
        tpl = self.template_name
        try:
            val = self._value
        except AttributeError:
            return "{0}({1!r}, {2})".format(name, tpl, dict.__repr__(self))
        else:
            if self:
                items = self.items()
                items.sort(key=lambda (k, v): k)
                dictrepr = ", ".join("{0}={1!r}".format(*i) for i in items)
                return "{0}({1!r}, {2!r}, {3})".format(name, tpl, val, dictrepr)
            return "{0}({1!r}, {2!r})".format(name, tpl, val)


class use_template(object):
    """The decorator that marks a function to use the template.

    .. todo:: To be more documented.
    
    """

    __slots__ = "template_name",

    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, function):
        def decorated(*args, **kwargs):
            result = function(*args, **kwargs)
            if not isinstance(result, TemplateResult):
                result = TemplateResult(self.template_name, result)
            return result
        return decorated


use = use_template

