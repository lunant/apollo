try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import doctest
import unittest


def run_tests():
    """Run all doctests."""
    from werkzeug import find_modules
    modules = find_modules("apollo", include_packages=True, recursive=True)
    tests = unittest.TestSuite()
    for module in modules:
        tests.addTests(doctest.DocTestSuite(module))
    return tests


setup(name="apollo",
      version="0.1",
      url="http://github.com/lunant/apollo",
      license="MIT",
      author="Minhee Hong",
      author_email="dahlia" "@" "lunant.net",
      description="Yet another web framework based on Werkzeug and Jinja2.",
      platforms="any",
      packages=["apollo"],
      install_requires=["Werkzeug>=0.6.2", "Jinja2>=2.5.4"],
      extras_require={"doc": ["Sphinx>=1.0.4"]},
      test_suite="__main__.run_tests"
)

