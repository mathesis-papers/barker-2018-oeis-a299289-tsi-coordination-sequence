import argparse
from collections import deque
from fractions import Fraction
import hashlib
import json
from itertools import product
from math import factorial
from pathlib import Path


def neighbors(vertex):
    horizontal, transverse, layer = vertex
    yield horizontal + 1, transverse, layer
    yield horizontal - 1, transverse, layer
    yield horizontal, transverse + 1, layer
    yield horizontal, transverse - 1, layer
    yield horizontal, transverse, layer + 1
    yield horizontal, transverse, layer - 1
    if layer % 2 == 0:
        yield horizontal + 1, transverse, layer + 1
        yield horizontal, transverse - 1, layer - 1
    else:
        yield horizontal, transverse + 1, layer + 1
        yield horizontal - 1, transverse, layer - 1


def gap(endpoint, coordinate):
    return max(0, min(0, endpoint) - coordinate) + max(0, coordinate - max(0, endpoint))


def metric(vertex):
    horizontal, transverse, layer = vertex
    return abs(layer) + gap((layer + 1) // 2, horizontal) + gap(layer // 2, transverse)


def shell(radius):
    return 1 if radius == 0 else (13 * radius * radius + (3 if radius % 2 else 4)) // 2


def ball(radius):
    return (26 * radius**3 + 39 * radius**2 + 34 * radius + (9 if radius % 2 else 12)) // 12


def breadth_first(center, radius):
    distances = {center: 0}
    queue = deque([center])
    counts = [0] * (radius + 1)
    while queue:
        vertex = queue.popleft()
        depth = distances[vertex]
        counts[depth] += 1
        if depth < radius:
            for adjacent in neighbors(vertex):
                if adjacent not in distances:
                    distances[adjacent] = depth + 1
                    queue.append(adjacent)
    return distances, counts


def centered_metric(center, vertex):
    horizontal, transverse, layer = vertex
    origin_horizontal, origin_transverse, origin_layer = center
    first = (layer + 1) // 2 - (origin_layer + 1) // 2
    second = layer // 2 - origin_layer // 2
    distance = (abs(layer - origin_layer) + gap(first, horizontal - origin_horizontal)
                + gap(second, transverse - origin_transverse))
    assert 2 * distance == (abs(layer - origin_layer) + abs(horizontal - origin_horizontal)
                            + abs(horizontal - origin_horizontal - first)
                            + abs(transverse - origin_transverse)
                            + abs(transverse - origin_transverse - second))
    return distance


def stack_checks():
    radius = 5
    checked_vertices = 0
    patterns = 0
    for directions in product((1, 2), repeat=2 * radius):
        orientation = dict(zip(range(-radius, radius), directions))
        first_counts = {0: 0}
        for layer in range(radius):
            first_counts[layer + 1] = first_counts[layer] + (orientation[layer] == 1)
        for layer in range(-1, -radius - 1, -1):
            first_counts[layer] = first_counts[layer + 1] - (orientation[layer] == 1)
        distances = {(0, 0, 0): 0}
        queue = deque([(0, 0, 0)])
        counts = [0] * (radius + 1)
        while queue:
            vertex = queue.popleft()
            horizontal, transverse, layer = vertex
            depth = distances[vertex]
            counts[depth] += 1
            first = first_counts[layer]
            second = layer - first
            assert depth == abs(layer) + gap(first, horizontal) + gap(second, transverse)
            assert 2 * depth == (abs(layer) + abs(horizontal) + abs(horizontal - first)
                                 + abs(transverse) + abs(transverse - second))
            if depth == radius:
                continue
            adjacent_vertices = [
                (horizontal + 1, transverse, layer), (horizontal - 1, transverse, layer),
                (horizontal, transverse + 1, layer), (horizontal, transverse - 1, layer),
                (horizontal, transverse, layer + 1), (horizontal, transverse, layer - 1),
            ]
            adjacent_vertices.append((horizontal + 1, transverse, layer + 1)
                                     if orientation[layer] == 1
                                     else (horizontal, transverse + 1, layer + 1))
            adjacent_vertices.append((horizontal - 1, transverse, layer - 1)
                                     if orientation[layer - 1] == 1
                                     else (horizontal, transverse - 1, layer - 1))
            for adjacent in adjacent_vertices:
                if adjacent not in distances:
                    distances[adjacent] = depth + 1
                    queue.append(adjacent)
        for index in range(1, radius + 1):
            extremal_products = []
            for layer in [index, -index]:
                first = abs(first_counts[layer])
                second = abs(layer - first_counts[layer])
                extremal_products.append((first + 1) * (second + 1))
            predicted = 6 * index**2 - 2 * index + sum(extremal_products)
            assert counts[index] == predicted
            assert 6 * index**2 + 2 <= predicted <= shell(index)
        checked_vertices += len(distances)
        patterns += 1
    period = (1, 2, 2, 1)
    example_bound = 1000
    for center_layer in [0, 1]:
        for index in range(1, example_bound + 1):
            products = []
            for sign in [-1, 1]:
                layers = range(center_layer, center_layer + index) if sign == 1 else range(center_layer - index, center_layer)
                first = sum(period[layer % 4] == 1 for layer in layers)
                products.append((first + 1) * (index - first + 1))
            predicted = 6 * index**2 - 2 * index + sum(products)
            if center_layer == 0:
                assert predicted == shell(index)
            elif index == 2:
                assert predicted == 26
    return {'slab_indices': [-radius, radius - 1], 'patterns': patterns,
            'graph_search_radius': radius, 'metric_equalities': checked_vertices,
            'period_four': {'directions': list(period), 'origin_series_maximum_index': example_bound,
                            'layer_one_radius_two': 26, 'alternating_radius_two': 28}}


def multiply(left, right):
    product = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            product[left_degree + right_degree] += left_value * right_value
    return product


def run(radius):
    origin_distances, counts = breadth_first((0, 0, 0), radius)
    assert all(metric(vertex) == distance for vertex, distance in origin_distances.items())
    assert counts == [shell(index) for index in range(radius + 1)]
    assert len(origin_distances) == ball(radius)
    prefix = [1, 8, 28, 60, 106, 164, 236, 320, 418, 528, 652, 788, 938, 1100,
              1276, 1464, 1666, 1880, 2108, 2348, 2602, 2868, 3148, 3440, 3746,
              4064, 4396, 4740, 5098, 5468, 5852, 6248, 6658, 7080, 7516, 7964,
              8426, 8900, 9388, 9888, 10402, 10928]
    partial_prefix = [1, 9, 37, 97, 203, 367, 603, 923, 1341, 1869, 2521, 3309,
                      4247, 5347, 6623, 8087, 9753, 11633, 13741, 16089, 18691,
                      21559, 24707, 28147, 31893, 35957, 40353, 45093, 50191,
                      55659, 61511, 67759, 74417, 81497, 89013, 96977, 105403,
                      114303, 123691]
    assert prefix == [shell(index) for index in range(len(prefix))]
    assert partial_prefix == [ball(index) for index in range(len(partial_prefix))]
    cumulative = 0
    algebra_bound = 1000
    for index in range(algebra_bound + 1):
        cumulative += shell(index)
        assert cumulative == ball(index)
        if index >= 5:
            assert shell(index) == 2 * shell(index - 1) - 2 * shell(index - 3) + shell(index - 4)
            assert ball(index) == (3 * ball(index - 1) - 2 * ball(index - 2)
                                   - 2 * ball(index - 3) + 3 * ball(index - 4) - ball(index - 5))
    numerator = [1, 6, 12, 6, 1]
    shell_denominator = [1, -2, 0, 2, -1]
    ball_denominator = [1, -3, 2, 2, -3, 1]
    coefficients = [shell(index) for index in range(algebra_bound + 1)]
    cumulative_coefficients = [ball(index) for index in range(algebra_bound + 1)]
    for sequence, denominator in [(coefficients, shell_denominator),
                                  (cumulative_coefficients, ball_denominator)]:
        product = multiply(sequence, denominator)
        assert product[:5] == numerator
        assert all(value == 0 for value in product[5:algebra_bound + 1])
    exponential_bound = 100
    for index in range(exponential_bound + 1):
        coefficient = Fraction(-1 if index == 0 else 0)
        for offset, multiplier in [(0, 4), (1, 13), (2, 13)]:
            residual = index - offset
            if residual >= 0 and residual % 2 == 0:
                coefficient += Fraction(multiplier, 2 * factorial(residual))
        for offset, multiplier in [(0, 3), (1, 13), (2, 13)]:
            residual = index - offset
            if residual >= 0 and residual % 2 == 1:
                coefficient += Fraction(multiplier, 2 * factorial(residual))
        assert coefficient == Fraction(shell(index), factorial(index))
    hex_shells = [1] + [6 * index**2 + 2 for index in range(1, algebra_bound + 1)]
    hex_balls = [index**3 + (index + 1)**3 for index in range(algebra_bound + 1)]
    assert [sum(hex_shells[:index + 1]) for index in range(algebra_bound + 1)] == hex_balls
    hex_numerator = [1, 5, 5, 1]
    for sequence, denominator in [(hex_shells, [1, -3, 3, -1]),
                                  (hex_balls, [1, -4, 6, -4, 1])]:
        coefficients = multiply(sequence, denominator)
        assert coefficients[:4] == hex_numerator
        assert all(value == 0 for value in coefficients[4:algebra_bound + 1])
    for index in range(exponential_bound + 1):
        for sequence, polynomial, correction in [(hex_shells, [2, 6, 6], -1),
                                                (hex_balls, [1, 8, 9, 2], 0)]:
            coefficient = Fraction(correction if index == 0 else 0)
            coefficient += sum((Fraction(multiplier, factorial(index - offset))
                                for offset, multiplier in enumerate(polynomial) if offset <= index), Fraction(0))
            assert coefficient == Fraction(sequence[index], factorial(index))
    centers = [(3, -2, 1), (-2, 1, -3), (0, 0, 4)]
    for center in centers:
        centered_distances, centered_counts = breadth_first(center, 6)
        assert centered_counts == [shell(index) for index in range(7)]
        assert all(centered_metric(center, vertex) == distance
                   for vertex, distance in centered_distances.items())
    local_bound = 8
    local_edges = 0
    for horizontal in range(-local_bound, local_bound + 1):
        for transverse in range(-local_bound, local_bound + 1):
            for layer in range(-local_bound, local_bound + 1):
                vertex = horizontal, transverse, layer
                transform = lambda point: (point[1], point[0], point[2] + 1)
                for adjacent in neighbors(vertex):
                    assert vertex in set(neighbors(adjacent))
                    assert abs(metric(adjacent) - metric(vertex)) <= 1
                    assert transform(adjacent) in set(neighbors(transform(vertex)))
                    local_edges += 1
    statement = {
        'arithmetic': 'exact integers and rational numbers',
        'graph_search': {'radius': radius, 'vertices': len(origin_distances), 'shells': counts},
        'metric_equalities': len(origin_distances),
        'local_edge_checks': {'coordinate_box': [-local_bound, local_bound], 'directed_edges': local_edges},
        'other_centers': {'centers': centers, 'radius': 6},
        'oeis_prefixes': {'A299289_terms': len(prefix), 'A299290_terms': len(partial_prefix)},
        'recurrences_partial_sums_ordinary_series': {'maximum_index': algebra_bound},
        'exponential_series': {'maximum_index': exponential_bound},
        'hex_specialization': {'ordinary_series_recurrences_partial_sums_maximum_index': algebra_bound,
                               'exponential_series_maximum_index': exponential_bound},
        'boundary_values': {'a0': shell(0), 'recurrence_residual_at_four': shell(4) - 2 * shell(3) + 2 * shell(1) - shell(0)},
        'arbitrary_stacks': stack_checks(),
        'coverage': 'Finite checks of the graph metric, shell and ball formulas, generating-function identities, arbitrary slab stacks and the period-four example; the all-radius proofs are in note.tex.',
        'status': 'pass',
    }
    statement['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return statement


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--radius', type=int, default=32)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    if not 1 <= arguments.radius <= 64:
        parser.error('Select a radius between 1 and 64.')
    result = json.dumps(run(arguments.radius), indent=2) + '\n'
    if arguments.output:
        arguments.output.write_text(result)
    else:
        print(result, end='')
