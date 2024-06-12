from lab1 import *

def test_shortest_path_1():
    G, pos, words = generate_directed_graph('input/1.txt')
    path_edges, path_length = calc_shortest_path(G, 'to', 'and')
    assert path_edges == [('to', 'explore'), ('explore', 'strange'), ('strange', 'new'), ('new', 'life'), ('life', 'and')], path_edges
    assert path_length == 20, path_length

def test_shortest_path_2():
    G, pos, words = generate_directed_graph('input/1.txt')
    path_edges, path_length = calc_shortest_path(G, 'To', 'AND')
    assert path_edges == [('to', 'explore'), ('explore', 'strange'), ('strange', 'new'), ('new', 'life'), ('life', 'and')], path_edges
    assert path_length == 20, path_length

def test_shortest_path_3():
    G, pos, words = generate_directed_graph('input/1.txt')
    path_edges, path_length = calc_shortest_path(G, 'AnD', 'To')
    assert path_edges == [('and', 'new'), ('new', 'worlds'), ('worlds', 'to')], path_edges
    assert path_length == 12, path_length

def test_shortest_path_4():
    G, pos, words = generate_directed_graph('input/1.txt')
    path_edges, path_length = calc_shortest_path(G, 'a', 'c')
    assert path_edges == [ ], path_edges
    assert path_length == 0, path_length

def test_shortest_path_5():
    G, pos, words = generate_directed_graph('input/1.txt')
    path_edges, path_length = calc_shortest_path(G, 'and', '')
    assert path_edges == [ ], path_edges
    assert path_length == 0, path_length

def test_shortest_path_6():
    G, pos, words = generate_directed_graph('input/1.txt')
    path_edges, path_length = calc_shortest_path(G, 'and', 'ww')
    assert path_edges == [ ], path_edges
    assert path_length == 0, path_length
    
    