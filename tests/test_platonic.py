from fractalprojection.platonic import TETRAHEDRON, OCTAHEDRON
from fractalprojection.vectors import norm, sub
import unittest


class PlatonicTest(unittest.TestCase):
    def test_tetrahedron(self):
        self._do_solid(TETRAHEDRON)

    def test_octahedron(self):
        self._do_solid(OCTAHEDRON)

    def _do_solid(self, solid):
        canon_edge_length = None
        canon_radius = None
        for face in solid:
            for i in range(len(face)):
                v0 = face[i]
                v1 = face[(i+1) % len(face)]
                edge_length = norm(sub(v0, v1))
                radius = norm(v0)
                if canon_radius is None:
                    canon_radius = radius
                else:
                    self.assertAlmostEqual(
                        radius, canon_radius, 2,
                        msg='Vertex {} wrong distance away {} !~= {}'.format(
                            v0, radius, canon_radius
                        )
                    )
                if canon_edge_length is None:
                    canon_edge_length = edge_length
                else:
                    self.assertAlmostEqual(
                        edge_length, canon_edge_length, 2,
                        msg='Edge {} :: {} wrong length {} !~= {}'.format(
                            v0, v1, edge_length, canon_edge_length
                        )
                    )


if __name__ == '__main__':
    unittest.main()
