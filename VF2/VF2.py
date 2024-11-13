from typing import List, Set
from VF2.Graph import Graph, Vertex, Edge, State

class Match:
    def __init__(self, s=None, id=None):
        self.s = s if s is not None else []  # match
        self.id = id  # graphDB id

class vf2:
    def __init__(self):
        self.DBGraph = []
        self.match = []
        self.QueryGraph = None
        self.QueryID = None
        self.pat = None
        self.revpat = None
        self.g = None
        self.revg = None
        self.m1 = []
        self.m2 = []
        self.tin1 = []
        self.tin2 = []
        self.tout1 = []
        self.tout2 = []
        self.n1 = []
        self.n2 = []
        self.ns1 = []
        self.ns2 = []
        self.t1 = []
        self.t2 = []
        self.pred1 = []
        self.pred2 = []
        self.succ1 = []
        self.succ2 = []
        self.allPairs = []
        self.candiPairs = []
        self.flagIn = False
        self.flagOut = False
        self.flagAll = False

    def init(self, db: List[Graph]):
        self.DBGraph.clear()
        self.DBGraph = db
        self.match.clear()

    def GenRevGraph(self, src: Graph, dst: Graph):
        dst.init()
        for i in range(src.vn):
            dst.addv(src.vtx[i].id, src.vtx[i].label)
        for i in range(src.en):
            dst.addse(src.edge[i].v, src.edge[i].u, src.edge[i].label)

    def CheckPrev(self, s: State, a: int, b: int) -> bool:
        tmp = list(set(self.m1) & set(self.pred1))
        for ite1 in tmp:
            flag = any(s.core1[ite1] == ite2 for ite2 in self.pred2)
            if not flag:
                return False
        return True

    def CheckSucc(self, s: State, a: int, b: int) -> bool:
        tmp = list(set(self.m1) & set(self.succ1))
        for ite1 in tmp:
            flag = any(s.core1[ite1] == ite2 for ite2 in self.succ2)
            if not flag:
                return False
        return True

    def CheckIn(self, s: State) -> bool:
        a = len(set(self.succ1) & set(self.tin1))
        b = len(set(self.succ2) & set(self.tin2))
        c = len(set(self.pred1) & set(self.tin1))
        d = len(set(self.pred2) & set(self.tin2))
        return (a <= b) and (c <= d)

    def CheckOut(self, s: State) -> bool:
        a = len(set(self.succ1) & set(self.tout1))
        b = len(set(self.succ2) & set(self.tout2))
        c = len(set(self.pred1) & set(self.tout1))
        d = len(set(self.pred2) & set(self.tout2))
        return (a <= b) and (c <= d)

    def CheckNew(self, s: State) -> bool:
        a = len(set(self.ns1) & set(self.pred1))
        b = len(set(self.ns2) & set(self.pred2))
        c = len(set(self.ns1) & set(self.succ1))
        d = len(set(self.ns2) & set(self.succ2))
        return (a <= b) and (c <= d)

    def CalDFSVec(self, s: State):
        self.m1.clear()
        self.m2.clear()
        self.tin1.clear()
        self.tin2.clear()
        self.tout1.clear()
        self.tout2.clear()
        self.n1.clear()
        self.n2.clear()
        self.ns1.clear()
        self.ns2.clear()
        self.t1.clear()
        self.t2.clear()

        for ite in s.s:
            self.m1.append(ite[0])
            self.m2.append(ite[1])
        self.m1.sort()
        self.m2.sort()

        self.tout1 = [i for i in range(self.pat.vn) if s.out1.get(i)]
        self.tout2 = [i for i in range(self.g.vn) if s.out2.get(i)]
        self.tin1 = [i for i in range(self.pat.vn) if s.in1.get(i)]
        self.tin2 = [i for i in range(self.g.vn) if s.in2.get(i)]
        self.n1 = list(range(self.pat.vn))
        self.n2 = list(range(self.g.vn))

        self.t1 = list(set(self.tin1) | set(self.tout1))
        self.t2 = list(set(self.tin2) | set(self.tout2))

        tmp = list(set(self.n1) - set(self.m1))
        self.ns1 = list(set(tmp) - set(self.t1))
        tmp = list(set(self.n2) - set(self.m2))
        self.ns2 = list(set(tmp) - set(self.t2))

    def CalCheckVec(self, s: State, a: int, b: int):
        self.pred1.clear()
        self.pred2.clear()
        self.succ1.clear()
        self.succ2.clear()
    
        # aPred
        i = self.revpat.head.get(a, -1)
        while i != -1:
            self.pred1.append(self.revpat.edge[i].v)
            i = self.revpat.edge[i].next
    
        # bPred
        i = self.revg.head.get(b, -1)
        while i != -1:
            self.pred2.append(self.revg.edge[i].v)
            i = self.revg.edge[i].next
    
        # aSucc
        i = self.pat.head.get(a, -1)
        while i != -1:
            self.succ1.append(self.pat.edge[i].v)
            i = self.pat.edge[i].next
    
        # bSucc
        i = self.g.head.get(b, -1)
        while i != -1:
            self.succ2.append(self.g.edge[i].v)
            i = self.g.edge[i].next
    
        self.pred1.sort()
        self.pred2.sort()
        self.succ1.sort()
        self.succ2.sort()

    def check(self, s: State, a: int, b: int) -> bool:
        if self.pat.vtx[a].label != self.g.vtx[b].label:
            return False
        self.CalCheckVec(s, a, b)
        return self.CheckPrev(s, a, b) and self.CheckSucc(s, a, b) and self.CheckIn(s) and self.CheckOut(s) and self.CheckNew(s)

    def GenPairs(self, s: State):
        self.CalDFSVec(s)
        self.flagIn = self.flagOut = self.flagAll = False
        self.allPairs.clear()

        for i in self.tout1:
            for j in self.tout2:
                self.allPairs.append((i, j))
        if self.allPairs:
            self.flagOut = True
            return

        for i in self.tin1:
            for j in self.tin2:
                self.allPairs.append((i, j))
        if self.allPairs:
            self.flagIn = True
            return

        t1 = [i for i in range(self.pat.vn) if s.core1.get(i) == -1]
        t2 = [i for i in range(self.g.vn) if s.core2.get(i) == -1]
        for i in t1:
            for j in t2:
                self.allPairs.append((i, j))
        self.flagAll = True

    def CheckPairs(self, s: State):
        self.candiPairs.clear()
        for pair in self.allPairs:
            if self.check(s, pair[0], pair[1]):
                self.candiPairs.append(pair)

    def UpdateState(self, s: State, a: int, b: int):
        s.core1[a] = b
        s.in1[a] = 0
        s.out1[a] = 0
        s.core2[b] = a
        s.in2[b] = 0
        s.out2[b] = 0
    
        i = self.pat.head.get(a, -1)
        while i != -1:
            v = self.pat.edge[i].v
            if s.core1.get(v) == -1:
                s.out1[v] = 1
            i = self.pat.edge[i].next
    
        i = self.revpat.head.get(a, -1)
        while i != -1:
            v = self.revpat.edge[i].v
            if s.core1.get(v) == -1:
                s.in1[v] = 1
            i = self.revpat.edge[i].next
    
        i = self.g.head.get(b, -1)
        while i != -1:
            v = self.g.edge[i].v
            if s.core2.get(v) == -1:
                s.out2[v] = 1
            i = self.g.edge[i].next
    
        i = self.revg.head.get(b, -1)
        while i != -1:
            v = self.revg.edge[i].v
            if s.core2.get(v) == -1:
                s.in2[v] = 1
            i = self.revg.edge[i].next
    
        s.s.append((a, b))

    def FinalCheck(self, s: State) -> bool:
        for i in range(self.pat.en):
            e1 = self.pat.edge[i]
            flag = False
            j = self.g.head.get(s.core1[e1.u], -1)
            while j != -1:
                e2 = self.g.edge[j]
                if e1.label == e2.label and s.core1[e1.v] == e2.v:
                    flag = True
                    break
                j = e2.next
            if not flag:
                return False
        return True
    
    def dfs(self, s: State, allmatchednodes: Set[int], gid: int) -> bool:
        if len(s.s) == self.pat.vn:
            if self.FinalCheck(s):
                # print("Matched!")
                self.tlist = s.s
                for i in range(self.g.vn + 1):
                    if s.core2.get(i) is not None and s.core2[i] != -1:
                        e = gid * 1000 + i
                        allmatchednodes.add(e)
    
                for i in range(self.pat.en):
                    e = self.pat.edge[i]
                    if s.core1.get(e.u) is not None and s.core1.get(e.v) is not None:
                        j = self.g.head.get(s.core1[e.u], -1)
                        while j != -1:
                            e2 = self.g.edge[j]
                            if (e2.u == s.core1[e.u] and e2.v == s.core1[e.v]) or (e2.u == s.core1[e.v] and e2.v == s.core1[e.u]):
                                edge_id = gid * 1000 + j
                                if j % 2 == 0:
                                    allmatchednodes.add(edge_id)
                            j = e2.next
                return True
    
        self.GenPairs(s)
        self.CheckPairs(s)
    
        vec = self.candiPairs[:]  # 复制一份 self.candiPairs
        m1t, m2t = self.m1[:], self.m2[:]
        tin1t, tin2t = self.tin1[:], self.tin2[:]
        tout1t, tout2t = self.tout1[:], self.tout2[:]
        n1t, n2t = self.n1[:], self.n2[:]
        ns1t, ns2t = self.ns1[:], self.ns2[:]
        t1t, t2t = self.t1[:], self.t2[:]
    
        for ite in vec:
            ns = State()
            ns.core1 = s.core1.copy()
            ns.core2 = s.core2.copy()
            ns.in1 = s.in1.copy()
            ns.in2 = s.in2.copy()
            ns.out1 = s.out1.copy()
            ns.out2 = s.out2.copy()
            ns.s = s.s[:]
            a, b = ite
            self.UpdateState(ns, a, b)
    
            self.m1, self.m2 = m1t[:], m2t[:]
            self.tin1, self.tin2 = tin1t[:], tin2t[:]
            self.tout1, self.tout2 = tout1t[:], tout2t[:]
            self.n1, self.n2 = n1t[:], n2t[:]
            self.ns1, self.ns2 = ns1t[:], ns2t[:]
            self.t1, self.t2 = t1t[:], t2t[:]
    
            ret = self.dfs(ns, allmatchednodes, gid)
    
            if ret:
                return True
    
        return False

    def query(self, allmatchednodes: Set[int], gid: int) -> bool:
        return self.dfs(State(), allmatchednodes, gid)

    def vf2(self, QG: Graph, QID: int, isOutput: bool, allmatchednodes: Set[int], matchedGraphIDs: List[int]) -> int:
        self.QueryGraph = QG
        self.QueryID = QID

        self.pat = self.QueryGraph
        self.revpat = Graph()
        self.GenRevGraph(self.pat, self.revpat)
        beforematched = len(allmatchednodes)
        ret = 0
        for i in range(len(self.DBGraph)):
            self.g = self.DBGraph[i]
            if self.pat.vn > self.g.vn or self.pat.en > self.g.en:
                continue
            self.revg = Graph()
            self.GenRevGraph(self.g, self.revg)
            temp = len(allmatchednodes)
            if self.query(allmatchednodes, i):
                if isOutput:
                    self.match.append(i)
                matchedGraphIDs.append(self.DBGraph[i].id)
                ret += 1
        return ret