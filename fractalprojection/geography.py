from fractalprojection.vectors import *


def latitude(coords, north=(0, 0, 1)):
    coords = normalized(tuple(coords))
    north = normalized(north)
    if len(coords) == 3:
        north_component = dot(coords, north)
        equatorial_component = norm(sub(coords, mul(north_component, north)))
        return math.degrees(math.atan2(north_component, equatorial_component))
    else:
        raise TypeError('Can only convert length 3 vectors to latitude')


def longitude(coords, meridian=(1, 0, 0), east=(0, 1, 0)):
    coords = normalized(tuple(coords))
    meridian = normalized(meridian)
    east = normalized(east)
    if len(coords) == 3:
        meridian_component = dot(coords, meridian)
        east_component = dot(coords, east)
        return math.degrees(math.atan2(east_component, meridian_component))
    else:
        raise TypeError('Can only convert length 3 vectors to longitude')


class ProjectiveVector(VectorClass()):
    def __init__(self, coords):
        super().__init__(normalized(coords))

    @classmethod
    def from_geographic(cls, coords, north=(0, 0, 1), meridian=(1, 0, 0), east=(0, 1, 0)):
        lat, long = coords
        
        north = normalized(north)
        meridian = normalized(meridian)
        east = normalized(east)
        north_component = math.sin(math.radians(lat))
        equatorial_component = math.cos(math.radians(lat))
        meridian_component = equatorial_component * math.cos(math.radians(long))
        east_component = equatorial_component * math.sin(math.radians(long))

        return cls(add(mul(north, north_component), mul(meridian, meridian_component), mul(east, east_component)))

    def to_geographic(self, north=(0, 0, 1), meridian=(1, 0, 0), east=(0, 1, 0)):
        return latitude(self, north=north), longitude(self, meridian=meridian, east=east)

    def __eq__(self, other):
        try:
            return len(self) == len(other) and all(a == b for a, b in zip(self, normalized(other)))
        except TypeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
