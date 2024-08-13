import math
class BloomFilter:
    def __init__(self, n, f):
        self.n = n
        self.f = f

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

