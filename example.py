#!/usr/bin/env python
# -*- coding: utf-8 -*-
import WazeRouteCalculator
import logging

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Budapest, Hungary'
to_address = 'Győr, Hungary'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address)
try:
    route.calc_route_info()
except WazeRouteCalculator.WRCError as err:
    print(err)
