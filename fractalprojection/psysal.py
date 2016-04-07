from fractalprojection.geography import ProjectiveVector


class GreatTriangle(object):
    __slots__ = ['vectors', 'splats']

    def __init__(self, vectors):
        self.vectors = tuple(ProjectiveVector(vector) for vector in vectors)
        self.splats = [None] * 4

    def __len__(self):
        return len(self.vectors)

    def __iter__(self):
        return iter(self.vectors)

    def __getitem__(self, item):
        return self.vectors[item]

    @classmethod
    def of(cls, vectors):
        if isinstance(vectors, GreatTriangle):
            return vectors
        else:
            return GreatTriangle(vectors)

    def split(self):
        return tuple(self.splat(i) for i in range(4))

    def splat(self, index):
        if self.splats[index] is None:
            if 0 <= index < 3:
                self.splats[index] = GreatTriangle((
                    self[index],
                    self[index] + self[(index + 1) % 3],
                    self[index] + self[(index + 2) % 3],
                ))
            elif index == 3:
                self.splats[index] = GreatTriangle((
                    self[0] + self[1],
                    self[1] + self[2],
                    self[2] + self[0],
                ))
            else:
                raise RuntimeError()

        return self.splats[index]


class Reprojection(object):
    def __init__(self, size, projection, order=(0, 1, 3, 2), equal_area=False):
        self.size = size
        self.projection = projection
        self.order = order
        if equal_area:
            raise NotImplementedError()

    def lookup(self, triangle, coords):
        """
        Return image coordinates (bounded by "size") using the given projection
        for `coords` which are two fractional coordinates, each bounded by 0,1, and
        suggesting a point in the `triangle` composed of three `ProjectiveVector`s.
        :param triangle: `tuple` of three `ProjectiveVector`s
        :param coords:
        :return: integer image coordinates, or `None`
        """
        fx, fy = coords
        triangle = GreatTriangle.of(triangle)
        while True:
            points = set()
            for coord in triangle:
                mapped = self.projection.get(coord.to_geographic())
                if mapped:
                    point = int(self.size[0]*mapped[0]), int(self.size[1]*mapped[1])
                else:
                    point = None
                points.add(point)
                if len(points) > 1:
                    break  # Don't map to same place -- iterate
            else:
                # Aiming the same place everywhere for sho
                return points.pop()
            which = (2 if fy >= 0.5 else 0) + (1 if fx >= 0.5 else 0)
            fx = (fx * 2) % 1.0
            fy = (fy * 2) % 1.0
            triangle = triangle.splat(which)



