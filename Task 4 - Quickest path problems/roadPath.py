
class Graph():
    
    def __init__(self):
        '''
        Initialises class
        Time complexity: O(1)
        Space complexity: O(1)
        Error handle: None
        Return: None
        Parameter: None
        Pre-requisite: None
        '''
        self.a = []
        self.minheap = []
        self.loclist = []
        self.service = []


    def buildGraph(self, filename):     # :SELF.A INITIALISED PERFECTLY, EACH INDEX AT SELF.A CONTAINS A LIST CONTAINING ALL [V,W] FROM THE INPUTED TEXT FILE:
        '''
        Builds adjacency list
        Time complexity: O(E+V)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        f = open(filename)
        max = 0
        # find max
        for line in f:
            line = line.strip().split(' ')
            u,v,w = line
            u = int(u)
            v = int(v)
            w = float(w)
            if u > max:
                max = u
            if v > max:
                max = v
        f.close()
        # initialise self.a
        self.a = []
        for i in range(max+1):
            self.a.append([1])
        # loop
        f = open(filename)
        for line in f:
            line = line.strip().split(' ')
            u,v,w = line
            u = int(u)
            v = int(v)
            w = float(w)
            self.a[u].append([v,w,1])


    def buildHeap(self, source, lst):    # :SELF.MINHEAP GETS INITIALISED PERFECTLY, WITH ROOT NODE AS SOURCE WITH WEIGHT 0 AND EVERYTHING ELSE WITH WEIGHT 0:
        '''
        Builds minheap
        Time complexity: O(E)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        added = [0] * len(lst)
        self.loclist = [None] * len(lst)
        self.minheap = []
        self.minheap.append( [source,0,None] )
        self.loclist[source] = 0
        added[source] = 1
        for pos in range(len(lst)):      # add all nodes in lst to the heap; loops V times
            if added[pos] == 0:
                if lst[pos][0] == 1:
                    self.minheap.append( [pos, float('inf'), None] )
                    self.loclist[pos] = len(self.minheap)-1
                    added[pos] = 1
                for linked_node in lst[pos][1:]: # add all linked nodes to the heap too; loops e times
                    if added[linked_node[0]] == 0:
                        if linked_node[2] == 1 and lst[linked_node[0]][0] == 1:
                            self.minheap.append( [linked_node[0], float('inf'), None] )
                            self.loclist[linked_node[0]] = len(self.minheap)-1
                            added[linked_node[0]] = 1


    def reposition(self, node):     # :WORKS:
        '''
        Repositions node to appropriate position
        Time complexity: O(logV)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        i = node
        parentI = (i-1)//2
        while (parentI >= 0) and (self.minheap[parentI][1] > self.minheap[i][1]):
            self.loclist[self.minheap[parentI][0]], self.loclist[self.minheap[i][0]] = i, parentI
            self.minheap[parentI], self.minheap[i] = self.minheap[i], self.minheap[parentI]
            i = parentI
            parentI = (i-1)//2
        i = node
        leftI = i*2+1
        rightI = i*2+2
        # while i > child, swap with smaller child (or bigger index if both are equal)
        while rightI < len(self.minheap) and (self.minheap[i][1] > self.minheap[leftI][1] or self.minheap[i][1] > self.minheap[rightI][1]):
            if self.minheap[rightI][1] < self.minheap[leftI][1]:
                swapI = rightI
            else:
                swapI = leftI
            self.loclist[self.minheap[i][0]], self.loclist[self.minheap[swapI][0]] = swapI, i
            self.minheap[i], self.minheap[swapI] = self.minheap[swapI], self.minheap[i]
            i = swapI
            leftI = i*2+1
            rightI = i*2+2
        #  check the left child before we exit
        if leftI < len(self.minheap) and self.minheap[i][1] > self.minheap[leftI][1]:
            iloc = self.minheap[i][0]
            swapiloc = self.minheap[leftI][0]
            self.loclist[iloc], self.loclist[swapiloc] = leftI, i
            self.minheap[i], self.minheap[leftI] = self.minheap[leftI], self.minheap[i]

    
    def quickestPath(self, source, target):
        '''
        Finds quickest path
        Time complexity: O(E)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        source = int(source)
        target = int(target)

        self.buildHeapDisreg(source, self.a)
        returnlist = []
        while len(self.minheap) > 0 and ( len(returnlist) == 0 or returnlist[-1][0] != target ):    # loops V times
            # self.printHeap()


            # pop and move last node to top
            pop = self.minheap[0]
            self.minheap[0] = self.minheap[-1]
            self.minheap = self.minheap[:-1]
            try:
                self.loclist[self.minheap[0][0]] = 0
            except:
                pass
            self.loclist[pop[0]] = None
            # reposition top node
            self.reposition(0)
            # update all adjacent node values and reposition within the heap
            lstAdjNodes = self.a[pop[0]][1:]
            for adjNode in lstAdjNodes:         # loops E times in total
                if self.loclist[adjNode[0]] != None:        # if adjacent node is in the heap
                    heappos = self.loclist[adjNode[0]]          # get position of adjcent node in heap
                    if pop[1]+adjNode[1] < self.minheap[heappos][1]:
                        self.minheap[heappos][1] = pop[1]+adjNode[1]
                        self.minheap[heappos][2] = pop[0]
                    # self.minheap[heappos][1] = min(self.minheap[heappos][1], pop[1]+adjNode[1])     # set weight of adjacent node to min(current value, pop.weight+adjnode.weight)
                    self.reposition(heappos)        # O(logV)
            returnlist.append( pop )


        # extract answer from returnlist
        if returnlist[-1][0] != target or returnlist[-1][1] == float('inf'):
            return [[],-1]
        else:
            templist = [returnlist[-1][0]]
            parent = returnlist[-1][2]
            weight = returnlist[-1][1]
            for i in range(len(returnlist)-1, -1, -1):
                if parent == returnlist[i][0]:  # found the parent node?
                    parent = returnlist[i][2]
                    templist.append(returnlist[i][0])
            templist.reverse()
            return (templist, weight)


    def augmentGraph(self, filename_camera, filename_toll):     # WORKS
        '''
        Updates adjacency list
        Time complexity: O(E)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename_camera, filename_toll
        Pre-requisite: None
        '''
        c = open(filename_camera)
        for i in c:
            node = int(i)
            self.a[node][0] = 0
        c.close()
        t = open(filename_toll)
        for i in t:
            u,v = i.strip().split()
            u = int(u)
            v = int(v)
            for lst in self.a[u][1:]:
                if lst[0] == v:
                    lst[2] = 0


    def quickestSafePath(self, source, target):
        '''
        Finds quickest safe path
        Time complexity: O(E)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        source = int(source)
        target = int(target)

        self.buildHeap(source, self.a)
        returnlist = []
        while len(self.minheap) > 0 and ( len(returnlist) == 0 or returnlist[-1][0] != target ):
            # self.printHeap()


            # pop and move last node to top
            pop = self.minheap[0]
            self.minheap[0] = self.minheap[-1]
            self.minheap = self.minheap[:-1]
            try:
                self.loclist[self.minheap[0][0]] = 0
            except:
                pass
            self.loclist[pop[0]] = None
            # reposition top node
            self.reposition(0)
            # update all adjacent node values and reposition within the heap
            lstAdjNodes = self.a[pop[0]][1:]
            for adjNode in lstAdjNodes:
                if self.loclist[adjNode[0]] != None:        # if adjacent node is in the heap
                    heappos = self.loclist[adjNode[0]]          # get position of adjcent node in heap
                    if pop[1]+adjNode[1] < self.minheap[heappos][1]:
                        self.minheap[heappos][1] = pop[1]+adjNode[1]
                        self.minheap[heappos][2] = pop[0]
                    # self.minheap[heappos][1] = min(self.minheap[heappos][1], pop[1]+adjNode[1])     # set weight of adjacent node to min(current value, pop.weight+adjnode.weight)
                    self.reposition(heappos)
            returnlist.append( pop )

        # extract answer from returnlist
        if returnlist[-1][0] != target or returnlist[-1][1] == float('inf') or self.a[source][0] == 0 or self.a[target][0] == 0:
            return [[],-1]
        else:
            templist = [returnlist[-1][0]]
            parent = returnlist[-1][2]
            weight = returnlist[-1][1]
            for i in range(len(returnlist)-1, -1, -1):
                if parent == returnlist[i][0]:  # found the parent node?
                    parent = returnlist[i][2]
                    templist.append(returnlist[i][0])
            templist.reverse()
            return (templist, weight)



    def buildHeapDisreg(self, source, lst):    # :SELF.MINHEAP GETS INITIALISED PERFECTLY, WITH ROOT NODE AS SOURCE WITH WEIGHT 0 AND EVERYTHING ELSE WITH WEIGHT 0:
        '''
        Builds minheap
        Time complexity: O(E)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        added = [0] * len(lst)
        self.loclist = [None] * len(lst)
        self.minheap = []
        self.minheap.append( [source,0,None] )
        self.loclist[source] = 0
        added[source] = 1
        for pos in range(len(lst)):      # add all nodes in lst to the heap
            if added[pos] == 0:
                self.minheap.append( [pos, float('inf'), None] )
                self.loclist[pos] = len(self.minheap)-1
                added[pos] = 1
            for linked_node in lst[pos][1:]: # add all linked nodes to the heap too
                if added[linked_node[0]] == 0:
                    self.minheap.append( [linked_node[0], float('inf'), None] )
                    self.loclist[linked_node[0]] = len(self.minheap)-1
                    added[linked_node[0]] = 1


    
    def addService(self, filename_service):
        '''
        Adds service to the graph
        Time complexity: O(V)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        self.service = []
        for line in open(filename_service):
            line = int(line.strip())
            self.service.append(line)


    def quickestDetourPath(self, source, target):
        '''
        Finds quickest detour
        Time complexity: O(ElogV)
        Space complexity: O(E+V)
        Error handle: None
        Return: None
        Parameter: filename
        Pre-requisite: None
        '''
        source = int(source)
        target = int(target)

        servicea = [None] * len(self.a)
        serviceb = [None] * len(self.a)

        # run dijkstra from source and save reults in returnlista
        self.buildHeapDisreg(source, self.a)
        returnlista = []
        while len(self.minheap) > 0:
            # pop and move last node to top
            pop = self.minheap[0]
            self.minheap[0] = self.minheap[-1]
            self.minheap = self.minheap[:-1]
            try:
                self.loclist[self.minheap[0][0]] = 0
            except:
                pass
            self.loclist[pop[0]] = None
            # reposition top node
            self.reposition(0)
            # update all adjacent node values and reposition within the heap
            lstAdjNodes = self.a[pop[0]][1:]
            for adjNode in lstAdjNodes:
                if self.loclist[adjNode[0]] != None:        # if adjacent node is in the heap
                    heappos = self.loclist[adjNode[0]]          # get position of adjcent node in heap
                    if pop[1]+adjNode[1] < self.minheap[heappos][1]:
                        self.minheap[heappos][1] = pop[1]+adjNode[1]
                        self.minheap[heappos][2] = pop[0]
                    self.reposition(heappos)
            servicea[pop[0]] = len(returnlista)
            returnlista.append( pop )

        # reverse self.a and create self.b ; and also add the location attribute     :WORKS:
        self.b = []
        for i in range(len(self.a)):
            self.b.append([1])

        for nodei in range(len(self.a)):
            for adjnode in self.a[nodei][1:]:
                weight = adjnode[1]
                self.b[adjnode[0]].append( [nodei, adjnode[1], 1] )       

        # run dijksta from target using self.b and record results in returnlistb
        self.buildHeapDisreg(target, self.b)
        returnlistb = []
        while len(self.minheap) > 0:
            # pop and move last node to top
            pop = self.minheap[0]
            self.minheap[0] = self.minheap[-1]
            self.minheap = self.minheap[:-1]
            try:
                self.loclist[self.minheap[0][0]] = 0
            except:
                pass
            self.loclist[pop[0]] = None
            # reposition top node
            self.reposition(0)
            # update all adjacent node values and reposition within the heap
            lstAdjNodes = self.b[pop[0]][1:]
            for adjNode in lstAdjNodes:
                if self.loclist[adjNode[0]] != None:        # if adjacent node is in the heap
                    heappos = self.loclist[adjNode[0]]          # get position of adjcent node in heap
                    if pop[1]+adjNode[1] < self.minheap[heappos][1]:
                        self.minheap[heappos][1] = pop[1]+adjNode[1]
                        self.minheap[heappos][2] = pop[0]
                    self.reposition(heappos)
            serviceb[pop[0]] = len(returnlistb)
            returnlistb.append( pop )

        # collate the results somehow we'll see
        minweight = float('inf')
        minStation = float('inf')
        weight = 0
        for station in self.service:
            posa = servicea[station]
            posb = serviceb[station]
            if posa == None or posb == None:
                continue
            if returnlista[posa][1] + returnlistb[posb][1] < minweight:
                minStation = returnlista[posa][0]
                minweight = returnlista[posa][1] + returnlistb[posb][1]

        if minStation == float('inf'):
            return [[],-1]

        returnlista = returnlista[:servicea[minStation]+1]
        returnlistb = returnlistb[:serviceb[minStation]+1]

        # extract answer from returnlista
        if returnlista[-1][0] != minStation or returnlista[-1][1] == float('inf'):
            return [[],-1]
        else:
            templist = [returnlista[-1][0]]
            parent = returnlista[-1][2]
            weight = returnlista[-1][1]
            for i in range(len(returnlista)-1, -1, -1):
                if parent == returnlista[i][0]:  # found the parent node?
                    parent = returnlista[i][2]
                    templist.append(returnlista[i][0])
            templist.reverse()
            returna = (templist, weight)
        # extract answer from returnlistb
        if returnlistb[-1][0] != minStation or returnlistb[-1][1] == float('inf'):
            return [[],-1]
        else:
            templist = [returnlistb[-1][0]]
            parent = returnlistb[-1][2]
            weight = returnlistb[-1][1]
            for i in range(len(returnlistb)-1, -1, -1):
                if parent == returnlistb[i][0]:  # found the parent node?
                    parent = returnlistb[i][2]
                    templist.append(returnlistb[i][0])
            templist.reverse()
            returnb = (templist, weight)
        
        returnb[0].reverse()
        returnlist = (returna[0] + returnb[0][1:], minweight)
        return returnlist
         
        

if __name__ == '__main__':
    g = Graph()
    g.buildGraph('basicGraph.txt')
    # print(g.quickestPath(17,29))
    # g.augmentGraph('camera.txt', 'toll.txt')
    # print(g.quickestSafePath(17,29))
    g.addService('service.txt')
    print(g.quickestDetourPath(20,29))
