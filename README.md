# WazeRouteCalculator
Calculate actual route time and distance with waze api

```python
import wrc

from_address = 'Budapest, Hungary'
to_address = 'Gyor, Hungary'
wrc = wrc.WazeRouteCalculator(from_address, to_address)
wrc.calc_route_info()
```

```
python example.py 
From: Budapest, Hungary - to: Gyor, Hungary
Time 69.27 minutes, distance 120.91 km.
```
