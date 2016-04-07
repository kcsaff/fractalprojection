import unittest
from fractalprojection.projections import MercatorProjection


class TestMercatorProjection(unittest.TestCase):
    def test_bounds(self):
        proj = MercatorProjection((-80, +80), (-180, +180))

        self.assertEqual(proj.get((-80, -180)), (0, 0))
        self.assertEqual(proj.get((+80, -180)), (1, 0))
        self.assertEqual(proj.get((+80, +180)), (1, 1))
        self.assertEqual(proj.get((-80, +180)), (0, 1))

        self.assertEqual(proj.get((0, 0)), (0.5, 0.5))


    def test_bbox(self):
        proj = MercatorProjection((-80, +80), (-180, +180), (-2, -3, +2, +3))

        self.assertEqual(proj.get((-80, -180)), (-2, -3))
        self.assertEqual(proj.get((+80, -180)), (+2, -3))
        self.assertEqual(proj.get((+80, +180)), (+2, +3))
        self.assertEqual(proj.get((-80, +180)), (-2, +3))


if __name__ == '__main__':
    unittest.main()