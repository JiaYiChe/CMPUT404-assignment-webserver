#  coding: utf-8 
import socketserver
import os
import time
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#References:
#https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists-2/
#https://docs.python.org/2/library/socketserver.html
#https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
#https://http.dev/301
#

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        data = self.data.decode("utf-8")
        data = data.split("\r\n")
        #print ("Got a request of: %s\n" % data[0])
        #print ("Got a request of: %s\n" % data[1])
        method, path, HTTP = data[0].split(" ")
        #print ("url", path)
        #print ("Got a request of: %s\n" % path[-1])

        #check if required GET method
        if method == "GET":
            #check if path end with /, if not add it
            if path[-1] != "/" and "." not in path.split("/"):
                #print("yes")
                self.request.sendall(bytearray(f"HTTP/1.1 301 Moved Permanently\r\nLocation:{path+'/'}\r\n","utf-8"))
                return
            #check if directory is empty if so add index.html 
            fileNames = path.split("/")[1:]
            if fileNames[-1] =="":
                #print("--------------------",path)
                #print("--------------------",fileNames)
                fileNames[-1] = "index.html"
            #check if .html file added unnecessarily, if so remove it
            counter = 0
            for i in fileNames:
                if "." in i:
                    counter +=1

            if counter > 1:
                fileNames.pop()
            #remove empty strings from list
            fileNames = list(filter(None, fileNames))
            filePath = "./www"
            #format file path to check if file exists
            for i in fileNames:
                filePath = filePath+"/"+i
            #print("path",filePath)
            #check if file exists
            if os.path.exists(filePath):
                status = "HTTP/1.1 200 OK\r\n"
                contentType=""
                #check if file is html or css
                if ".html" in fileNames[-1]:
                    contentType = "Content-Type: text/html\r\n"
                elif ".css" in fileNames[-1]:
                    contentType = "Content-Type: text/css\r\n"
                #read file and store it
                f = open(filePath, "r")
                file = '\r\n'+f.read() #end header with \r\n to start body
                f.close()
                #send 200 status and file as body
                self.request.sendall(bytearray(status+contentType+file, "utf-8"))
                return
            #if file not found return 404
            else:
                self.request.sendall(bytearray(f"HTTP/1.1 404 Not Found\r\n",'utf-8'))
                return
        #if not GET method return 405
        else:
            self.request.sendall(bytearray(f"HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            return


        #self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
