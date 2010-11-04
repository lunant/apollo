try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


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
      extras_require={"doc": ["Sphinx>=1.0.4"]})

