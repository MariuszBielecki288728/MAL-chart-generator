from setuptools import setup

setup(name='MAL_chart_generator',
      version='1.0',
      description='myanimelist.net infographic generator',
      author='Mariusz Bielecki',
      author_email='288728@uwr.edu.pl',
      url='https://github.com/MariuszBielecki288728/MAL-chart-generator/',
      packages=['MAL_chart_generator'],
      package_data={'MAL_chart_generator': ['templates/*.html']},
      install_requires=[
          'requests',
          'bs4',
          'progressbar',
          'matplotlib',
          'seaborn',
          'pandas',
          'dateutil',
          'jinja2']
      )
