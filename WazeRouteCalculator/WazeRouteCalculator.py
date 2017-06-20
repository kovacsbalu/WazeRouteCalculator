# -*- coding: utf-8 -*-
"""Waze route calculator"""

import logging
import requests


class WRCError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WazeRouteCalculator(object):
    """Calculate actual route time and distance with Waze API"""

    WAZE_URL = "https://www.waze.com/"

    def __init__(self, start_address, end_address, region='EU', log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)
        if log_lvl is None:
            log_lvl = logging.WARNING
        self.log.setLevel(log_lvl)
        if not len(self.log.handlers):
            self.log.addHandler(logging.StreamHandler())
        self.log.info("From: %s - to: %s", start_address, end_address)

        region = region.upper()
        if region == 'NA':  # North America
            region = 'US'
        self.region = region

        self.start_coords = self.address_to_coords(start_address)
        self.log.debug('Start coords: (%s, %s)', self.start_coords["lon"], self.start_coords["lat"])
        self.end_coords = self.address_to_coords(end_address)
        self.log.debug('End coords: (%s, %s)', self.end_coords["lon"], self.end_coords["lat"])

    def address_to_coords(self, address):
        """Convert address to coordinates"""

        EU_BASE_COORDS = {"lon": 19.040, "lat": 47.498}
        US_BASE_COORDS = {"lon": -74.006, "lat": 40.713}
        IL_BASE_COORDS = {"lon": 35.214, "lat": 31.768}
        BASE_COORDS = dict(US=US_BASE_COORDS, EU=EU_BASE_COORDS, IL=IL_BASE_COORDS)[self.region]
        # the origin of the request can make a difference in the result

        get_cords = "SearchServer/mozi?"
        url_options = {
            "q": address,
            "lang": "eng",
            "origin": "livemap",
            "lon": BASE_COORDS["lon"],
            "lat": BASE_COORDS["lat"]
        }
        response = requests.get(self.WAZE_URL + get_cords, params=url_options)
        response_json = response.json()[0]
        lon = response_json['location']['lon']
        lat = response_json['location']['lat']
        return {"lon": lon, "lat": lat}

    def get_route(self, npaths=1):
        """Get route data from waze"""

        routing_req_eu = "row-RoutingManager/routingRequest?"
        routing_req_us_canada = "RoutingManager/routingRequest"
        routing_req_israel = "il-RoutingManager/routingRequest"
        routing_req = dict(US=routing_req_us_canada, EU=routing_req_eu, IL=routing_req_israel)[self.region]

        url_options = {
            "from": "x:%s y:%s" % (self.start_coords["lon"], self.start_coords["lat"]),
            "to": "x:%s y:%s" % (self.end_coords["lon"], self.end_coords["lat"]),
            "at": 0,
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": npaths,
            "options": "AVOID_TRAILS:t",
        }
        response = requests.get(self.WAZE_URL + routing_req, params=url_options)
        response_json = response.json()
        if response_json.get("error"):
            raise WRCError(response_json.get("error"))
        if response_json.get("alternatives"):
            return [alt['response'] for alt in response_json['alternatives']]
        if npaths > 1:
            return [response_json['response']]
        return response_json['response']

    def _add_up_route(self, results):
        time = 0
        distance = 0
        for segment in results:
            time += segment['crossTime']
            distance += segment['length']
        route_time = time / 60.0
        route_distance = distance / 1000.0
        return route_time, route_distance

    def calc_route_info(self):
        """Calculate best route info."""

        route = self.get_route(1)
        results = route['results']
        route_time, route_distance = self._add_up_route(results)
        self.log.info('Time %.2f minutes, distance %.2f km.', route_time, route_distance)
        return route_time, route_distance

    def calc_all_routes_info(self, npaths=3):
        """Calculate all route infos."""

        routes = self.get_route(npaths)
        results = {route['routeName']: self._add_up_route(route['results']) for route in routes}
        route_time = [route[0] for route in results.values()]
        route_distance = [route[1] for route in results.values()]
        self.log.info('Time %.2f - %.2f minutes, distance %.2f - %.2f km.', min(route_time), max(route_time), min(route_distance), max(route_distance))
        return results
