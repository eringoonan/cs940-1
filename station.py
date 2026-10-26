import re
from numbers import Real
from decimal import Decimal
import math
from typing import List
from exceptions import InvalidCoordError, TubeError, InvalidStationTypeError

class Station():
    TUBE_LINES = frozenset({"bakerloo", "central", "circle", "district", 
                            "hammersmith-city", "jubilee", "metropolitan", 
                            "northern", "piccadilly", "victoria", "waterloo-city"})
    
    EARTH_RADIUS_KM = 6371.0

    ranges = {
        "longitude": (-180, 180),
        "latitude": (-90, 90)
    }

    def __init__(self, station_id:str, station_name:str, interchange_lines:List, zones:str, lat:float, lon:float):
        # verify lat/lon are valid
        self.lon = self._validate_coordinate(lon, "longitude")
        self.lat = self._validate_coordinate(lat, "latitude")

        # initialise given variables
        self.station_id = station_id
        self.station_name = station_name
        
        # split zones into a list
        self.zones = re.split(r"[+/]", zones)

        # parse interchange lines into list of line ids
        self.interchange_lines = []
        for line in interchange_lines:
            self.interchange_lines.append(line["id"])

    # is interchange
    def is_interchange(self) -> bool:
        return len(self.TUBE_LINES.intersection(self.interchange_lines)) > 1

    # distance to
    def distance_to(self, other:"Station") -> float:
        """used to calculate distance from one station to another, takes in an instance of another station and itself, calculating using lon/lat from both"""
        if not isinstance(other, Station):
            raise InvalidStationTypeError(other)

        lon_self, lat_self, lon_other, lat_other = map(math.radians, [self.lon, self.lat, other.lon, other.lat])

        delta_lat = lat_other - lat_self
        delta_lon = lon_other - lon_self

        a = (math.sin(delta_lat / 2) ** 2 + math.cos(lat_self) * math.cos(lat_other) * math.sin(delta_lon / 2) ** 2)

        a = min(1.0, a)

        c = 2 * math.asin(math.sqrt(a))

        return self.EARTH_RADIUS_KM * c

    # magic methods
    def __eq__(self, other):
        """compare if two instances of station are equal via station id"""
        if not isinstance(other, Station):
            return NotImplemented

        return self.station_id == other.station_id

    def __hash__(self):
        """hash stations based on their unique IDs"""
        return hash(self.station_id)

    def __repr__(self):
        """return developer friendly representation with useful debugging details"""
        return f"Station(station_id={self.station_id!r}, station_name={self.station_name!r})"

    def __str__(self):
        """return readable station name"""
        return self.station_name

    # validate lon/lat coordinates as real numbers
    def _validate_coordinate(self, value, field):
        # check for bool/valid number
        if isinstance(value, bool) or not isinstance(value, (Real, Decimal)):
            raise InvalidCoordError(value, field)

        # block infinity
        if not math.isfinite(value):
            raise InvalidCoordError(value, field)

        low, high = self.ranges[field]

        # check within a range
        if not low <= value <= high:
            raise InvalidCoordError(value, field)

        return value