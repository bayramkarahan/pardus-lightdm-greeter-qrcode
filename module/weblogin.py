#!/usr/bin/python3
#### Security Warning: This module is not support ssl. your password may leak!!!
####You should use stunnel for cypt http server connection.

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import subprocess
hostName = "0.0.0.0"
serverPort = 8080
userlist=[]

for k in lightdm.get_user_list():
	userlist = userlist+[k.get_name()]
       
#userlist=["etapadmin"]
#userlist=userlist+["ogretmen"]
#userlist=userlist+["ogrenci"]

usrlst=""
for i in userlist:
	usrlst=usrlst+"<option value='"+i+"'>"+i+"</option>"


uststring="""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

input[type=text],input[type=password], select, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

label {
  padding: 12px 12px 12px 0;
  display: inline-block;
}

input[type=submit] {
  background-color: #04AA6D;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  float: right;
  margin:20px 0px 0px 0px;
}

input[type=submit]:hover {
  background-color: #45a049;
}

.container {
  border-radius: 5px;
  background-color: #f2f2f2;
  padding: 20px;
}

.col-25 {
  float: left;
  width: 25%;
  margin-top: 6px;
}

.col-75 {
  float: left;
  width: 75%;
  margin-top: 6px;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Responsive layout - when the screen is less than 600px wide, make the two columns stack on top of each other instead of next to each other */
@media screen and (max-width: 600px) {
  .col-25, .col-75, input[type=submit] {
    width: 100%;
    margin-top: 0;
  }
}
</style>
</head>
<body>
<div class="container">
<h2 style="text-align:center;">Login Screen</h2>
 <form action="/" method="post">
<div class="row">
	<div class="col-25">        <label for="username"><b>Username</b></label>      </div>
      	<div class="col-75">        
<select name="username" id="fname">
"""

altstring="""
</select>

     </div>
    </div>

<div class="row">
    	<div class="col-25">        <label for="password"><b>Password</b></label>      </div>
      	<div class="col-75">        <input type="password" id="fpasswd" name="password" placeholder="Enter Password.." required>      </div>
    </div>

   
     <div class="row">
      <input type="submit" value="Login">
    </div>

</form> 
</div>

</body>
</html>
"""
login_page=uststring+usrlst+altstring

#login_page=login_page.format(usrlst)

from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs

class WebLogin(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(login_page.encode("utf-8"))

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                           self.rfile.read(length), 
                           keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        postvars = self.parse_POST()
        print(postvars,file=sys.stderr)
        
        #loginwindow.o("ui_entry_username").set_text(postvars[b'username'][0].decode("utf-8"))
        #loginwindow.o("ui_entry_password").set_text(postvars[b'password'][0].decode("utf-8"))
        #subprocess.run(["/usr/bin/sshlogin", postvars[b'username'][0].decode("utf-8"),postvars[b'password'][0].decode("utf-8")]) 
        #lightdm.set(
        #    username = postvars[b'username'][0].decode("utf-8"),
        #    password = postvars[b'password'][0].decode("utf-8")
        #)
        #lightdm.login()
        os.system("echo 'qrcode:"+postvars[b'username'][0].decode("utf-8")+":"+postvars[b'password'][0].decode("utf-8")+"' | netcat localhost 7777 &")

@asynchronous
def module_init():      
    webServer = HTTPServer((hostName, serverPort), WebLogin)
    print("Server started http://%s:%s" % (hostName, serverPort),file=sys.stderr)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.",file=sys.stderr)
