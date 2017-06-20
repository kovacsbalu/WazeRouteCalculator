# -*- coding: utf-8 -*-

import WazeRouteCalculator as wrc
import mock
import requests_mock


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

    def test_get_route_eu(self):
        self.routing_req = self.waze_url + "row-RoutingManager/routingRequest"
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "", "EU")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_route_us(self):
        self.routing_req = self.waze_url + "RoutingManager/routingRequest"
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "", "US")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_route_na(self):
        """NA (North America) is an alias for US (United States)"""
        self.routing_req = self.waze_url + "RoutingManager/routingRequest"
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "", "na")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_route_il(self):
        self.routing_req = self.waze_url + "il-RoutingManager/routingRequest"
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "", "il")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_route(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_all_routes(self):
        length2, time2 = (410, 62)
        self.routing_response = '{"alternatives":[{"response":{"results":[{"length":%s,"crossTime":%s}]}},{"response":{"results":[{"length":%s,"crossTime":%s}]}}]}' % (self.length, self.time, length2, time2)
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route(3)
        assert response == [{"results": [{"length": self.length, "crossTime": self.time}]}, {"results": [{"length": length2, "crossTime": time2}]}]
        assert self.routing_req in m.request_history[2].url

    def test_get_route_only_one(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route(3)
        assert response == [{"results": [{"length": self.length, "crossTime": self.time}]}]
        assert self.routing_req in m.request_history[2].url

    def test_add_up_route(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        results = [{"length": 1000, "crossTime": 120}, {"length": 1000, "crossTime": 120}]
        time, dist = route._add_up_route(results)
        assert time == 4.00
        assert dist == 2.00

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

    def test_calc_all_routes_info(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value=[{"routeName": "1", "results": [{"length": 1000, "crossTime": 120}]}, {"routeName": "2", "results": [{"length": 1100, "crossTime": 150}]}])
        route.get_route = route_mock
        results = route.calc_all_routes_info()
        assert route_mock.called
        assert results == {"1": (2.0, 1.0), "2": (2.5, 1.1)}

    def test_calc_all_routes_info_only_one(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value=[{"routeName": "1", "results": [{"length": 1000, "crossTime": 120}]}])
        route.get_route = route_mock
        results = route.calc_all_routes_info()
        assert route_mock.called
        assert results == {"1": (2.0, 1.0)}

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

    def test_silent_logging(self):
        from_address = 'From address'
        to_address = 'To address'
        route = wrc.WazeRouteCalculator(from_address, to_address, log_lvl=None)
        assert route.log.getEffectiveLevel() == wrc.logging.WARNING
