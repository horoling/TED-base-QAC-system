from itertools import combinations
import networkx as nx
from compose import fi_compose
import random

class lambda_i:
    def __init__(self, value):
        self.value = value

def generate_all_subgraphs(G, n):
    if G is None or n <= 0:
        return []
    subgraphs = []
    nodes = list(G.nodes)
    
    # 生成包含 n 个节点的所有可能的节点组合
    for node_combination in combinations(nodes, n):
        subgraph = G.subgraph(node_combination).copy()
        subgraphs.append(subgraph)
    
    return subgraphs

def node_matcher(n1, n2):
    return str(n1['label']) == str(n2['label'])

def edge_matcher(e1, e2):
    return str(e1['label']) == str(e2['label'])

def find_automorphisms(G1, G2):
    common_subgraphs = []
    matcher = nx.algorithms.isomorphism.GraphMatcher(G1, G2, node_match=node_matcher, edge_match=edge_matcher)
    
    for subgraph_mapping in matcher.subgraph_isomorphisms_iter():
        subgraph_nodes = list(subgraph_mapping.keys())
        subgraph_edges = [(u, v) for u in subgraph_nodes for v in subgraph_nodes if G1.has_edge(u, v)]
        common_subgraph = nx.Graph()
        
        # 添加节点及其属性
        common_subgraph.add_nodes_from((n, G1.nodes[n]) for n in subgraph_nodes)
        
        # 添加边及其属性
        common_subgraph.add_edges_from((u, v, G1.edges[u, v]) for u, v in subgraph_edges)
        
        common_subgraphs.append(common_subgraph)
        
    return common_subgraphs

def find_common_subgraph(G1, G2):
    if G1 is None or G2 is None:
        return nx.Graph()
    common_subgraph = nx.Graph()
    sub_G1 = generate_all_subgraphs(G1,G2.number_of_nodes())
    for subgraph in sub_G1:
        matcher = nx.algorithms.isomorphism.GraphMatcher(subgraph, G2, node_match=node_matcher, edge_match=edge_matcher)
        
        for subgraph_mapping in matcher.subgraph_isomorphisms_iter():
            subgraph_nodes = list(subgraph_mapping.keys())
            subgraph_edges = [(u, v) for u in subgraph_nodes for v in subgraph_nodes if subgraph.has_edge(u, v)]
            
            common_subgraph.add_nodes_from((n, subgraph.nodes[n]) for n in subgraph_nodes)
            
            common_subgraph.add_edges_from((u, v, subgraph.edges[u, v]) for u, v in subgraph_edges)
            
            return common_subgraph
    
    return common_subgraph

def find_common_subgraphs(G1, G2):
    common_subgraphs = []
    unique_subgraphs = set()
    sub_G1 = generate_all_subgraphs(G1,G2.number_of_nodes())
    
    for subgraph in sub_G1:
        matcher = nx.algorithms.isomorphism.GraphMatcher(subgraph, G2, node_match=node_matcher, edge_match=edge_matcher)
        
        for subgraph_mapping in matcher.subgraph_isomorphisms_iter():
            common_subgraph = nx.Graph()
            subgraph_nodes = list(subgraph_mapping.keys())
            subgraph_edges = [(u, v) for u in subgraph_nodes for v in subgraph_nodes if subgraph.has_edge(u, v)]
            
            common_subgraph.add_nodes_from((n, subgraph.nodes[n]) for n in subgraph_nodes)
            common_subgraph.add_edges_from((u, v, subgraph.edges[u, v]) for u, v in subgraph_edges)
            
            # Convert the subgraph to a hashable type
            subgraph_hash = frozenset((u, v, tuple(common_subgraph.edges[u, v].items())) for u, v in common_subgraph.edges())
            
            if subgraph_hash not in unique_subgraphs:
                unique_subgraphs.add(subgraph_hash)
                common_subgraphs.append(common_subgraph)
    
    return common_subgraphs

