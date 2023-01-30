import random
import socketserver
import string
from os.path import exists
from socket import socket
import bcrypt
from pymongo import MongoClient
import json
import hashlib
import base64
import re
import helpers


class MyTCPHandler(socketserver.BaseRequestHandler):
    global listofUser
    listofUser = []

    def handle(self):
        self.data = self.request.recv(2048)
        mongo_client = MongoClient("mongo")
        db = mongo_client["next-level"]
        tokenData = db["tokens"]
        userpass = db["userpass"]
        usertoken = db["usertoken"]
        teampts = db["teampts"]
        headersDict = helpers.requestParser(self.data)
        print(self.data)
        def GETfunctionjs():
            with open('functions.js', 'r') as file:
                jsLen = str(len(file.read()))
            with open('functions.js', 'r') as file:
                self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nContent-Length: " + jsLen + "\r\nContent-Type: text/javascript; charset=utf-8; \r\nX-Content-Type-Options: nosniff\r\n\r\n" + file.read()).encode())

        def GETstylecss():
            with open('style.css', 'r') as file:
                cssLen = str(len(file.read()))
            with open('style.css', 'r') as file:
                self.request.sendall((
                                             "HTTP/1.1 200 OK\r\nContent-Length: " + cssLen + "\r\nContent-Type: text/css; charset=utf-8; \r\nX-Content-Type-Options: nosniff\r\n\r\n" + file.read()).encode())

        # Start of Parsing -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if b"GET / HTTP/1.1" in self.data:
            allcookies = {}
            userDic = {}
            list1 = []
            with open('index.html', 'r') as file:
                ht = file.read()
            if b'cookie' in headersDict:
                allcookies = helpers.stringTomap(headersDict[b'cookie'])
            if b'cookie' not in headersDict:
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=1; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())
            elif int(allcookies[b'visits'].decode()) >= 1:
                user = ""
                if b'token' in allcookies:
                    user = usertoken.find_one({"token": allcookies[b'token'].decode()})["username"].decode()
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=" + str(int(
                    allcookies[
                        b'visits'].decode()) + 1) + "; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())

        elif b"GET /game HTTP/1.1" in self.data:
            allcookies = {}
            userDic = {}
            list1 = []
            user = ""
            with open('game.html', 'r') as file:
                ht = file.read()
            if b'cookie' in headersDict:
                allcookies = helpers.stringTomap(headersDict[b'cookie'])
                if int(allcookies[b'visits'].decode()) >= 1:
                    if b'token' in allcookies:
                        user = usertoken.find_one({"token": allcookies[b'token'].decode()})["username"].decode()
                        ht = ht.replace("{{team}}", user)
                    else:
                        user = '<button onclick="window.location.href="/login"">Login</button>'
                        ht = ht.replace("{{team}}", user)
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=" + str(int(
                    allcookies[
                        b'visits'].decode()) + 1) + "; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())
            if b'cookie' not in headersDict:
                ht = ht.replace("{{team}}", user)
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=1; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())




        elif b"GET /leaderboard HTTP/1.1" in self.data:
            allcookies = {}
            userDic = {}
            list1 = []
            leaderboarddic = {}
            with open('leaderboard.html', 'r') as file:
                ht = file.read()

            for i in teampts.find({}):
                for k in i:
                    if k != "_id":
                        if {k: i[k]} not in list1:
                            print({k: i[k]})
                            list1.append({k: i[k]})

            leader = ""
            for p in list1:
                for k in p:
                    h = p[k]
                    if h == "Q1" or h == "Q2" or h == "Q3" or h == "Q4" or h == "Q5" or h == "Q6" or h == "Q7" or h == "Q8" or h == "Q9" or h == "Q10":
                        if k in leaderboarddic:
                            v = leaderboarddic[k] + 10
                            leaderboarddic[k] = v
                        else:
                            leaderboarddic[k] = 10

            for i in leaderboarddic:
                leader += str(i) + ":" + str(leaderboarddic[i]) + "<br>"
            ht = ht.replace("{{leader}}", leader)
            if b'cookie' in headersDict:
                allcookies = helpers.stringTomap(headersDict[b'cookie'])
            if b'cookie' not in headersDict:
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=1; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())
            elif int(allcookies[b'visits'].decode()) >= 1:
                user = ""
                if b'token' in allcookies:
                    user = usertoken.find_one({"token": allcookies[b'token'].decode()})["username"].decode()
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=" + str(int(
                    allcookies[
                        b'visits'].decode()) + 1) + "; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())

        elif b"GET /mentors HTTP/1.1" in self.data:
            allcookies = {}
            userDic = {}
            list1 = []
            with open('mentors.html', 'r') as file:
                ht = file.read()

            if b'cookie' in headersDict:
                allcookies = helpers.stringTomap(headersDict[b'cookie'])
            if b'cookie' not in headersDict:
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=1; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())
            elif int(allcookies[b'visits'].decode()) >= 1:
                user = ""
                if b'token' in allcookies:
                    user = usertoken.find_one({"token": allcookies[b'token'].decode()})["username"].decode()

                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=" + str(int(
                    allcookies[
                        b'visits'].decode()) + 1) + "; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())

        elif b"GET /login HTTP/1.1" in self.data:
            allcookies = {}
            userDic = {}
            list1 = []
            with open('login.html', 'r') as file:
                ht = file.read()

            if b'cookie' in headersDict:
                allcookies = helpers.stringTomap(headersDict[b'cookie'])
            if b'cookie' not in headersDict:
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=1; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())
            elif int(allcookies[b'visits'].decode()) >= 1:
                user = ""
                if b'token' in allcookies:
                    user = usertoken.find_one({"token": allcookies[b'token'].decode()})["username"].decode()

                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=" + str(int(
                    allcookies[
                        b'visits'].decode()) + 1) + "; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())

        elif b"GET /schedule HTTP/1.1" in self.data:
            allcookies = {}
            userDic = {}
            list1 = []
            with open('schedule.html', 'r') as file:
                ht = file.read()
            if b'cookie' in headersDict:
                allcookies = helpers.stringTomap(headersDict[b'cookie'])
            if b'cookie' not in headersDict:
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=1; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())
            elif int(allcookies[b'visits'].decode()) >= 1:
                user = ""
                if b'token' in allcookies:
                    user = usertoken.find_one({"token": allcookies[b'token'].decode()})["username"].decode()

                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Length: " + str(
                    len(ht)) + "\r\nContent-Type: text/html; charset=utf-8; \r\nSet-Cookie: visits=" + str(int(
                    allcookies[
                        b'visits'].decode()) + 1) + "; Max-Age=3600;\r\nX-Content-Type-Options: nosniff;\r\n\r\n" + ht).encode())

        elif b"GET /style.css" in self.data:
            GETstylecss()

        elif b"GET /functions.js" in self.data:
            GETfunctionjs()

        elif b"/registeruser" in self.data:
            multipart = self.data[self.data.index(b'\r\n\r\n'):].split(
                b'--' + (headersDict[b'content-type'].split(b'boundary=')[1]))
            username = multipart[1].split(b'name="username"')[1].strip()
            password = multipart[2].split(b'name="regpass"')[1].strip()
            # salt and hash the password before storing it in a database
            salt = bcrypt.gensalt()
            passwordHash = bcrypt.hashpw(password, salt)
            userpass.insert_one({"username": username, "password": passwordHash})
            self.request.sendall(
                "HTTP/1.1 301 Moved Permanently\r\nLocation: /login\r\nContent-Length: 0\r\n\r\n".encode())

        elif b"/loginuser" in self.data:
            multipart = self.data[self.data.index(b'\r\n\r\n'):].split(
                b'--' + (headersDict[b'content-type'].split(b'boundary=')[1]))
            username = multipart[1].split(b'name="usernamel"')[1].strip()
            password = multipart[2].split(b'name="regpassl"')[1].strip()
            # check if the username is stored in the database
            if not userpass.find_one({"username": username}):
                self.request.send(bytes(
                    "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<html><head></head><body><p>Username not found</p></body></html>",
                    "utf-8"))
            # authenticate the password
            storedPasswordHash = userpass.find_one({"username": username})["password"]
            if bcrypt.checkpw(password, storedPasswordHash):
                token = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(200))
                tokenHash = hashlib.sha256(token.encode("utf-8")).hexdigest()
                usertoken.insert_one({"username": username, "token": tokenHash})
                tokenCookie = b"token=" + tokenHash.encode("utf-8") + b"; Max-Age=3600;"
                self.request.sendall(
                    b"HTTP/1.1 301 Moved Permanently\r\nLocation: /game\r\nSet-Cookie:" + tokenCookie + b"\r\nContent-Length: 0\r\n\r\n")
            else:
                self.request.send(bytes(
                    "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<html><head></head><body><p>Username not found</p></body></html>",
                    "utf-8"))

        elif b"/submit" in self.data:
            multipart = self.data[self.data.index(b'\r\n\r\n'):].split(
                b'--' + (headersDict[b'content-type'].split(b'boundary=')[1]))
            q1 = multipart[1].split(b'name="Q1"')[1].strip().decode()
            q2 = multipart[2].split(b'name="Q2"')[1].strip().decode()
            q3 = multipart[3].split(b'name="Q3"')[1].strip().decode()
            q4 = multipart[4].split(b'name="Q4"')[1].strip().decode()
            q5 = multipart[5].split(b'name="Q5"')[1].strip().decode()
            q6 = multipart[6].split(b'name="Q6"')[1].strip().decode()
            q7 = multipart[7].split(b'name="Q7"')[1].strip().decode()
            q8 = multipart[8].split(b'name="Q8"')[1].strip().decode()
            q9 = multipart[9].split(b'name="Q9"')[1].strip().decode()
            q10 = multipart[10].split(b'name="Q10"')[1].strip().decode()
            allcookies = helpers.stringTomap(headersDict[b'cookie'])
            user = usertoken.find_one({"token": allcookies[b'token'].decode()})["username"].decode()
            teampts.find({})
            if q1 == "XYZ":
                teampts.insert_one({user: "Q1"})
            if q2 == "ZXY":
                teampts.insert_one({user: "Q2"})
            if q3 == "123":
                teampts.insert_one({user: "Q3"})
            if q4 == "RTY":
                teampts.insert_one({user: "Q4"})
            if q5 == "YTR":
                teampts.insert_one({user: "Q5"})
            if q6 == "MNO":
                teampts.insert_one({user: "Q6"})
            if q7 == "NMO":
                teampts.insert_one({user: "Q7"})
            if q8 == "POL":
                teampts.insert_one({user: "Q8"})
            if q9 == "LOP":
                teampts.insert_one({user: "Q9"})
            if q10 == "951":
                teampts.insert_one({user: "Q10"})
            self.request.sendall(
                b"HTTP/1.1 301 Moved Permanently\r\nLocation: /leaderboard\r\nContent-Length: 0\r\n\r\n")
        
        elif b"GET /assets/img/mentors/" in self.data:
            data = self.data.decode().split(' ')
            filename = data[1].split('/')[-1]
            if exists('assets/img/mentors/' + filename):
                with open('assets/img/mentors/' + filename, 'rb') as file:
                    imagelen = str(len(file.read()))
                with open('assets/img/mentors/' + filename, 'rb') as file:
                    self.request.sendall(
                        b"HTTP/1.1 200 OK\r\nContent-Length: " + imagelen.encode() + b"\r\nContent-Type: image/jpeg; charset=utf-8; \r\nX-Content-Type-Options: nosniff\r\n\r\n" + file.read())
            else:
                self.request.sendall(
                    "HTTP/1.1 404 Not Found\r\nContent-Length: 25\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nError 404: Page Not Found".encode())
        elif b"GET /assets/img/others/" in self.data:
            data = self.data.decode().split(' ')
            filename = data[1].split('/')[-1]
            print(filename)
            if exists('assets/img/others/' + filename):
                with open('assets/img/others/'+ filename, 'rb') as file:
                    imagelen = str(len(file.read()))
                with open('assets/img/others/'+ filename, 'rb') as file:
                    self.request.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: " + imagelen.encode() + b"\r\nContent-Type: image/svg+xml; charset=utf-8; \r\nX-Content-Type-Options: nosniff\r\n\r\n" + file.read())
            else:
                self.request.sendall(
                    "HTTP/1.1 404 Not Found\r\nContent-Length: 25\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nError 404: Page Not Found".encode())

        else:
            self.request.sendall(
                "HTTP/1.1 404 Not Found\r\nContent-Length: 25\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nError 404: Page Not Found".encode())


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 3000
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
