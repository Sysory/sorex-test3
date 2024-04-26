import logging
import os

from user import User, UserData
from currency import Currency
from worker import Worker

class FileWorker(Worker):
    def __init__(self, path):
        self.filePath : str = path
        if (not os.path.isfile(path)):
            open(path, "w").close()

    def saveUser(self, user : User):
        userID = str(user.userData.userID)
        isExists = self.isUserExists(user)

        if (isExists):
            oldFile = ""
            oldLine = ""
            newFile = ""
            with open(self.filePath, "r") as f:
                for line in f:
                    if (line.startswith(f"{userID}")): oldLine = line
                    oldFile += line
            newFile = oldFile.replace(oldLine, f"{user}")
            with open(self.filePath, "w") as f:
                f.write(newFile)
        else:
            with open(self.filePath, "a") as f:
                f.write(f"{user}")

    def loadUser(self, userID : int) -> User:
        with open(self.filePath, "r") as f:
            for line in f:
                if line.startswith(str(userID)):
                    user = self.parseUser(line)
                    logging.info(f"Parsing user {user} from file")
                    return user
                else:
                    logging.warning(f"No user with id {userID} found")

    def loadUsers(self) -> list[User]:
        users = []
        with open(self.filePath, "r") as f:
            for line in f:
                user = self.parseUser(line)
                logging.info(f"Parsing user {user} from file")
                users.append(user)
        return users

    def isUserExists(self, user : User) -> bool:
        with open(self.filePath, "r") as f:
            for line in f:
                if (line.startswith(str(user.userData.userID))):
                    return True
            return False