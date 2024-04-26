import logging

from user import User, UserData
from currency import Currency

class Worker:
    def __init__(self):
        pass

    def saveUser(self, user : User):
        pass
    
    def loadUser(self, userID : int) -> User:
        pass

    def loadUsers(self) -> list[User]:
        pass

    def isUserExists(self, user : User):
        pass

    def parseUser(self, line : str) -> User:
        # uid:cid:minVal:maxVal:cid:minVal:maxVal
        data = line.split(":")
        userID = int(data[0])
        currs : list[Currency] = []
        for i in range(1, len(data) -1, 3):
            currID = data[i]
            currMinVal = data[i+1]
            currMaxVal = data[i+2]
            curr = Currency(currID, currMinVal, currMaxVal)
            currs.append(curr)
        udata = UserData(userID, currs)
        user = User(udata)
        return user
