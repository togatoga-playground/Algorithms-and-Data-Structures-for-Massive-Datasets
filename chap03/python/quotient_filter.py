class Slot:
    def __init__(self) -> None:
        self.remainder = -1
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
    
    def insert(self, fingerprint):
        quotient, remainder = divmod(fingerprint, self.size)
        b = quotient
        while self.filter[quotient].is_shifted:
            b = b - 1
        s = b
        while b != quotient:
            s = s + 1
            while self.filter[s].run_continued:
                s = s + 1
            b = b + 1
            while not self.filter[b].bucket_occupied:
                b = b + 1

        k = s
        while True:
            if self.filter[s].remainder == remainder:
                return
            if not self.filter[s].run_continued:
                k = s
                break
            s = s + 1
        kk = k
        while self.filter[kk].is_shifted:
            kk = kk + 1
        while kk != k:
            prev_filter = self.filter[kk - 1]
            self.filter[kk].remainder = prev_filter.remainder
            self.filter[kk].run_continued = prev_filter.run_continued
            self.filter[kk].is_shifted  = True
            kk = kk - 1

        self.filter[k].remainder = remainder
        self.filter[k].run_continued = self.filter[quotient].bucket_occupied
        self.filter[k].is_shifted = quotient != k
        self.filter[quotient].bucket_occupied = 1
