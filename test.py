# -*- coding: utf-8 -*-

import wrc
import mock
import StringIO


class TestWRC():

    def mock_waze_api(self, url, data=None):
        urls = {self.address_req: self.address_to_coords_response,
                self.routing_req: self.routing_response}
        return StringIO.StringIO(urls[url])

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
        self.url_mock = mock.Mock()
        self.url_mock.side_effect = self.mock_waze_api
        wrc.urllib.urlopen = self.url_mock

    def test_address_to_coords(self):
        from_address = 'From address'
        to_address = 'To address'
        test_address = "Testaddress"
        route = wrc.WazeRouteCalculator(from_address, to_address)
        coords = route.address_to_coords(test_address)
        calls = self.url_mock.call_args_list
        url, data = calls[2]
        assert url[0] == self.address_req
        assert test_address in data.get("data")
        assert coords == {'lat': self.lat, 'lon': self.lon}

    def test_get_route(self):
        route = wrc.WazeRouteCalculator("", "")
        response = route.get_route()
        calls = self.url_mock.call_args_list
        url, data = calls[2]
        assert url[0] == self.routing_req
        assert str(self.lat) in data.get("data")
        assert str(self.lon) in data.get("data")
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}

    def test_get_best_route(self):
        self.routing_response = '{"alternatives":[{"response":{"results":[{"length":%s,"crossTime":%s}]}}]}' % (self.length, self.time)
        route = wrc.WazeRouteCalculator("", "")
        response = route.get_route()
        calls = self.url_mock.call_args_list
        url, data = calls[2]
        assert url[0] == self.routing_req
        assert str(self.lat) in data.get("data")
        assert str(self.lon) in data.get("data")
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}

    def test_calc_route_info(self):
        route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"results": [{"length": 1000, "crossTime": 120}]})
        route.get_route = route_mock
        time, dist = route.calc_route_info()
        assert route_mock.called
        assert time == 2.00
        assert dist == 1.00

    def test_full_route_calc(self):
        from_address = 'From address'
        to_address = 'To address'
        route = wrc.WazeRouteCalculator(from_address, to_address)
        time, dist = route.calc_route_info()
        assert len(self.url_mock.call_args_list) == 3
        assert time == 1.00
        assert dist == 0.40
