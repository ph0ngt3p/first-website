# Movie Database
> Basic movie database website using Python-Flask.

[![Python Version][python-image]][python-url]

## Environment setup

Ubuntu documentation:

[https://pythonprogramming.net/creating-first-flask-web-app/](https://pythonprogramming.net/creating-first-flask-web-app/)

Installing requirements:

```sh
pip install -r requirement.txt
```

## API
```sh
/api/actors
/api/actors/(id)
/api/actors&orderby=(key)&descending=(true/false)
/api/actors/search?string=(string)
/api/actors/search?string=(string)&orderby=(key)&descending=(true/false)
/api/movies
/api/movies/(id)
/api/movies&orderby=(key)&descending=(true/false)
/api/movies?genre=(genre)(year/rated)
/api/movies?genre=(genre)&orderby=(key)&descending=(true/false)
/api/movies/search?string=(string)&genre=(genre)&year=(year)&rated=(rated)
/api/movies/search?string=(string)&genre=(genre)&year=(year)&rated=(rated)&orderby=(key)&descending=(true/false)
```

## Release History

* 0.2.1
    * REST API

* 0.1.0
    * Added more JQuery functions

* 0.0.1
    * Work in progress

## Author

Tuan Dzung – zun1903@gmail.com

[https://github.com/ph0ngt3p](https://github.com/ph0ngt3p)

[python-image]: https://img.shields.io/pypi/pyversions/Django.svg?style=flat-square
[python-url]: https://www.python.org