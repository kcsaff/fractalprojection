import pkgutil
from io import BytesIO
from PIL import Image
from fractalprojection.psysal import Reprojection, GreatTriangle
from fractalprojection.projections import MercatorProjection
from fractalprojection.geography import *
from fractalprojection.platonic import TETRAHEDRON, OCTAHEDRON


RESOURCE_PACKAGE = 'fractalprojection.resources'


def resource(resource_name):
    return pkgutil.get_data(RESOURCE_PACKAGE, resource_name)


GREAT_OCTAHEDRON = [
    GreatTriangle.of(triangle)
    for triangle in OCTAHEDRON
]

GREAT_TETRAHEDRON = [
    GreatTriangle.of(triangle)
    for triangle in TETRAHEDRON
]


SIZE = (512, 512)


def jitter(point, amount=2):
    for dy in range(amount):
        for dx in range(amount):
            yield point[0]+dx/amount, point[1]+dy/amount


def antialias_getpixel(reprojector, triangle, pt, amount, source, default=(255, 255, 255)):
    lookups = [reprojector.lookup(triangle, jpt) for jpt in jitter(pt, amount)]
    lookups = [lookup for lookup in lookups if lookup is not None]
    if not lookups:
        return default
    return floormean(source.getpixel(lookup) for lookup in lookups)


def main():
    source = Image.open(BytesIO(resource('mercator-projection.jpg')))
    projection = MercatorProjection((-80, +80), (-180, +180))
    reprojector = Reprojection(source.size, projection)

    target = Image.new(source.mode, SIZE)
    for y in range(SIZE[1]):
        fy = y / SIZE[1]
        iy = 2 if fy >= 0.5 else 0
        fy2 = (fy * 2) % 1.0
        for x in range(SIZE[0]):
            fx = x / SIZE[0]
            ii = iy + (1 if fx >= 0.5 else 0)
            fx2 = (fx * 2) % 1.0
            pixel = antialias_getpixel(reprojector, GREAT_TETRAHEDRON[ii], (fx2, fy2), 1, source)
            target.putpixel((x, y), pixel)

    target.save("out.png")


if __name__ == '__main__':
    main()
