import os
import time
import shutil
from VF2.Graph import Graph
from VF2.VF2 import vf2

class Solver:
    def __init__(self):
        self.queryPath = []
        self.DBGraph = []
        self.QueryGraph = []
        self.outputPath = []
        self.isOutput = False
        self.vf2 = vf2()
        self.dbPath = ""
        self.δ = 1

    def init(self, _isOutput, _δ=1):
        with open("time.txt", "w") as fout:
            fout.write("")
        self.queryPath.clear()
        self.DBGraph.clear()
        self.QueryGraph.clear()
        self.outputPath.clear()
        self.isOutput = _isOutput
        self.δ = _δ

    def split(self, str, delim):
        return str.split(delim)

    def ReadFile(self, path, vec):
        vec.clear()
        with open(path, "r") as fin:
            tmp = Graph()
            for buff in fin:
                buff = buff.strip()
                if not buff:
                    if tmp:
                        vec.append(tmp)
                    continue
                if buff == "t # -1":
                    if tmp:
                        vec.append(tmp)
                    break
                if buff.startswith('t'):
                    parts = buff.split()
                    id = int(parts[2])
                    tmp = Graph()
                    tmp.appendid(id)
                elif buff.startswith('v'):
                    parts = buff.split()
                    m, l = int(parts[1]), int(parts[2])
                    tmp.addv(m, l)

                elif buff.startswith('e'):
                    if tmp:
                        parts = buff.split()
                        p, q, l = int(parts[1]), int(parts[2]), int(parts[3])
                        tmp.adde(p, q, l)
                        if len(self.QueryGraph) != 0:
                            # print(tmp.vn, self.QueryGraph[0].vn)
                            if abs(tmp.vn - self.QueryGraph[0].vn) >= self.δ:
                                tmp = None
                elif buff.startswith('['):
                    pass
                elif buff.isdigit():
                    pass
                else:
                    print("Error!")

    def ReadDB(self, path):
        self.ReadFile(path, self.DBGraph)

    def ReadQuery(self, path):
        self.ReadFile(path, self.QueryGraph)

    def input(self, pathsource, pathquery):
        self.dbPath = pathsource
        self.queryPath.append(pathquery)
        if os.path.exists("Output"):
            shutil.rmtree("Output")
        os.mkdir("Output")
        tt = "Output/ans"
        for i in range(len(self.queryPath)):
            self.outputPath.append(f"{tt}{i + 1}.txt")
        for path in self.outputPath:
            with open(path, "w") as fout:
                fout.write("")
        print("Start reading graphs")
        self.ReadDB(self.dbPath)
        print(f"Number of Targeted Graphs: {len(self.DBGraph)}")
        print("Read Data Finished!")

    def PrintQueryAns(self, id, cnt):
        with open(self.outputPath[id], "a") as fout:
            fout.write("+++++\n")
            fout.write(f"Query ID: {self.vf2.QueryID}\n")
            fout.write(f"Count: {len(self.vf2.match)}\n")
            fout.write("Match List:\n")
            for match in self.vf2.match:
                fout.write(f"{self.vf2.QueryID} {match}\n")
            fout.write("+++++\n\n")

    def solve(self):
        self.vf2.init(self.DBGraph)
        with open("time.txt", "a") as ftimeout:
            allmatchednodes = set()
            matchedGraphIDs = []
            for query_path in self.queryPath:
                print("Read Queries")
                # self.ReadQuery(query_path)
                print(f"Number of Query Graphs: {len(self.QueryGraph)}")
                stTime = time.time()
                for i, query in enumerate(self.QueryGraph):
                    print(f"Query {query_path}: {i}")
                    cnt = self.vf2.vf2(query, i, self.isOutput, allmatchednodes, matchedGraphIDs)
                edTime = time.time()
                dur = edTime - stTime
                ftimeout.write(f"{query_path} Time: {dur}\n")
                print(f"{query_path} Time: {dur}")
            print("Matched Graph IDs: ", " ".join(map(str, matchedGraphIDs)))
        return matchedGraphIDs
    
    def output(self):
        self.PrintQueryAns(0, 0)
        return self.vf2.match