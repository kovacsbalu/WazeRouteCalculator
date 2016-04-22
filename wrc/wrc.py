# -*- coding: utf-8 -*-
"""Waze route calculator"""

import json
import logging
try:
  import urllib2,urllib
except ImportError:
  import urllib

class WazeRouteCalculator(object):
    """Calculate actual route time and distance with waze api"""

    def __init__(self, start_address, end_address, log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_lvl)
        self.log.addHandler(logging.StreamHandler())
        self.log.info("From: %s - to: %s", start_address, end_address)

        self.start_coords = self.address_to_coords(start_address)
        self.log.debug('Start coords: (%s, %s)', self.start_coords["lon"], self.start_coords["lat"])
        self.end_coords = self.address_to_coords(end_address)
        self.log.debug('End coords: (%s, %s)', self.end_coords["lon"], self.end_coords["lat"])

    def address_to_coords(self, address):
        """Convert address to coordinates"""
        return address_to_coords(address)

    def get_route(self):
        """Get route data from waze"""
        return get_route(self.start_coords,self.end_coords)

    def calc_route_info(self):
        """Calculate best route info."""
        return calc_route_info(self.start_coords,self.end_coords,log=self.log)

def address_to_coords(address,WAZE_URL="https://www.waze.com/"):
    """Convert address to coordinates"""

    get_cords = "SearchServer/mozi"
    url_options = {
        "q": address,
        "lang": "eng",
        "origin": "livemap",
        "lon": "19.040",
        "lat": "47.498"
    }
    try:
        response = urllib2.urlopen(WAZE_URL + get_cords, data=urllib.urlencode(url_options)).read()
    except NameError:
        response = urllib.urlopen(WAZE_URL + get_cords, data=urllib.urlencode(url_options)).read()
    response_json = json.loads(response)[0]
    lon = response_json['location']['lon']
    lat = response_json['location']['lat']
    return {"lon": lon, "lat": lat}

def get_route(start_coords,end_coords,WAZE_URL="https://www.waze.com/",RoutingManager="row-RoutingManager"):
    """Get route data from waze"""

    routing_req = RoutingManager+"/routingRequest"
    # routing_req_us_canada = "RoutingManager/routingRequest"
    # routing_req_israel = "il-RoutingManager/routingRequest"

    url_options = {
        "from": "x:%s y:%s bd:true" % (start_coords["lon"], start_coords["lat"]),
        "to": "x:%s y:%s bd:true" % (end_coords["lon"], end_coords["lat"]),
        "at": 0,
        "returnJSON": "true",
        "returnGeometries": "true",
        "timeout": 60000,
        "nPaths": 1,
        "options": "AVOID_TRAILS:t"
    } #             "returnInstructions": "true",
    try:
        response = urllib2.urlopen(WAZE_URL + routing_req, data=urllib.urlencode(url_options)).read()
    except NameError:
        response = urllib.urlopen(WAZE_URL + routing_req, data=urllib.urlencode(url_options)).read()
    response_json = json.loads(response)
    if response_json.get("alternatives"):
        return response_json['alternatives'][0]['response']
    return response_json['response']

def calc_route_info(start_coords,end_coords,log=None):
    """Calculate and print best route info."""
    route_time, route_distance = calc_route_time_and_length(start_coords,end_coords)
    if log: log.info('Time %.2f minutes, distance %.2f km.', route_time, route_distance)
    return route_time, route_distance


def calc_route_time_and_length(start_coords,end_coords):
    """Compute best route info"""
    route = get_route(start_coords,end_coords)
    results = route['results']
    time = 0
    distance = 0
    for segment in results:
        time += segment['crossTime']
        distance += segment['length']
    route_time = time / 60.0
    route_distance = distance / 1000.0
    return route_time,route_distance
