# GH-HWfailover
Queries the Genius Hub API for a failure to heat hot water and triggers the immersion zone to compensate

This is proof of concept code, it is not guarunteed to work in any capacity, be tidy to look at or efficient to run or scale.

Genius configuration assumes:
A "primary" zone of type hot water temperature driving the boiler hot water call for heat and being supplied the probe temperature value.
A "secondary" zone of type hot water temperature driving an electric switch connected to the immersion with hot water probe for termpartiure, shared with primary zone above.

This script leverages the V1 cloud API and can be run anywhere with an internet connection and a configured API token

Python script takes positional arguments, run 'python GH-HWfailover.py -h' for details:

usage: GH-HWfailover.py [-h] [--debug] token primary secondary delta window

Query the Genius Hub API for a primary zone active state and boost the secondary zone if the temperature does not rise
sufficiently quickly. A good example is a boiler controlled HW zone as primary with an immersion as secondary with the
temp probe feeding both zones.

positional arguments:
  token       The auth token provided by mygenius hub portal https://my.geniushub.co.uk/#/tokens
  primary     The zone to be monitored
  secondary   The zone to boost on failure
  delta       Degrees change expected in the assessment window in the primary zone when heating
  window      Assessment window size in minutes

optional arguments:
  -h, --help  show this help message and exit
  --debug     Enable debug output on run