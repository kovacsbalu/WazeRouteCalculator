#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wrc

from_address = 'Budapest, Hungary'
to_address = 'Győr, Hungary'
route = wrc.WazeRouteCalculator(from_address, to_address)
try:
    route.calc_route_info()
except wrc.WRCError as err:
    print err
