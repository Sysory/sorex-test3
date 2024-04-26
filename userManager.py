import logging

from user import User, UserData
from currency import Currency

from worker import Worker
from fileWorker import FileWorker

class UserManager:
    def __init__(self, worker : Worker = FileWorker("db.txt")):
        self.worker : Worker = worker

    def saveUser(self, user : User):
        self.worker.saveUser(user)
    
    def loadUser(self, userID) -> User:
        return self.worker.loadUser(userID)
    
    def loadUsers(self) -> list[User]:
        return self.worker.loadUsers()

    def isUserExists(self, user : User) -> bool:
        return self.worker.isUserExists(user)

if __name__ == "__main__":
    um = UserManager()
    print(type(um.worker))