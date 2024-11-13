class Vertex:
    def __init__(self, id, label):
        self.id = id
        self.label = label
        self.seq = -1
        self.del_flag = False

class Edge:
    def __init__(self, u, v, label, next_edge):
        self.u = u
        self.v = v
        self.label = label
        self.next = next_edge
        self.del_flag = False

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v and self.label == other.label
    
class Graph:
    maxv = 850
    maxe = 850

    def __init__(self):
        self.head = {i: -1 for i in range(Graph.maxv)}
        self.vtx = {}
        self.edge = []
        self.vn = 0
        self.en = 0
        self.id = -1

    def init(self):
        self.head = {i: -1 for i in range(Graph.maxv)}
        self.vtx = {}
        self.edge = []
        self.vn = 0
        self.en = 0
        
    def appendid(self, id):
        self.id = id

    def addv(self, id, label):
        self.vtx[id] = Vertex(id, label)
        self.vn += 1

    def is_empty(self):
        return self.vn == 0 and self.en == 0
    
    def addse(self, u, v, label):
        new_edge = Edge(u, v, label, self.head[u])
        self.edge.append(new_edge)
        self.head[u] = self.en
        self.en += 1

    def adde(self, u, v, label):
        self.addse(u, v, label)
        self.addse(v, u, label)

    def delse(self, u, v, label):
        i = self.head[u]
        while i != -1:
            if self.edge[i].u == u and self.edge[i].v == v and self.edge[i].label == label:
                self.edge[i].del_flag = True
                return
            i = self.edge[i].next

    def dele(self, u, v, label):
        i = self.head[u]
        while i != -1:
            if self.edge[i].u == u and self.edge[i].v == v and self.edge[i].label == label:
                self.edge[i].del_flag = True
                self.edge[i ^ 1].del_flag = True
                return
            i = self.edge[i].next

class State:
    def __init__(self):
        self.core1 = {}
        self.core2 = {}
        self.in1 = {}
        self.in2 = {}
        self.out1 = {}
        self.out2 = {}
        self.s = []
        for i in range(Graph.maxv):
            self.core1[i] = -1
            self.core2[i] = -1
            self.in1[i] = 0
            self.in2[i] = 0
            self.out1[i] = 0
            self.out2[i] = 0