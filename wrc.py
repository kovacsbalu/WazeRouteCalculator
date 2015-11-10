#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import urllib


class WazeRouteCalculator(object):

    WAZE_URL = "https://www.waze.com/"

    def __init__(self, start_address, end_address, log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_lvl)
        self.log.addHandler(logging.StreamHandler())
        self.log.info("From: %s - to: %s" % (start_address, end_address))

        self.start_coords = self.address_to_coords(start_address)
        self.log.debug('Start coords: (%s, %s)' % (self.start_coords["lon"], self.start_coords["lat"]))
        self.end_coords = self.address_to_coords(end_address)
        self.log.debug('End coords: (%s, %s)' % (self.end_coords["lon"], self.end_coords["lat"]))

    def address_to_coords(self, address):
        GET_CORDS = "SearchServer/mozi"
        url_options = {
            "q": address,
            "lang": "eng",
            "origin": "livemap",
            "lon": "19.040",
            "lat": "47.498"
        }
        response = urllib.urlopen(self.WAZE_URL + GET_CORDS, data=urllib.urlencode(url_options)).read()
        response_json = json.loads(response)[0]
        lon = response_json['location']['lon']
        lat = response_json['location']['lat']
        return {"lon": lon, "lat": lat}

    def get_route(self):
        GET_ROUTE = "row-RoutingManager/routingRequest"
        # GET_ROUTE_US_CANADA = "RoutingManager/routingRequest"
        # GET_ROUTE_ISRAEL = "il-RoutingManager/routingRequest"

        url_options = {
            "from": "x:%s y:%s bd:true" % (self.start_coords["lon"], self.start_coords["lat"]),
            "to": "x:%s y:%s bd:true" % (self.end_coords["lon"], self.end_coords["lat"]),
            "at": 0,
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": 3,
            "options": "AVOID_TRAILS:t"
        }
        response = urllib.urlopen(self.WAZE_URL + GET_ROUTE, data=urllib.urlencode(url_options)).read()
        response_json = json.loads(response)
        return response_json['alternatives'][0]['response']

    def calc_route_info(self, route):
        results = route['results']
        time = 0
        distance = 0
        for segment in results:
            time += segment['crossTime']
            distance += segment['length']
        route_time = time / 60.0
        route_distance = distance / 1000.0
        self.log.info('Time %.2f minutes, distance %.2f km.' % (route_time, route_distance))
        return route_time, route_distance


if __name__ == '__main__':
    from_address = 'Budapest, Hungary'
    to_address = 'Győr, Hungary'
    wrc = WazeRouteCalculator(from_address, to_address)
    route = wrc.get_route()
    wrc.calc_route_info(route)
