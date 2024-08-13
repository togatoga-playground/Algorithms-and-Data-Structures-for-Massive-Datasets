class Node:
    def __init__(self, hashvValue):
        self.hashValue = hashvValue
        self.fingerTable = []
        self.resources = {}
        self.next = None
        self.previous = None


class HashRing:
    def __init__(self, k):
        self.head = None
        self.k = k
        self.min = 0
        self.max = 2**k - 1

    def leagalRange(self, hashValue):
        return self.min <= hashValue <= self.max

    def distance(self, a, b):  # a -> b
        if a == b:
            return 0
        elif a < b:
            return b - a
        else:
            return (2 ** self.k) + b - a

    def addNode(self, hashValue):
        if self.leagalRange(hashValue):
            newNode = Node(hashValue)
            if self.head is None:
                newNode.next = newNode
                newNode.previous = newNode
                self.head = newNode
                print("Adding a head node" + str(hashValue) + "...")
            else:
                temp = self.lookupNode(hashValue)
                newNode.next = temp
                newNode.previous = temp.previous
                newNode.previous.next = newNode
                newNode.next.previous = newNode
                print("Adding a node" + str(hashValue) + ". Its prev is " + str(
                    newNode.previous.hashValue) + ", and its next is " + str(newNode.next.hashValue) + ".")
                self.moveResources(newNode, newNode.next, False)
                if hashValue < self.head.hashValue:
                    self.head = newNode

    def moveResources(self, dest, orig, deleteTrue):
        delete_list = []
        for i,  j in orig.resources.items():
            if deleteTrue or (self.distance(i, dest.hashValue) < self.distance(i, orig.hashValue)):
                dest.resources[i] = j
                delete_list.append(i)
                print("\tMoving a resource " + str(i) + " from " +
                      str(orig.hashValue) + " to " + str(dest.hashValue) + ".")
        for i in delete_list:
            del orig.resources[i]

    def addResource(self,  hashValueResource):
        if self.leagalRange(hashValueResource):
            print("Adding a resource " + str(hashValueResource) + "...")
            targetNode = self.lookupNode(hashValueResource)
            if targetNode is not None:
                value = "Dummy resource value of " + str(hashValueResource)
                targetNode.resources[hashValueResource] = value
            else:
                print("Can't add a resource to an empty hashring.")

    def removeNode(self, hashValue):
        temp = self.lookupNode(hashValue)
        if temp.hashValue == hashValue:
            print("Removing a node " + str(hashValue) + "...")
            self.moveResources(temp.next, temp, True)
            temp.previous.next = temp.next
            temp.next.previous = temp.previous
            if temp == self.head:
                self.head = temp.next
                if self.head == self.head.next:
                    self.head = None
            return temp.next
        else:
            print("Nothing to remove.")

    def chordLookupNode(self, hashValue):
        if self.leagalRange(hashValue):
            temp = self.head
            if temp is None:
                return None
            else:
                while True:
                    if temp.hashValue == hashValue:
                        return temp
                    if self.distance(temp.hashValue, hashValue) > self.distance(temp.previous.hashValue, hashValue):
                        return temp
                    if self.distance(temp.hashValue, hashValue) < self.distance(temp.next.hashValue, hashValue):
                        return temp.next
                    result = temp
                    for i, node in enumerate(temp.fingerTable):
                        finger = 2**i + temp.hashValue
                        if finger > self.max:
                            finger = finger - 2**self.k
                        if finger == hashValue:
                            return node
                        if self.distance(finger, hashValue) < self.distance(result.hashValue, hashValue):
                            result = node                                        
                    
                    if result == temp:
                        return result
                    temp = result

    def lookupNode(self, hashValue):
        if self.leagalRange(hashValue):
            tmp = self.head
            if tmp is None:
                return None
            else:
                while (self.distance(tmp.hashValue, hashValue) > self.distance(tmp.next.hashValue, hashValue)):
                    tmp = tmp.next
                if tmp.hashValue == hashValue:
                    return tmp
                return tmp.next

    def buildFingerTable(self):
        if self.head is None:
            print("Empty hashring.")
        else:
            temp = self.head
            while (True):
                temp.fingerTable = []
                for i in range(0, self.k):
                    node = 2**i + temp.hashValue
                    if node > self.max:
                        node = node - 2**self.k
                    result = self.lookupNode(node)
                    temp.fingerTable.append(result)
                temp = temp.next
                if (temp == self.head):
                    break

    def printHashRing(self):
        print("*****")
        print("Printing tthe hashring in clockwise order:")
        temp = self.head
        if self.head is None:
            print("Empty hashring.")
        else:
            while (True):
                print("Node: " + str(temp.hashValue) + ",", end=" ")
                print("Finger Table: ",end=" ")
                for i in temp.fingerTable:
                    print(str(i.hashValue) + " ", end="")
                
                print("Resources: ", end=" ")
                if not bool(temp.resources):
                    print("Empty", end="")
                else:
                    for i in temp.resources.keys():
                        print(str(i) + " ", end="")
                temp = temp.next
                print(" ")
                if (temp == self.head):
                    break
        print("*****")


hr = HashRing(5)
hr.addNode(12)
hr.addNode(18)
hr.addResource(24)
hr.addResource(21)
hr.addResource(16)
hr.addResource(23)
hr.addResource(2)
hr.addResource(29)
hr.addResource(28)
hr.addResource(7)
hr.addResource(10)
hr.printHashRing()

hr.addNode(5)
hr.addNode(27)
hr.addNode(30)
hr.printHashRing()


hr.removeNode(12)
hr.printHashRing()


hr.addNode(12)
hr.addNode(16)
hr.buildFingerTable()
hr.printHashRing()

for i in range(0, 2**5):
    print("Chord Lookup for " + str(i) + " is " + str(hr.chordLookupNode(i).hashValue) + ".")
