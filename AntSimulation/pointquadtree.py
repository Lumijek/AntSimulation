import numpy as np
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


"""
QuadTree works with any object that has a x and y variable.
"""


total = []  # List to keep track of all rectangles


class PointQuadTree:
    def __init__(
        self, x, y, width, height, max_points, max_depth, depth=0
    ):  # (x, y) represent top left of rectangle
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (x + width / 2, y + height / 2)
        self.max_points = max_points
        self.max_depth = max_depth
        self.points = []
        self.nodes = []  # in order: topleft, topright, bottomleft, bottomright
        self.depth = depth
        self.total_points_under = 0 # To know when to destroy 4 nodes and turn quadtree into leaf
        total.append(self)  # keeps track of all the quadtrees in case you want to display/see the rectangles

    def insert(self, point):
        """
        Attempts to insert point into current quadtree and if can't creates
        4 nodes and inserts into them.
        """
        self.total_points_under += 1
        if not self.nodes:
            self.points.append(point)

            if self.depth <= self.max_depth and len(self.points) > self.max_points:
                self.subdivide()

        else:
            self.insert_to_node(point)

    def insert_to_node(self, point):
        """
        Inserts point to
        """
        if point.y <= self.center[1]:
            if point.x <= self.center[0]:
                self.nodes[0].insert(point)
                return
            else:
                self.nodes[1].insert(point)
                return
        else:
            if point.x <= self.center[0]:
                self.nodes[2].insert(point)
                return
            else:
                self.nodes[3].insert(point)
                return

    def subdivide(self):
        """
        Creates 4 nodes for the quadtree all with same dimensions.
        """
        new_width = self.width / 2
        new_height = self.height / 2
        new_depth = self.depth + 1
        self.nodes = [
            PointQuadTree(
                self.x,
                self.y,
                new_width,
                new_height,
                self.max_points,
                self.max_depth,
                new_depth,
            ),
            PointQuadTree(
                self.x + new_width,
                self.y,
                new_width,
                new_height,
                self.max_points,
                self.max_depth,
                new_depth,
            ),
            PointQuadTree(
                self.x,
                self.y + new_height,
                new_width,
                new_height,
                self.max_points,
                self.max_depth,
                new_depth,
            ),
            PointQuadTree(
                self.x + new_width,
                self.y + new_height,
                new_width,
                new_height,
                self.max_points,
                self.max_depth,
                new_depth,
            ),
        ]
        for point in self.points:
            self.insert_to_node(point)
        self.points = []

    def query_rect(self, bounds, lis=None):
        """
        Uses given bounds (x, y, width, height) where x and y represent top left
        of the rectangle to search all quadtrees that intersect that region for
        the in that region
        """
        x1, y1 = (bounds[0], bounds[1])
        x2, y2 = (bounds[0] + bounds[2], bounds[1] + bounds[3])
        if lis == None:
            lis = []

        if self.nodes:
            if y1 <= self.center[1]:
                if x1 <= self.center[0]:
                    self.nodes[0].query_rect(bounds, lis)
                if x2 > self.center[0]:
                    self.nodes[1].query_rect(bounds, lis)
            if y2 > self.center[1]:
                if x1 <= self.center[0]:
                    self.nodes[2].query_rect(bounds, lis)
                if x2 > self.center[0]:
                    self.nodes[3].query_rect(bounds, lis)

        for point in self.points:
            if point.x >= x1 and point.x < x2 and point.y >= y1 and point.y < y2:
                lis.append(point)
        return lis


    def query_circle(self, center, radius, lis=None):
        '''
        Uses given bounds of center and radius and
        creates AABB to search all quadtrees that intersect that region for
        the in that region
        '''
        bounds = [center[0] - radius, center[1] - radius, radius * 2, radius * 2]
        x1, y1 = (bounds[0], bounds[1])
        x2, y2 = (bounds[0] + bounds[2], bounds[1] + bounds[3])
        radius_squared = radius * radius
        if lis == None:
            lis = []

        if self.nodes:
            if y1 <= self.center[1]:
                if x1 <= self.center[0]:
                    self.nodes[0].query_circle(center, radius, lis)
                if x2 > self.center[0]:
                    self.nodes[1].query_circle(center, radius, lis)
            if y2 > self.center[1]:
                if x1 <= self.center[0]:
                    self.nodes[2].query_circle(center, radius, lis)
                if x2 > self.center[0]:
                    self.nodes[3].query_circle(center, radius, lis)

        for point in self.points:
            if (point.x - center[0]) ** 2 + (point.y - center[1]) ** 2 <= radius_squared:
                lis.append(point)
        return lis

    def query_circle2(self, center, radius):
        '''
        Uses given bounds of center and radius and
        creates AABB to search all quadtrees that intersect that region for
        the in that region
        '''
        bounds = [center[0] - radius, center[1] - radius, radius * 2, radius * 2]
        x1, y1 = (bounds[0], bounds[1])
        x2, y2 = (bounds[0] + bounds[2], bounds[1] + bounds[3])
        radius_squared = radius * radius
        lis = []

        def query_circle_closure(node):
            n_center = node.center
            n_nodes = node.nodes
            if n_nodes:
                if y1 <= n_center[1]:
                    if x1 <= n_center[0]:
                        query_circle_closure(n_nodes[0])
                    if x2 > n_center[0]:
                        query_circle_closure(n_nodes[1])
                if y2 > n_center[1]:
                    if x1 <= n_center[0]:
                        query_circle_closure(n_nodes[2])
                    if x2 > n_center[0]:
                        query_circle_closure(n_nodes[3])

            else:
                for point in node.points:
                    if (point.x - center[0]) * (point.x - center[0]) + (point.y - center[1]) * (point.y - center[1]) <= radius_squared:
                        lis.append(point)
        query_circle_closure(self)

        return lis

        #return query_circle_closure(self, lis)


    def remove(self, point):
        """
        Removes point from quadtree. If point doesn't exist
        nothing will happen.
        """
        self.total_points_under -= 1
        if not self.nodes:
            try:
                self.points.remove(point)
            except:
                self.total_points_under += 1

        else:

            if point.y <= self.center[1]:
                if point.x <= self.center[0]:
                    self.nodes[0].remove(point)
                    return
                else:
                    self.nodes[1].remove(point)
                    return
            else:
                if point.x <= self.center[0]:
                    self.nodes[2].remove(point)
                    return
                else:
                    self.nodes[3].remove(point)
                    return

    def cleanup(self):  # only call if you have moving objects in your quadtree or are constantly removing elements
        """
        Checks all 4 nodes of a quadtree and if all of them are empty it
        destroys the 4 nodes and makes the current quadtree a leaf
        """
        if self.nodes:
            node_element_sum = 0
            for node in self.nodes:
                node.cleanup()
                node_element_sum += node.total_points_under
            if node_element_sum == 0:
                total.remove(self.nodes[0])
                total.remove(self.nodes[1])
                total.remove(self.nodes[2])
                total.remove(self.nodes[3])
                self.nodes = []
