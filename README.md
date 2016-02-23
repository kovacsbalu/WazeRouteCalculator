# WazeRouteCalculator

[![Build Status](https://travis-ci.org/kovacsbalu/WazeRouteCalculator.svg?branch=master)](https://travis-ci.org/kovacsbalu/WazeRouteCalculator)
[![Coverage Status](https://coveralls.io/repos/github/kovacsbalu/WazeRouteCalculator/badge.svg?branch=master)](https://coveralls.io/github/kovacsbalu/WazeRouteCalculator?branch=master)

Calculate actual route time and distance with waze api

```python
import wrc

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
route = wrc.WazeRouteCalculator(from_address, to_address)
route.calc_route_info()
```

```
python example.py 
From: Budapest, Hungary - to: Gyor, Hungary
Time 69.27 minutes, distance 120.91 km.
```
