Getting Started
===============

Here's a small but complete example application for Apollo::

    import apollo.wsgi
    from apollo.routing import Map, Rule

    def greet(request, name=None):
        if name:
            return "Hello, ", name, "."
        return "Hello."

    class HelloApplication(apollo.wsgi.Application):
        rules = Map([
            Rule("/", endpoint=greet),
            Rule("/<name>", endpoint=greet)
        ])

    if __name__ == "__main__":
        from wsgiref.simple_server import make_server
        httpd = make_server("", 8080, HelloApplication())
        httpd.serve_forever()

The above small program greets when the user requests the application.

