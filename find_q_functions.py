import networkx as nx
from newf import vf2_emb
import re
from Func1 import get_valid_λ,read_single_graph

def get_qs(source,result):
    data = extract_matching_lines(source, result)
    graphs = read_query_graphs_from_list(data)
    return graphs


def read_query_graphs_from_list(data):
    graphs = []
    current_graph = None
    
    for line in data:
        if line.startswith('t #'):
            if current_graph is not None:
                graphs.append(current_graph)
            current_graph = nx.Graph()
        elif line.startswith('v'):
            parts = line.split()
            node_id = int(parts[1])
            node_label = parts[2]
            current_graph.add_node(node_id, label=node_label)
        elif line.startswith('e'):
            parts = line.split()
            source = int(parts[1])
            target = int(parts[2])
            edge_label = parts[3]
            current_graph.add_edge(source, target, label=edge_label)
    
    if current_graph is not None:
        graphs.append(current_graph)
    
    return graphs

def extract_matching_lines(file_path, numbers):
    if isinstance(numbers, int):
        numbers = [numbers]
    
    numbers = [str(num) for num in numbers]

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    matching_lines = []
    add_lines = False
    
    for line in lines:
        if line.startswith('t'):
            line_number = re.search(r'\d+', line.strip()).group()
            if line_number in numbers:
                add_lines = True
                matching_lines.append(line.strip())
            else:
                add_lines = False
        elif add_lines:
            matching_lines.append(line.strip())
    with open("embeddings.my", 'w', encoding='utf-8') as file:
        for line in matching_lines:
            file.write(line + '\n')    
    
    return matching_lines


def get_embeddings(qs, target):
    emb = []
    q = read_single_graph(target)
    for graph in qs:
        λ = get_valid_λ(graph, q)
        print(λ)
        emb.append((graph,λ))
    return emb