# WazeRouteCalculator

[![Build Status](https://github.com/kovacsbalu/WazeRouteCalculator/actions/workflows/python-app.yml/badge.svg)](https://travis-ci.org/kovacsbalu/WazeRouteCalculator)

Calculate actual route time and distance with Waze API.

## Installation

```
pip install WazeRouteCalculator
```

Tested on Python 2.7 and 3.6, 3.8, 3.10

## Example

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

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

`from_address` and `to_address` are required. The address can also be coordinates.
`region` is optional, and defaults to "EU". `region` can be one of:

- EU (Europe)
- US or NA (North America)
- IL (Israel)

Region is used for address searching. Setting base coord parameter.
(Removed from route server selection. Looping through all route servers.)

### Vehicle types

`vehicle_type` is also optional, and defaults to "" which is private. `vehicle_type` can be one of:

- TAXI
- MOTORCYCLE

Time to destination will be adjusted based on the mode of transport.

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
vehicle_type = 'MOTORCYCLE'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region, vehicle_type)
route.calc_route_info()
```

```
python example.py
From: Budapest, Hungary - to: Gyor, Hungary
Time 112.92 minutes, distance 124.93 km.
```

### Avoid toll roads

`avoid_toll_roads` is also optional, and defaults to False. Setting `avoid_toll_roads` to True
will only return results not on a tollway.

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Chicago, Illinois'
to_address = 'New York City, New York'
region = 'US'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region, avoid_toll_roads=True)
route.calc_route_info()
```

### Avoid subscription roads (vignette system)

`avoid_subscription_roads` is also optional, and defaults to False. Setting `avoid_subscription_roads` to True
will only return results not involving a subscription road (toll roads in coutries that use vignettes).

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Long Branch, New Jersey'
to_address = 'New York City, New York'
region = 'US'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region, avoid_subscription_roads=True)
route.calc_route_info()
```

### Avoid ferries

`avoid_ferries` is also optional, and defaults to False. Setting `avoid_ferries` to True
will only return results not involving a ferry.

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Long Branch, New Jersey'
to_address = 'New York City, New York'
region = 'US'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region, avoid_ferries=True)
route.calc_route_info()
```

### Multiple routes

You can get multiple routes using the `route.calc_all_routes_info()` function:

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route.calc_all_routes_info()
```

```
python example.py
From: Budapest, Hungary - to: Győr, Hungary
Start coords: (47.467660814, 19.077617881)
End coords: (47.67936706542969, 17.707035064697266)
Min	Max
72.92	80.33 minutes
118.75	120.21 km
```

`calc_all_routes_info` takes an optional single parameter, the number of routes to fetch. Note that the Waze API may not return as many possibilities as requested. The function returns a dict: `{'routeType-shortRouteName': (route_time1, route_distance1), 'routeType-shortRouteName': (route_time2, route_distance2), ...}`.

### No real time

You can pass `real_time=False` to `calc_route_info` or `calc_all_routes_info` to get the time estimate not including current conditions, but rather the average travel time for the current time. This would avoid something like traffic accidents or construction that is slowing down traffic abnormally on the day you run it from messing up the data. Note that this is not the same as travel time with no traffic at all, it is simply the usual traffic.

### Intercity travel times only

Sometimes you may want to map travel times between cities and just see how long it takes to get from one to other. However, Waze's API will take you between two specific spots in the city, which can add to the time and distance, especially in larger cities.

You can pass `stop_at_bounds=True` to `calc_route_info` or `calc_all_routes_info` and it will ignore travel within the origin and destination cities.

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
From: Budapest, Hungary - to: Gyor, Hungary

route.calc_route_info(stop_at_bounds=True)
Time 46.27 minutes, distance 95.29 km.

route.calc_route_info()
Time 72.42 minutes, distance 121.33 km.
```

### Leave at
You can pass `time_delta=<int>` to `calc_route_info` or `calc_all_routes_info` to set the leave time from now. The value (minute) can be negative so you can step back and forward. Default 0 = now.
The following example shows route info from now + 60 minute.

```python
import WazeRouteCalculator

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
From: Budapest, Hungary - to: Gyor, Hungary

route.calc_route_info(time_delta=60)
Time 73.33 minutes, distance 120.92 km.
```

### No logging
`log_lvl` argument is depricated.

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
region = 'EU'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route_time, route_distance = route.calc_route_info()
print 'Time %.2f minutes, distance %.2f km.' % (route_time, route_distance)
```
