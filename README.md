# WazeRouteCalculator
Calculate actual route time and distance with waze api

[![Build Status](https://travis-ci.org/kovacsbalu/WazeRouteCalculator.svg?branch=master)](https://travis-ci.org/kovacsbalu/WazeRouteCalculator)

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
