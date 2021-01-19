from flask import Flask
from chatbot import chatbot
app = Flask (__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/<apicall>')
def hello_user(apicall):
    file=open('log.txt','a')
    file.write(apicall+'\n')
    file.close()
    try:
        a = apicall.split("@2@")
        result = chatbot(a[0],a[1],a[2],a[3])

        return result
    except:
        return "no such command"

if __name__ == "__main__":
    app.run()
