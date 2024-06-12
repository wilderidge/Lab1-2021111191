import random
import re
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import time


def print_words(words):
    st.write("解析出的单词序列为", end=' ')
    words_str = ' '.join(words)
    st.write(words_str)


def parse_txt(txt_path):
    with open(txt_path, "r") as f:
        text = f.read()
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words


def query_bridge_words(G, word1, word2):
    if word1 not in G or word2 not in G:
        return None
    neighbors1 = set(G.neighbors(word1))
    neighbors2 = set(G.predecessors(word2))
    bridge_words = neighbors1.intersection(neighbors2)
    return list(bridge_words)


def insert_bridge_words(G, file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    new_words = []
    for i in range(len(words) - 1):
        new_words.append(words[i])
        bridge_words = query_bridge_words(G, words[i], words[i + 1])
        if bridge_words:
            new_words.append(random.choice(bridge_words))
    new_words.append(words[-1])
    return ' '.join(new_words)


def generate_directed_graph(input_path):
    G = nx.MultiDiGraph()
    edge_counts = {}
    words = parse_txt(input_path)
    new_edges_list = [(words[i], words[i + 1]) for i in range(len(words) - 1)]
    for edge in new_edges_list:
        if edge in edge_counts:
            # Remove the old edge
            G.remove_edge(*edge)
            # Increase the count
            edge_counts[edge] += 1
            print(f"Edge {edge} has been added {edge_counts[edge]} times.")
        else:
            edge_counts[edge] = 1

        # Add the edge with the new count as the weight
        G.add_edge(*edge, key=edge_counts[edge], weight=edge_counts[edge])

    # 设置随机种子
    np.random.seed(0)
    pos = nx.spring_layout(G)
    return G, pos, words


def showDirectedGraph(G, output_path, pos):
    nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
    D = nx.DiGraph(G)
    edge_labels = nx.get_edge_attributes(D, 'weight')
    nx.draw_networkx_edge_labels(D, pos, edge_labels=edge_labels, label_pos=0.3)
    plt.savefig(output_path)
    print("The graph has been saved to", output_path)
    st.pyplot(plt)  # 使用 Streamlit 的函数来显示图形


def fun_3():
    G, pos, words = generate_directed_graph('input/1.txt')
    showDirectedGraph(G, 'output/1.png', pos)
    st.button('返回主页面',on_click=chong_zhi)
    word1 = input("请输入第一个单词: ")
    word2 = input("请输入第二个单词: ")
    bridge_words = query_bridge_words(G, word1, word2)
    if bridge_words is None:
        st.write("No \"{}\" or \"{}\" in the graph!".format(word1, word2))
    elif len(bridge_words) == 0:
        st.write("No bridge words from \"{}\" to \"{}\"!".format(word1, word2))
    else:
        st.write("The bridge words from \"{}\" to \"{}\" are: \"{}\"".format(word1, word2, ', '.join(bridge_words)))


def generate_new_text(file_path):
    G, pos, words = generate_directed_graph('input/1.txt')
    showDirectedGraph(G, 'output/1.png', pos)
    st.button('返回主页面',on_click=chong_zhi)
    words = parse_txt(file_path)
    new_words = []
    for i in range(len(words) - 1):
        new_words.append(words[i])
        bridge_words = query_bridge_words(G, words[i], words[i + 1])
        if bridge_words:
            new_words.append(random.choice(bridge_words))
    new_words.append(words[-1])
    new_text = ' '.join(new_words)
    st.write(f"插入桥接词后的新文本为： {new_text}")


def fun_5(output_path):
    G, pos, words = generate_directed_graph('input/1.txt')
    slot = st.empty()
    nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
    D = nx.DiGraph(G)
    edge_labels = nx.get_edge_attributes(D, 'weight')
    nx.draw_networkx_edge_labels(D, pos, edge_labels=edge_labels, label_pos=0.3)
    st.pyplot(plt)
    st.button('返回主页面',on_click=chong_zhi)
    
    word1 = input("请输入第一个单词: ")
    word2 = input("请输入第二个单词: ")
    path_edges, path_length = calc_shortest_path(G, word1, word2)
    plt.clf()
    slot.empty()
    
    # 创建一个边到索引的映射
    edge_to_index = {edge: i for i, edge in enumerate(G.edges())}
    # 初始化所有边的颜色为黑色
    edge_colors = ['black' for _ in G.edges()]

    for i, edge in enumerate(path_edges):
        # 找到当前边在 G.edges() 中的正确位置，然后设置其颜色
        edge_colors[edge_to_index[edge]] = 'red'
        nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1', edge_color=edge_colors)
        D = nx.DiGraph(G)
        edge_labels = nx.get_edge_attributes(D, 'weight')
        nx.draw_networkx_edge_labels(D, pos, edge_labels=edge_labels, label_pos=0.3)
        plt.savefig(output_path)
        slot.pyplot(plt)  # 在插槽中显示图形
        plt.clf()  # 清空当前的图形
        time.sleep(1)
        if i != len(path_edges) - 1:
            slot.empty()
        else:
            st.write(f"The shortest path from {word1} to {word2} has length {path_length}.")


def calc_shortest_path(G, word1, word2):
    # 检查 word1 和 word2 是否为空字符串
    if word1 == "" or word2 == "":
        return [ ], 0
    # 将 word1 和 word2 都转换为小写
    word1 = word1.lower()
    word2 = word2.lower()
    # 检查 word1 和 word2 是否都在图中
    if word1 not in G or word2 not in G:
        return [ ], 0
    try:
        shortest_path = nx.shortest_path(G, source=word1, target=word2, weight='weight')
    except nx.NetworkXNoPath:
        return [ ], 0
    path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
    path_length = 0
    for u, v in path_edges:
        edge_data = G.get_edge_data(u, v)
        min_weight = min(data['weight'] for data in edge_data.values())
        path_length += min_weight

    return path_edges, path_length


def toggle_pause_6():
    st.session_state.stage = 6
    st.session_state.is_paused = not st.session_state.is_paused

def chong_zhi():
    st.session_state.clear()
    st.session_state.stage = 0


def randomWalk():
    G, pos, words = generate_directed_graph('input/1.txt')

    # 创建一个边到索引的映射
    edge_to_index = {edge: i for i, edge in enumerate(G.edges())}

    if 'current_node' not in st.session_state:
        st.session_state.current_node = random.choice(list(G.nodes()))
        st.session_state.visited_nodes = [st.session_state.current_node]
        st.session_state.visited_edges = []
        st.session_state.text = f"{st.session_state.current_node}"
        st.session_state.edge_colors = ['black' for _ in G.edges()]  # 初始化所有边的颜色为黑色
        st.write(f"选择{st.session_state.current_node}作为初始点")

    # 创建一个空的插槽
    slot = st.empty()

    st.button('暂停/继续',on_click=toggle_pause_6)
    st.button('返回主页面',on_click=chong_zhi)

    nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1', edge_color=st.session_state.edge_colors)
    D = nx.DiGraph(G)
    edge_labels = nx.get_edge_attributes(D, 'weight')
    nx.draw_networkx_edge_labels(D, pos, edge_labels=edge_labels, label_pos=0.3)
    slot.pyplot(plt)  # 在插槽中显示图形
    plt.clf()  # 清空当前的图形

    while not st.session_state.is_paused:
        out_edges = list(G.out_edges(st.session_state.current_node, data=True))
        if not out_edges:
            st.write("No out edges from the current node!")
            break

        edge = random.choice(out_edges)
        target_node = edge[1]

        if edge in st.session_state.visited_edges:
            st.write(f"Edge {edge} has been visited!")
            break

        st.session_state.visited_nodes.append(target_node)
        st.session_state.visited_edges.append(edge)

        st.session_state.edge_colors[edge_to_index[(edge[0], edge[1])]] = 'red'
        nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1', edge_color=st.session_state.edge_colors)
        D = nx.DiGraph(G)
        edge_labels = nx.get_edge_attributes(D, 'weight')
        nx.draw_networkx_edge_labels(D, pos, edge_labels=edge_labels, label_pos=0.3)
        slot.pyplot(plt)  # 在插槽中显示图形
        plt.clf()  # 清空当前的图形
        st.session_state.current_node = target_node
        st.session_state.text = f"{st.session_state.text} -> {st.session_state.current_node}"
        time.sleep(1)

    return st.session_state.text
