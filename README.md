# WazeRouteCalculator

[![Build Status](https://travis-ci.org/kovacsbalu/WazeRouteCalculator.svg?branch=master)](https://travis-ci.org/kovacsbalu/WazeRouteCalculator)
[![Coverage Status](https://coveralls.io/repos/github/kovacsbalu/WazeRouteCalculator/badge.svg?branch=master)](https://coveralls.io/github/kovacsbalu/WazeRouteCalculator?branch=master)

Calculate actual route time and distance with waze api

## Installation

```
pip install WazeRouteCalculator
```
## Example

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address)
route.calc_route_info()
```

```
python example.py
From: Budapest, Hungary - to: Gyor, Hungary
Time 69.27 minutes, distance 120.91 km.
```

Pass `log_lvl=None` to silence output and just get the return value:

```python
import WazeRouteCalculator

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, log_lvl=None)
route_time, route_distance = route.calc_route_info()
print 'Time %.2f minutes, distance %.2f km.' % (route_time, route_distance)
```
