import math
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, n, f):
        self.n = n
        self.f = f
        self.m = self.calculateM()
        self.k = self.calculateK()

        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)
        self.printParameters()

    def calculateM(self):
        return int(-math.log(self.f) * self.n / (math.log(2) ** 2))
    
    def calculateK(self):
        return int(self.m * math.log(2) / self.n)
    
    def printParameters(self):
        print("Init parameters:")
        print(f"n = {self.n}, f = {self.f}, m = {self.m}, k = {self.k}")

    def insert(self, item):
        for i in range(self.k):
            index = mmh3.hash(item, i) % self.m
            self.bit_array[index] = 1
    
    def lookup(self, item):
        for i in range(self.k):
            index = mmh3.hash(item, i) % self.m
            if self.bit_array[index] == 0:
                return False
        return True

bf = BloomFilter(10, 0.01)
bf.insert("1")
bf.insert("2")
bf.insert("42")

for i in range(1, 4):
    print(f"{i} {bf.lookup(str(i))}")

print(f"42 {bf.lookup('42')}")
print(f"43 {bf.lookup('43')}")

value = 43
while True:
    if bf.lookup(str(value)):
        print(f"False positive: {value}")
        break
    value += 1

