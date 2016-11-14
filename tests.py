# -*- coding: utf-8 -*-

import WazeRouteCalculator as wrc
import mock
import requests_mock
import StringIO


class TestWRC():

    def setup_method(self, method):
        self.waze_url = "https://www.waze.com/"
        self.address_req = self.waze_url + "SearchServer/mozi"
        self.routing_req = self.waze_url + "row-RoutingManager/routingRequest"
        self.lat = 47.4979
        self.lon = 19.0402
        self.length = 400
        self.time = 60
        self.address_to_coords_response = '[{"location":{"lat":%s,"lon":%s}}]' % (self.lat, self.lon)
        self.routing_response = '{"response":{"results":[{"length":%s,"crossTime":%s}]}}' % (self.length, self.time)

    def test_address_to_coords(self):
        from_address = 'From address'
        to_address = 'To address'
        test_address = "Testaddress"
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
            coords = route.address_to_coords(test_address)
        assert coords == {'lat': self.lat, 'lon': self.lon}
        assert m.call_count == 3

    def test_get_route(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_best_route(self):
        self.routing_response = '{"alternatives":[{"response":{"results":[{"length":%s,"crossTime":%s}]}}]}' % (self.length, self.time)
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_calc_route_info(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"results": [{"length": 1000, "crossTime": 120}]})
        route.get_route = route_mock
        time, dist = route.calc_route_info()
        assert route_mock.called
        assert time == 2.00
        assert dist == 1.00

    def xtest_full_route_calc(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
            time, dist = route.calc_route_info()
        assert len(self.url_mock.call_args_list) == 3
        assert time == 1.00
        assert dist == 0.40
