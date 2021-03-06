""":mod:`shorturl` --- Apollo-powered URL shortener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is an example web application powered by Apollo.

"""
import anydbm
import random
import os.path
import werkzeug.utils
import werkzeug.exceptions
import apollo.wsgi
from apollo.routing import Map, Rule
from apollo import template


class Slug(object):
    """Slug-URL pair.

    .. data:: ALPHABETS

       The list of alphabets used for autogenerating slugs.

    .. attribute:: slug

       The slug string.

    .. attribute:: url

       The URL mapped to the slug.

    """

    ALPHABETS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                "0123456789"

    __slots__ = "slug", "url", "autogenerated"

    def __init__(self, slug, url):
        self.slug = slug
        self.url = url
        self.autogenerated = False

    def is_empty(self):
        """The predicate method that tests whether its slug is empty.

        :returns: ``True`` if its slug is empty.

        """
        return bool(self.slug.strip())

    def generate(self):
        """Fills :attr:`slug` attribute into autogenerated slug."""
        if self.is_empty() or self.autogenerated is True:
            self.slug = "".join(random.choice(self.ALPHABETS)
                                for _ in xrange(6))
            self.autogenerated = True
        else:
            if self.autogenerated:
                length = 0
            else:
                length = len(str(self.autogenerated)) + 1
            self.autogenerated += 1
            self.slug = "{0}-{1}".format(self.slug[:-length],
                                         self.autogenerated)


@template.use("index")
def index(context, created_slug=None):
    """Home page."""
    url = created_slug and context.request.host_url + created_slug.slug
    return template.Result(created_slug=created_slug, created_url=url)


def shorten(context):
    """Shortens the given URL."""
    url = context.form["url"]
    slug = Slug(context.form.get("slug", "").strip(), url)
    if slug.is_empty():
        slug = slug.generate()
    try:
        dbm = application.open_dbm()
        while slug.slug in dbm:
            slug.generate()
        dbm[slug.slug] = slug.url
        return index(context, created_slug=slug)
    except:
        raise
    finally:
        application.close_dbm()


def expand(context, slug):
    """Redirects the user agent."""
    try:
        dbm = application.open_dbm()
        if slug in dbm:
            return werkzeug.redirect(dbm[slug], code=301)
        raise werkzeug.exceptions.NotFound()
    except:
        raise
    finally:
        application.close_dbm()



class ShortUrlApplication(apollo.wsgi.Application):
    """URL shortener application."""

    rules = Map([
        Rule("/", endpoint=index, methods=["GET"]),
        Rule("/", endpoint=shorten, methods=["POST"]),
        Rule("/<slug>", endpoint=expand, methods=["GET"])
    ])

    template_path = os.path.join(os.path.dirname(__file__), "templates")

    def open_dbm(self):
        if not hasattr(self, "dbm") or not self.dbm:
            self.dbm = anydbm.open(self.dbm_filename, "c")
        return self.dbm

    def close_dbm(self):
        if hasattr(self, "dbm"):
            if self.dbm and hasattr(self.dbm, "close"):
                self.dbm.close()
            del self.dbm


if __name__ == "__main__":
    import sys
    import werkzeug.serving
    dbm_filename = sys.argv[1] if len(sys.argv) > 1 else "shorturl"
    application = ShortUrlApplication(dbm_filename="shorturl")
    port = sys.argv[2] if len(sys.argv) > 2 else 8080
    werkzeug.serving.run_simple("", port, application)

