class Slot:
    def __init__(self) -> None:
        self.remainder = 0
        self.bucket_occupied = 0
        self.run_continued = 0
        self.is_shifted = False

class QuotientFilter:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.size = 2 ** q
        self.filter = [Slot() for _ in range(self.size)]

    def lookup(self, fingerprint):
        quotient, remainder = divmod(fingerprint, self.size)
        if not self.filter[quotient].bucket_occupied:
            return False
        
        b = quotient
        while (self.filter[b].is_shifted):
            b = b - 1
        s = b
        while b != quotient:
            s = s + 1
            while self.filter[s].run_continued:
                s = s + 1
            b = b + 1
            while not self.filter[b].bucket_occupied:
                b = b + 1
        
        while self.filter[s].remainder != remainder:
            s = s + 1
            if not self.filter[s].run_continued:
                return False
        return True
