import math


class MercatorProjection(object):
    def __init__(self, latitudes, longitudes=(0, 360), bbox=(1, 1)):
        self.latitudes = latitudes
        self.longitudes = longitudes

        self.latitudes_mapped = tuple(self._map_latitude(lat) for lat in latitudes)

        if len(bbox) == 2:
            bbox = (0, 0) + bbox
        self.bbox = bbox

    def get(self, coords, default=None):
        latitude, longitude = coords  # degrees
        if not (min(self.latitudes) <= latitude <= max(self.latitudes)):
            return default

        while longitude < min(self.longitudes):
            longitude += 360
        while longitude > max(self.longitudes):
            longitude -= 360
        if not (min(self.longitudes) <= longitude <= max(self.longitudes)):
            return default

        long_fraction = (longitude - self.longitudes[0]) / (self.longitudes[-1] - self.longitudes[0])
        mapped_lat = self._map_latitude(latitude)
        lat_fraction = (mapped_lat - self.latitudes_mapped[0]) / (self.latitudes_mapped[-1] - self.latitudes_mapped[0])

        lat_result = self.bbox[0] + (self.bbox[2] - self.bbox[0]) * lat_fraction
        long_result = self.bbox[1] + (self.bbox[3] - self.bbox[1]) * long_fraction
        return lat_result, long_result

    @classmethod
    def _map_latitude(cls, latitude):
        return math.log(math.tan(math.radians(90 + latitude)/2))
