# -*- coding: utf-8 -*-

import WazeRouteCalculator as wrc
import mock
import requests_mock
import pytest


class TestWRC():

    def setup_method(self, method):
        self.waze_url = "https://www.waze.com/"
        self.address_req = self.waze_url + "row-SearchServer/mozi"
        self.routing_req = self.waze_url + "row-RoutingManager/routingRequest"
        self.lat = 47.4979
        self.lon = 19.0402
        self.bounds = {"bottom": 47.4, "top": 47.5, "left": 19, "right": 19.3}
        self.length = 400
        self.time = 60
        self.address_to_coords_response = '[{"city":"Test","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (self.lat, self.lon, str(self.bounds).replace("'", '"'))
        self.routing_response = '{"response":{"results":[{"length":%s,"crossTime":%s}]}}' % (self.length, self.time)

    def test_address_to_coords(self):
        from_address = 'From address'
        to_address = 'To address'
        test_address = "Testaddress"
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
            coords = route.address_to_coords(test_address)
        assert coords == {'lat': self.lat, 'lon': self.lon, 'bounds': self.bounds}
        assert m.call_count == 3

    def test_address_to_coords_reversed(self):
        from_address = 'From address'
        to_address = 'To address'
        test_address = "Testaddress"

        bounds = {"top": 47.4, "bottom": 47.5, "right": 19, "left": 19.3}
        address_to_coords_response = '[{"city":"Test","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (self.lat, self.lon, str(bounds).replace("'", '"'))

        with requests_mock.mock() as m:
            m.get(self.address_req, text=address_to_coords_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
            coords = route.address_to_coords(test_address)
        assert coords == {'lat': self.lat, 'lon': self.lon, 'bounds': self.bounds}
        assert m.call_count == 3

    def test_address_to_coords_nocity(self):
        from_address = 'From address'
        to_address = 'To address'
        test_address = "Testaddress"
        address_to_coords_response = '[{"location":{"lat":%s,"lon":%s},"bounds":%s}]' % (self.lat, self.lon, str(self.bounds).replace("'", '"'))
        with pytest.raises(wrc.WRCError):
            with requests_mock.mock() as m:
                m.get(self.address_req, text=address_to_coords_response)
                route = wrc.WazeRouteCalculator(from_address, to_address)
                coords = route.address_to_coords(test_address)

    def test_already_coords(self):
        from_address = '47.497912,19.040235'
        to_address = '47.687457,17.650397'
        with requests_mock.mock() as m:
            addr_query = m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
        assert not addr_query.called
        assert route.start_coords["lat"] == from_address.split(",")[0]
        assert route.end_coords["lat"] == to_address.split(",")[0]

    def test_get_route(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route()
        assert response == {"results": [{"length": self.length, "crossTime": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_route_v2(self):
        routing_response_v2 = '{"response":[{"result":[{"length":%s,"cross_time":%s}]}]}' % (self.length, self.time)
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=routing_response_v2)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route()
        assert response == {"result": [{"length": self.length, "cross_time": self.time}]}
        assert self.routing_req in m.request_history[2].url

    def test_get_route_next_server(self):
        fail_routing_req = self.waze_url + "RoutingManager/routingRequest"
        fail_routing_response = '{}'
        ok_routing_req = self.waze_url + "row-RoutingManager/routingRequest"
        ok_routing_response = '{"response":{"results":[{"length":%s,"crossTime":%s}]}}' % (self.length, self.time)
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(fail_routing_req, text=fail_routing_response)
            m.get(ok_routing_req, text=ok_routing_response)
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

    def test_get_all_routes_v2(self):
        length2, time2 = (410, 62)
        self.routing_response = '{"alternatives":[{"response":{"result":[{"length":%s,"cross_time":%s}]}},{"response":{"result":[{"length":%s,"cross_time":%s}]}}]}' % (self.length, self.time, length2, time2)
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator("", "")
            response = route.get_route(3)
        assert response == [{"result": [{"length": self.length, "cross_time": self.time}]}, {"result": [{"length": length2, "cross_time": time2}]}]
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

    def test_add_up_route_v2(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        results = [{"length": 1000, "cross_time": 120}, {"length": 1000, "cross_time": 120}]
        time, dist = route._add_up_route(results)
        assert time == 4.00
        assert dist == 2.00

    def test_add_up_route_real_time(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        results = [{"length": 1000, "crossTime": 120, "crossTimeWithoutRealTime": 110}, {"length": 1000, "crossTime": 120, "crossTimeWithoutRealTime": 115}]
        time, dist = route._add_up_route(results, real_time=True)
        assert time == 4.00
        assert dist == 2.00

    def test_add_up_route_real_time_v2(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        results = [{"length": 1000, "cross_time": 120, "cross_time_without_real_time": 110}, {"length": 1000, "cross_time": 120, "cross_time_without_real_time": 115}]
        time, dist = route._add_up_route(results, real_time=True)
        assert time == 4.00
        assert dist == 2.00

    def test_add_up_route_no_real_time(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        results = [{"length": 1000, "crossTime": 120, "crossTimeWithoutRealTime": 110}, {"length": 1000, "crossTime": 120, "crossTimeWithoutRealTime": 115}]
        time, dist = route._add_up_route(results, real_time=False)
        assert time == 3.75
        assert dist == 2.00

    def test_add_up_route_no_real_time_v2(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        results = [{"length": 1000, "crosstime": 120, "cross_time_without_real_time": 110}, {"length": 1000, "cross_time": 120, "cross_time_without_real_time": 115}]
        time, dist = route._add_up_route(results, real_time=False)
        assert time == 3.75
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

    def test_calc_route_info_v2(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"result": [{"length": 1000, "cross_time": 120}]})
        route.get_route = route_mock
        time, dist = route.calc_route_info()
        assert route_mock.called
        assert time == 2.00
        assert dist == 1.00

    def test_calc_all_routes_info(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value=[{
                "routeType": ["Best"],
                "shortRouteName": "test1",
                "results": [{"length": 1000, "crossTime": 120}]
            }, {
                "routeType": ["Normal"],
                "shortRouteName": "test2",
                "results": [{"length": 1100, "crossTime": 150}]}
            ])
        route.get_route = route_mock
        results = route.calc_all_routes_info()
        assert route_mock.called
        assert results == {"Best-test1": (2.0, 1.0), "Normal-test2": (2.5, 1.1)}

    def test_calc_route_info_nort(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"results": [{"length": 1000, "crossTime": 140, "crossTimeWithoutRealTime": 120}]})
        route.get_route = route_mock
        time, dist = route.calc_route_info(real_time=False)
        assert route_mock.called
        assert time == 2.00
        assert dist == 1.00

    def test_calc_route_info_nort_v2(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"result": [{"length": 1000, "cross_Time": 140, "cross_time_without_real_time": 120}]})
        route.get_route = route_mock
        time, dist = route.calc_route_info(real_time=False)
        assert route_mock.called
        assert time == 2.00
        assert dist == 1.00

    def test_calc_all_routes_info_nort(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value=[{
                "routeType": ["Best"],
                "shortRouteName": "test1",
                "results": [{"length": 1000, "crossTime": 130, "crossTimeWithoutRealTime": 120}]
            }, {
                "routeType": ["Normal"],
                "shortRouteName": "test2",
                "results": [{"length": 1100, "crossTime": 150, "crossTimeWithoutRealTime": 120}]
            }])
        route.get_route = route_mock
        results = route.calc_all_routes_info(real_time=False)
        assert route_mock.called
        assert results == {"Best-test1": (2.0, 1.0), "Normal-test2": (2.0, 1.1)}

    def test_calc_all_routes_info_only_one(self):
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value=[{
            "routeType": ["Best"],
            "shortRouteName": "test1",
            "results": [{"length": 1000, "crossTime": 120}]}
            ])
        route.get_route = route_mock
        results = route.calc_all_routes_info()
        assert route_mock.called
        assert results == {"Best-test1": (2.0, 1.0)}

    def test_calc_route_info_with_path_not_ignored(self):
        with requests_mock.mock() as m:
            lat = [47.49, 47.612, 47.645]
            lon = [19.04, 18.99, 18.82]
            bounds = [{"bottom": 47.4, "top": 47.5, "left": 19, "right": 19.1}, None, {"bottom": 47.6, "top": 47.7, "left": 18.8, "right": 18.9}]
            length = [400, 5000, 500]
            time = [40, 300, 50]
            address_to_coords_response = [
                '[{"city":"Test1","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[0], lon[0], str(bounds[0]).replace("'", '"')),
                '[{"city":"Test2","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[2], lon[2], str(bounds[2]).replace("'", '"'))
            ]
            m.get(self.address_req, [{'text': address_to_coords_response[0]}, {'text': address_to_coords_response[1]}])
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"results": [
            {"length": length[0], "crossTime": time[0], "path": {"x": lon[0], "y": lat[0]}},
            {"length": length[1], "crossTime": time[1], "path": {"x": lon[1], "y": lat[1]}},
            {"length": length[2], "crossTime": time[2], "path": {"x": lon[2], "y": lat[2]}}
        ]})
        route.get_route = route_mock
        time, dist = route.calc_route_info()
        assert route_mock.called
        assert time == 6.5
        assert dist == 5.9

    def test_calc_route_info_with_ignored(self):
        with requests_mock.mock() as m:
            lat = [47.49, 47.612, 47.645]
            lon = [19.04, 18.99, 18.82]
            bounds = [{"bottom": 47.4, "top": 47.5, "left": 19, "right": 19.1}, None, {"bottom": 47.6, "top": 47.7, "left": 18.8, "right": 18.9}]
            length = [400, 5000, 500]
            time = [40, 300, 50]
            address_to_coords_response = [
                '[{"city":"Test1","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[0], lon[0], str(bounds[0]).replace("'", '"')),
                '[{"city":"Test2","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[2], lon[2], str(bounds[2]).replace("'", '"'))
            ]
            m.get(self.address_req, [{'text': address_to_coords_response[0]}, {'text': address_to_coords_response[1]}])
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"results": [
            {"length": length[0], "crossTime": time[0], "path": {"x": lon[0], "y": lat[0]}},
            {"length": length[1], "crossTime": time[1], "path": {"x": lon[1], "y": lat[1]}},
            {"length": length[2], "crossTime": time[2], "path": {"x": lon[2], "y": lat[2]}}
        ]})
        route.get_route = route_mock
        time, dist = route.calc_route_info(stop_at_bounds=True)
        assert route_mock.called
        assert time == 5.00
        assert dist == 5.00

    def test_calc_route_info_with_ignored_and_nort(self):
        with requests_mock.mock() as m:
            lat = [47.49, 47.612, 47.645]
            lon = [19.04, 18.99, 18.82]
            bounds = [{"bottom": 47.4, "top": 47.5, "left": 19, "right": 19.1}, None, {"bottom": 47.6, "top": 47.7, "left": 18.8, "right": 18.9}]
            length = [400, 5000, 500]
            time = [40, 360, 60]
            nort_time = [40, 300, 50]
            address_to_coords_response = [
                '[{"city":"Test1","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[0], lon[0], str(bounds[0]).replace("'", '"')),
                '[{"city":"Test2","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[2], lon[2], str(bounds[2]).replace("'", '"'))
            ]
            m.get(self.address_req, [{'text': address_to_coords_response[0]}, {'text': address_to_coords_response[1]}])
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"results": [
            {"length": length[0], "crossTime": time[0], "crossTimeWithoutRealTime": nort_time[0], "path": {"x": lon[0], "y": lat[0]}},
            {"length": length[1], "crossTime": time[1], "crossTimeWithoutRealTime": nort_time[1], "path": {"x": lon[1], "y": lat[1]}},
            {"length": length[2], "crossTime": time[2], "crossTimeWithoutRealTime": nort_time[2], "path": {"x": lon[2], "y": lat[2]}}
        ]})
        route.get_route = route_mock
        time, dist = route.calc_route_info(stop_at_bounds=True, real_time=False)
        assert route_mock.called
        assert time == 5.00
        assert dist == 5.00

    def test_calc_route_info_stopatbounds_missing_bounds(self):
        with requests_mock.mock() as m:
            lat = [47.49, 47.612, 47.645]
            lon = [19.04, 18.99, 18.82]
            bounds = [None, None, {"bottom": 47.6, "top": 47.7, "left": 18.8, "right": 18.9}]
            length = [400, 5000, 500]
            time = [45, 300, 60]
            address_to_coords_response = [
                '[{"city":"Test1","location":{"lat":%s,"lon":%s},"bounds":null}]' % (lat[0], lon[0]),
                '[{"city":"Test2","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[2], lon[2], str(bounds[2]).replace("'", '"'))
            ]
            m.get(self.address_req, [{'text': address_to_coords_response[0]}, {'text': address_to_coords_response[1]}])
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value={"results": [
            {"length": length[0], "crossTime": time[0], "path": {"x": lon[0], "y": lat[0]}},
            {"length": length[1], "crossTime": time[1], "path": {"x": lon[1], "y": lat[1]}},
            {"length": length[2], "crossTime": time[2], "path": {"x": lon[2], "y": lat[2]}}
        ]})
        route.get_route = route_mock
        time, dist = route.calc_route_info(stop_at_bounds=True)
        assert route_mock.called
        assert time == 5.75
        assert dist == 5.40

    def test_calc_all_routes_info_with_ignored(self):
        with requests_mock.mock() as m:
            lat = [47.49, [47.612, 47.614, 47.56], 47.645]
            lon = [19.04, [18.99, 18.99, 19.01], 18.82]
            bounds = [{"bottom": 47.4, "top": 47.5, "left": 19, "right": 19.1}, None, {"bottom": 47.6, "top": 47.7, "left": 18.8, "right": 18.9}]
            length = [400, [5000, 5100, 4500], 500]
            time = [40, [300, 330, 345], 50]
            address_to_coords_response = [
                '[{"city":"Test1","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[0], lon[0], str(bounds[0]).replace("'", '"')),
                '[{"city":"Test2","location":{"lat":%s,"lon":%s},"bounds":%s}]' % (lat[2], lon[2], str(bounds[2]).replace("'", '"'))
            ]
            m.get(self.address_req, [{'text': address_to_coords_response[0]}, {'text': address_to_coords_response[1]}])
            route = wrc.WazeRouteCalculator("", "")
        route_mock = mock.Mock(return_value=[{
            "routeType": ["Best"],
            "shortRouteName": "test1",
            "results": [
                {"length": length[0], "crossTime": time[0], "path": {"x": lon[0], "y": lat[0]}},
                {"length": length[1][0], "crossTime": time[1][0], "path": {"x": lon[1][0], "y": lat[1][0]}},
                {"length": length[2], "crossTime": time[2], "path": {"x": lon[2], "y": lat[2]}}
            ]
        }, {
            "routeType": ["Normal"],
            "shortRouteName": "test2",
            "results": [
                {"length": length[0], "crossTime": time[0], "path": {"x": lon[0], "y": lat[0]}},
                {"length": length[1][1], "crossTime": time[1][1], "path": {"x": lon[1][1], "y": lat[1][1]}},
                {"length": length[2], "crossTime": time[2], "path": {"x": lon[2], "y": lat[2]}}
            ]
        }, {
            "routeType": ["Slow"],
            "shortRouteName": "test3",
            "results": [
                {"length": length[0], "crossTime": time[0], "path": {"x": lon[0], "y": lat[0]}},
                {"length": length[1][2], "crossTime": time[1][2], "path": {"x": lon[1][2], "y": lat[1][2]}},
                {"length": length[2], "crossTime": time[2], "path": {"x": lon[2], "y": lat[2]}}
            ]
        }])
        route.get_route = route_mock
        results = route.calc_all_routes_info(stop_at_bounds=True)
        assert route_mock.called
        assert results == {"Best-test1": (5.0, 5.0), "Normal-test2": (5.5, 5.1), "Slow-test3": (5.75, 4.5)}

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
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
        assert route.log.getEffectiveLevel() == wrc.logging.WARNING

    def test_region_change(self):
        from_address = 'From address'
        to_address = 'To address'
        address_req = self.waze_url + "SearchServer/mozi"
        with requests_mock.mock() as m:
            m.get(address_req, text=self.address_to_coords_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, region='NA')
        assert route.region == 'US'

    def test_vehicle_motor(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, vehicle_type='MOTORCYCLE')
            route.get_route()
        assert 'vehicletype=motorcycle' in req.last_request.query

    def test_empty_vehicle_type(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
            route.get_route()
        assert 'vehicletype' not in req.last_request.query

    def test_default_route_options(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address)
            route.get_route()
        assert route.ROUTE_OPTIONS['AVOID_TRAILS'] == 't'
        assert route.ROUTE_OPTIONS['AVOID_TOLL_ROADS'] == 'f'
        assert 'avoid_trails%3at' in req.last_request.query
        assert 'avoid_toll_roads%3af' in req.last_request.query

    def test_avoid_toll_road_true(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, avoid_toll_roads=True)
            route.get_route()
        assert 'avoid_toll_roads%3at' in req.last_request.query

    def test_avoid_toll_road_false(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, avoid_toll_roads=False)
            route.get_route()
        assert 'avoid_toll_roads%3af' in req.last_request.query

    def test_avoid_ferries_true(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, avoid_ferries=True)
            route.get_route()
        assert 'avoid_ferries%3at' in req.last_request.query

    def test_avoid_ferries_false(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, avoid_ferries=False)
            route.get_route()
        assert 'avoid_ferries%3af' in req.last_request.query

    def test_avoid_subscription_road_true(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, avoid_subscription_roads=True)
            route.get_route()
        assert 'subscription=' not in req.last_request.query

    def test_avoid_subscription_road_false(self):
        from_address = 'From address'
        to_address = 'To address'
        with requests_mock.mock() as m:
            m.get(self.address_req, text=self.address_to_coords_response)
            req = m.get(self.routing_req, text=self.routing_response)
            route = wrc.WazeRouteCalculator(from_address, to_address, avoid_subscription_roads=False)
            route.get_route()
        assert 'subscription=' in req.last_request.query
