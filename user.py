import logging
from currency import Currency

class UserData:
    userID : int = 0
    currencies : list[Currency] = []

    def __init__(self, userID, currencies : list[Currency] = []):
        self.userID = userID
        self.currencies = currencies

    def __str__(self):
        return ":".join(map(str, (self.userID, *self.currencies)))
    
    def getCurrency(self, currID : str):
        for curr in self.currencies:
            if currID == curr.id:
                return curr
        return None
    
    def getAllCurrencies(self):
        return [curr for curr in self.currencies]

class User:
    def __init__(self, userData : UserData):
        self.userData = userData
    
    def __str__(self):
        return str(self.userData)
    
    def hString(self):
        tmp = "Отслеживаемые валюты:\n"
        currs = self.userData.getAllCurrencies()
        if (len(currs) > 0):
            for curr in currs:
                tmp += f"{curr.id.upper()}: minVal: {curr.minVal}, maxVal: {curr.maxVal}\n"
        else:
            tmp += "Пока таких нет"
        return tmp

    def changeMinVal(self, currID : str, minVal : float):
        currID = currID.upper()
        curr = self.userData.getCurrency(currID)
        if (curr is not None):
            logging.info(f"Changing minVal of {currID} to {minVal} for {self.userData.userID}")
            curr.setMinVal(minVal)
        else:
            logging.warning(f"Currency {currID} for user {self.userData.userID} not found")

    def changeMaxVal(self, currID : str, maxVal : float):
        currID = currID.upper()
        curr = self.userData.getCurrency(currID)
        if (curr is not None):
            logging.info(f"Changing maxVal of {currID} to {maxVal} for {self.userData.userID}")
            curr.setMaxVal(maxVal)
        else:
            logging.warning(f"Currency {currID} for user {self.userData.userID} not found")

    def removeCurrency(self, currID : str):
        currID = currID.upper()
        curr = self.userData.getCurrency(currID)
        if (curr is not None):
            logging.info(f"Removing currency {currID} for user {self.userData.userID}")
            self.userData.currencies.remove(curr)
        else:
            logging.warning(f"Currency {currID} for user {self.userData.userID} not found")

if __name__ == "__main__":
    udata = UserData(-2281337)
    udata.currencies.append(Currency("BTC", 30.5, 35.5))
    udata.currencies.append(Currency("ETH", 60.5, 65.5))
    u = User(udata)
    print(u)
    print(u.userData.getAllCurrencies())
