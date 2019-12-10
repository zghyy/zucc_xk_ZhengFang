import json


def set_account():
    account = {"username": input("Username:"), "password": input("Password:")}
    account_file = open("account.json", "w")
    account_file.write(json.dumps(account))
    account_file.close()


def read_account():
    account_file = open("account.json", "r")
    account_data = json.load(account_file)
    account_file.close()
    return account_data
