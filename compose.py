import networkx as nx
import copy

def sub_compose(fi, composed, λi):
    max_node = max(composed.nodes) if composed.nodes else 0  # 获取 composed 中的最大节点标号
    for node in fi.nodes(data=True):
        u = node[0]
        if u not in λi:
            max_node += 1
            composed.add_node(max_node, label=fi.nodes[u]['label'])
            for edge in fi.edges(data=True):
                ue, ve = edge[0], edge[1]
                uc, vc = ue, ve
                if ue == u:
                    uc = max(composed.nodes)
                    vc = get_order(ve, λi)
                    composed.add_edge(uc, vc, label=fi.edges[ue, ve]['label'])
                elif ve == u:
                    vc = max(composed.nodes)
                    uc = get_order(ue, λi)
                    composed.add_edge(uc, vc, label=fi.edges[ue, ve]['label'])
    return composed

def sub_compose2(composed, fi, λi):
    max_node = max(composed.nodes) if composed.nodes else 0 
    node_map = {i: λi[i] for i in range(len(λi))}  # Mapping fi nodes to composed nodes

    for node in fi.nodes(data=True):
        u = node[0]
        if u in node_map:
            composed_node = node_map[u]
        else:
            max_node += 1
            composed_node = max_node
            composed.add_node(composed_node, label=int(fi.nodes[u]['label']))  # Ensure label is int
            node_map[u] = composed_node

    for edge in fi.edges(data=True):
        ue, ve = edge[0], edge[1]
        uc = node_map.get(ue, ue)
        vc = node_map.get(ve, ve)
        composed.add_edge(uc, vc, label=int(fi.edges[ue, ve]['label']))  # Ensure label is int

    return composed

def get_order(n, λi):
    for i, val in enumerate(λi):
        if n == val:
            return i
    return -1

def compose(fi, fj, cs, λi, λj):  
    if λj == "inorder":
        λj = list(range(len(fj.nodes)))
    composed = copy.deepcopy(cs)
    sub_compose(fi, composed, λi)
    sub_compose(fj, composed, λj)
    return composed

def fi_compose(fi, q, λi):
    composed = copy.deepcopy(q)
    sub_compose2(composed, fi, λi)
    return composed

# fi = read_query_graph("f10.my")
# fj = read_query_graph("f13.my")
# cs = read_query_graph("f4.my")
# λ0 = [0, 2]
# λ1 = [2, 0]
# λj = [1, 2]
# λ3 = [0,1]

# f10 = fi_compose(fi, cs, λ0)
# drw(f10, "composed graph")
# f22 = compose(fi, fj, cs, λ0, λj)
# drw(f22, "composed graph")
# f18 = compose(fi, fj, cs, λ1, λj)
# drw(f18, "composed graph")