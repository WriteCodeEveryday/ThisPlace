#!/usr/bin/env python

import bottle
from bottle import (
    get,
    run,
    abort,
    static_file,
    template
)

import thisplace


example_locs = [("sydney", (-33.867480754852295, 151.20700120925903)),
                ("battery", (40.70329427719116, -74.0170168876648)),
                ("san_fran", (37.790114879608154, -122.4202036857605))]
example_locs = dict((name, thisplace.four_words(pos)) for name,pos in example_locs)

@get('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static')


@get('/')
def index():
    return template('map', lat=None, lng=None)


# @get('/help.html')
# def help():
#     return template('help', err=None, **example_locs)


@get('/<fourwords>')
def showMap(fourwords):
    try:
        lat, lng = thisplace.decode(fourwords)
        return template('map', lat=lat, lng=lng, fourwords=fourwords)
    except:
        return template('help',
                        err="Could not find location {}".format(fourwords),
                        **example_locs)


@get('/latlng/<lat:float>,<lng:float>')
def showMapFromLatLng(lat, lng):
    try:
        fourwords = thisplace.four_words((lat, lng))
        return template('map', lat=lat, lng=lng, fourwords=fourwords)
    except:
        return template('index',
                        err="Could not find location {}".format(fourwords),
                        **example_locs)


# API
@get('/api/<lat:float>,<lng:float>')
def latLngToHash(lat, lng):
    try:
        three = thisplace.three_words((lat, lng))
        four = thisplace.four_words((lat, lng))
        six = thisplace.six_words((lat, lng))
        return {'three': three, 'four': four, 'six': six}
    except Exception:
        return {}


@get('/api/<fourwords>')
def hashToLatLng(fourwords):
    try:
        lat, lng = thisplace.decode(fourwords)
        return {"lat": lat, "lng": lng}
    except:
        abort(404)

@get('/.well-known/acme-challenge/JgePqyxFcoPO3EvGrK5ZvYj4x25WR-3xwyGvQJ59e1s')
def tp_without_www():
    return 'JgePqyxFcoPO3EvGrK5ZvYj4x25WR-3xwyGvQJ59e1s.qmQ7Ba17QUSzsS58ZGPuVaAjT2_QTE_bU1UvqETPGbs'

@get('/.well-known/acme-challenge/BwTYpFmdfh6C3VVGXoIMSyzlsdhkDeEIqjqYotzcjd4')
def tp_with_www():
    return 'BwTYpFmdfh6C3VVGXoIMSyzlsdhkDeEIqjqYotzcjd4.qmQ7Ba17QUSzsS58ZGPuVaAjT2_QTE_bU1UvqETPGbs'

if __name__ == '__main__':
    run(host='localhost', port=8080)

app = bottle.default_app()