def read_graph_from_file(file_path):
    """Read graphs from a .my file and return a list of NetworkX graphs with their support."""
    graphs = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_graph = None
    support = None
    for line in lines:
        if line.startswith('t #'):
            if current_graph is not None:
                graphs.append((current_graph, support))
            current_graph = nx.Graph()
        elif line.startswith('v'):
            _, node_id, label = line.split()
            current_graph.add_node(int(node_id), label=int(label))
        elif line.startswith('e'):
            _, node1, node2, label = line.split()
            current_graph.add_edge(int(node1), int(node2), label=int(label))
        else:
            support = int(line.strip())
    
    if current_graph is not None:
        graphs.append((current_graph, support))
    
    return graphs

def compare_graphs(g1, g2):
    """Compare two NetworkX graphs for isomorphism."""
    return nx.is_isomorphic(g1, g2, node_match=lambda n1, n2: n1['label'] == n2['label'],
                            edge_match=lambda e1, e2: e1['label'] == e2['label'])

def find_support(file_path, input_id):
    """Find the number preceding the line that starts with 't' and ends with 'id+1'."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    target_suffix = str(input_id + 1)
    for i in range(1, len(lines)):
        if lines[i].startswith('t') and lines[i].strip().endswith(target_suffix):
            previous_line = lines[i - 1].strip()
            if previous_line.isdigit():
                return int(previous_line)
    
    return None

def find_arrays(q,FDAG):
    node = find_f(q, FDAG)
    arr = FDAG.nodes[node]['arrays']
    return arr

def find_f(f, I):
    for v in I.nodes:
        graph_v = I.nodes[v]['graph']
        if nx.is_isomorphic(f, graph_v):
            return v
    return None

def find_η(fi, fj, f, I):
    node = find_f(f, I)
    if node is None:
        return None
    η = I.nodes[node]['η']
    for n in η:
        if n[1] == fi:
            return n[0]
    return None

def generate_suggestions(Qk, Mq, Q, k):
    q = read_single_graph(Q)

    suggestions = []
    count = 0
    for qk in Qk:
        for mq in Mq:
            if qk[1] == mq[0]:
                candidate = fi_compose(qk[0], q, qk[2])
                
                # 同构检测
                is_isomorphic = False
                for suggestion in suggestions:
                    if nx.is_isomorphic(candidate, suggestion):
                        is_isomorphic = True
                        break
                
                if not is_isomorphic:
                    suggestions.append(candidate)
                    count += 1
                if count >= k:
                    return suggestions
    return suggestions

def read_single_graph(file_path):
    """Read a single graph from a .my file and return a NetworkX graph."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_graph = nx.Graph()
    for line in lines:
        if line.startswith('v'):
            _, node_id, label = line.split()
            current_graph.add_node(int(node_id), label=int(label))
        elif line.startswith('e'):
            _, node1, node2, label = line.split()
            current_graph.add_edge(int(node1), int(node2), label=int(label))
    
    return current_graph

import hashlib

def hash_graph(graph):
    # 将图转换为字符串并计算其哈希值
    graph_str = str(graph)
    return hashlib.md5(graph_str.encode()).hexdigest()

def check_duplicate_graphs(candidates):
    seen_hashes = set()
    for i, candidate in enumerate(candidates):
        graph_hash = hash_graph(candidate)
        if graph_hash in seen_hashes:
            print(f"Duplicate graph found: candidate_{i}")
        else:
            seen_hashes.add(graph_hash)

def get_valid_λ(graph , q):
    r = find_common_subgraphs(graph, q)
    node_arrays = []

    for i, subgraph_mapping in enumerate(r):
        node_array = []
        for node in subgraph_mapping:
            node_array.append(node)
        node_arrays.append(node_array)
    return node_arrays

def read_query_graph(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    query_graph = nx.Graph()  # 创建一个空的 NetworkX 图
    
    for line in lines:
        if line.startswith('v'):
            parts = line.split()
            node_id = int(parts[1])
            node_label = parts[2]
            query_graph.add_node(node_id, label=node_label)  # 添加节点及其标签
        elif line.startswith('e'):
            parts = line.split()
            source = int(parts[1])
            target = int(parts[2])
            edge_label = parts[3]
            query_graph.add_edge(source, target, label=edge_label)  # 添加边及其标签
    
    return query_graph
