# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
from shapely.geometry import Point


def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max() * 2
        print "radius: " + str(radius)

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


def get_voronoi_areas(points):
    points = np.array(points)
    min_x, max_x, min_y, max_y = -5.0, 52.0, -5.0, 55.0
    vor = Voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor, 1500)
    box = Polygon([[min_x, min_y], [min_x, max_y], [max_x, max_y],
                  [max_x, min_y]])
    areas = [-1 for num in range(5)]
    for region in regions:
        polygon = vertices[region]
        # Clipping polygon
        poly = Polygon(polygon).intersection(box)

        for i, (x, y) in enumerate(points):
            point = Point(x, y)
            if point.within(poly):
                areas[i] = poly.area
                break

        # polygon = [p for p in poly.exterior.coords]
        # plt.fill(*zip(*polygon), alpha=0.4)

    # plt.plot(points[:, 0], points[:, 1], 'ko')
    # plt.axis('equal')
    # plt.xlim(-5, 52)
    # plt.ylim(-4, 55)
    # plt.show()

    for i, area in enumerate(areas):
        if area <= 0:
            raise Exception("Point not assigned to a Voronoi Cell: " +
                            str(i) + " | " + str(points))

    return areas
###############################################################################


"""
# colorize
for region in regions:
    polygon = vertices[region]
    # Clipping polygon
    poly = Polygon(polygon)
    poly = poly.intersection(box)
    print poly.area
    print " "
    polygon = [p for p in poly.exterior.coords]

    plt.fill(*zip(*polygon), alpha=0.4)

plt.plot(points[:, 0], points[:, 1], 'ko')
plt.axis('equal')
plt.xlim(-5, 52)
plt.ylim(-4, 55)

# plt.savefig('voro.png')
plt.show()
"""
# arr = ([[21.0447, 26.8672], [20.7569, 30.13343], [20.2059, 51.08914],
#        [20.5643, 26.25739],
#        [20.857, 34.19209]])
# print get_voronoi_areas(np.array(arr))
