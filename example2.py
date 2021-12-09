#!/usr/bin/env python
# -*- coding: utf-8 -*-
import WazeRouteCalculator
import logging

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Calais, France'
to_address = 'Dover, UK'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, avoid_toll_roads=True)
try:
    route.calc_route_info()
except WazeRouteCalculator.WRCError as err:
    print(err)
