from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import text
from user import User, UserData
from userManager import UserManager
from currency import Currency

router = Router()
uman = UserManager()

# TODO строку 12 и 14 перенести в UserManager
# cachedUsers : list[User] = []

def getUserFromMessage(msg : Message):
    user : User = loadOrSaveUser(User(UserData(msg.from_user.id)))
    return user

def loadOrSaveUser(user : User):
    # for u in cachedUsers:
    #     if (user.userData.userID == u.userData.userID):
    #         return u
    
    isExists = uman.isUserExists(user)
    if (isExists):
        user_ = uman.loadUser(user.userData.userID)
        # cachedUsers.append(user_)
        return user_
    else:
        uman.saveUser(user)
        # cachedUsers.append(user)
        return user

@router.message(Command("start"))
async def start_com_handler(msg: Message):
    user = getUserFromMessage(msg)
    await msg.answer(text=text.HELLOMSG.format(msg.from_user.first_name))

@router.message(Command("help"))
async def help_com_handler(msg: Message):
     await msg.answer(text=text.HELPMSG)

@router.message(Command("info"))
async def info_com_handler(msg: Message):
    user = getUserFromMessage(msg)
    await msg.answer(text=user.hString())

@router.message(Command("add"))
# BTC 33.3 44.4
async def add_com_handler(msg: Message):
    user = getUserFromMessage(msg)
    text = msg.text
    args = text.split(" ")
    if (len(args) != 4):
        await msg.answer(f"Введите команду снова, но передайте 3 аргумента (прим. /add BTC 60000 65000.34)")
        return
    
    _, currID, minVal, maxVal = args
    try:
        minVal = float(minVal)
        maxVal = float(maxVal)
    except:
        await msg.answer(f"Введенные аргументы не корректны. (прим. /add BTC 60000 65000.34)")
        return
    
    user.userData.currencies.append(Currency(currID, minVal, maxVal))
    uman.saveUser(user)
    await msg.answer(f"Валюта {currID.upper()} Добавлена!")

@router.message(Command("remove"))
async def remove_com_handler(msg: Message):
    user = getUserFromMessage(msg)
    text = msg.text
    args = text.split(" ")
    if (len(args) != 2):
        await msg.answer(f"Введите команду снова, но передайте 1 аргумент (прим. /remove BTC)")
        return
    else:
        _, currID = args
        currs = user.userData.currencies
        for curr in currs:
            if (curr.id.upper() == currID.upper()):
                user.removeCurrency(currID.upper())
                await msg.answer(f"Валюта {currID.upper()} удалена!")
    uman.saveUser(user)

# @router.message(Command("change"))
# async def change_com_handler(msg: Message):
#     user = getUserFromMessage(msg)

#     uman.saveUser(user)

