import logging

class Currency:
    def __init__(self, id, minVal = 0, maxVal = 0):
        self.id : str = id
        self.minVal : float = minVal
        self.maxVal : float = maxVal
    
    def __str__(self):
        return ":".join(map(str, (self.id, self.minVal, self.maxVal)) )

    def setMinVal(self, minVal : float):
        if (minVal < self.maxVal):
            self.minVal = minVal
        else:
            logging.warning(f"New minVal >= old maxVal ({minVal} >= {self.maxVal})")

    def setMaxVal(self, maxVal : float):
        if (maxVal > self.minVal):
            self.maxVal = maxVal
        else:
            logging.warning(f"New maxVal <= old minVal ({maxVal} <= {self.minVal})")

if __name__ == "__main__":
    c = Currency("BTC", 30000.5, 35000.5)
    print(c)
    c.setMinVal(10)
    print(c)
    c.setMaxVal(9)
    print(c)
    c.setMaxVal(11)
    print(c)