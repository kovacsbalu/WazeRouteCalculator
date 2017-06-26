# WazeRouteCalculator

[![Build Status](https://travis-ci.org/kovacsbalu/WazeRouteCalculator.svg?branch=master)](https://travis-ci.org/kovacsbalu/WazeRouteCalculator)
[![Coverage Status](https://coveralls.io/repos/github/kovacsbalu/WazeRouteCalculator/badge.svg?branch=master)](https://coveralls.io/github/kovacsbalu/WazeRouteCalculator?branch=master)

Calculate actual route time and distance with Waze API.

## Installation

```
pip install WazeRouteCalculator
```

Tested on Python 2 and 3.

## Example

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route.calc_route_info()
```

```
python example.py
From: Budapest, Hungary - to: Gyor, Hungary
Time 69.27 minutes, distance 120.91 km.
```

`calc_route_info` returns a tuple `(route_time, route_distance)` in addition to logging.

`from_address` and `to_address` are required. `region` is optional, and defaults to "EU". `region` can be one of:

- EU (Europe)
- US or NA (North America)
- IL (Israel)

The Waze API has separate URLs for each region, and so identifying the correct region is crucial.

### Multiple routes

You can get multiple routes using the `route.calc_all_routes_info()` function:

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route.calc_all_routes_info()
```

```
python example.py
From: Budapest, Hungary - to: Gyor, Hungary
Time 74.45 - 129.43 minutes, distance 120.91 - 130.08 km.
```

`calc_all_routes_info` takes an optional single parameter, the number of routes to fetch. Note that the Waze API may not return as many possibilities as requested. The function returns a dict: `{'route_name1': (route_time1, route_distance1), 'route_name2': (route_time2, route_distance2), ...}`.

### No real time

You can pass `real_time=False` to `calc_route_info` or `calc_all_routes_info` to get the time estimate not including current conditions, but rather the average travel time for the current time. This would avoid something like traffic accidents or construction that is slowing down traffic abnormally on the day you run it from messing up the data. Note that this is not the same as travel time with no traffic at all, it is simply the usual traffic.

### Intercity travel times only

Sometimes you may want to map travel times between cities and just see how long it takes to get from one to other. However, Waze's API will take you between two specific spots in the city, which can add to the time and distance, especially in larger cities.

You can pass `stop_at_bounds=True` to `calc_route_info` or `calc_all_routes_info` and it will ignore travel within the origin and destination cities.

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
From: Budapest, Hungary - to: Gyor, Hungary

route.calc_route_info(stop_at_bounds=True)
Time 46.27 minutes, distance 95.29 km.
(46.266666666666666, 95.294)

route.calc_route_info()
Time 72.42 minutes, distance 121.33 km.
(72.41666666666667, 121.325)
```

### Silence logging
Pass `log_lvl=None` to silence output and just get the return value:

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, log_lvl=None)
route_time, route_distance = route.calc_route_info()
print 'Time %.2f minutes, distance %.2f km.' % (route_time, route_distance)
```
