from flask import Flask
from flask import render_template, redirect,url_for
from flask import request

from jsonrpc.backend.flask import api
from flask_cors import *

import base64
from Crypto.Cipher import AES

from datetime import date
import time

app = Flask(__name__,static_url_path='')    
CORS(app, supports_credentials=True)
app.register_blueprint(api.as_blueprint())

@app.route('/', methods=['get','POST'])
def index():
   return render_template('index.html')

@api.dispatcher.add_method
def my_add(a,b):
   a = int(a)
   b = int(b)
   return  a+b

@api.dispatcher.add_method
def Convert(num,scale0,scale1):
    if scale0 == "Binary" and scale1 == "Decimal":
        result = int(num,2)
    if scale0 == "Binary" and scale1 == "Hexadecimal":
        result = hex(int(num,2))
    if scale0 == "Decimal" and scale1 == "Binary":
        num = int(num)
        result = bin(num)    
    if scale0 == "Decimal" and scale1 == "Hexadecimal":
        num = int(num)
        result = hex(num)
    if scale0 == "Hexadecimal" and scale1 == "Binary":
        result = bin(int(num,16))
    if scale0 == "Hexadecimal" and scale1 == "Decimal":
        result = int(num,16)
    return result

@api.dispatcher.add_method
def AEScode(text,flag):
    AES_key = "meaqua774tietie"
    aes = AES.new(add_16bit(AES_key), AES.MODE_ECB) 
    if flag == "Encryption":
        Encryption = str(base64.encodebytes(aes.encrypt(add_16bit(text))),
        encoding='utf8').replace('\n', '')
        return   Encryption
    else:
        Decryption = str(aes.decrypt(base64.decodebytes(bytes(text, 
        encoding='utf8'))).rstrip(b'\0').decode("utf8"))
        return   Decryption

def add_16bit(t):
    while len(t) % 16 != 0:
        t += '\0'
    return str.encode(t)

@api.dispatcher.add_method
def comparetime(stringtime):
    nowtime = date.today()
    if isinstance(nowtime,date):
        pass
    else:
        nowtime=convertstringtodate(nowtime)

    if isinstance(stringtime,date):
        pass
    else:
        stringtime=convertstringtodate(stringtime)
        result=nowtime-stringtime
    return result.days

def convertstringtodate(stringtime):
    year=stringtime[0:4]
    month=stringtime[4:6]
    day=stringtime[6:8]
    begintime=date(int(year),int(month),int(day))
    return begintime

@api.dispatcher.add_method
def LogicNum(num1,num2,nmeth):
    if nmeth == "AND":
        return bin(int(num1,2) & int(num2,2))
    if nmeth == "OR":
        return bin(int(num1,2) | int(num2,2))
    if nmeth == "XOR":
        return bin(int(num1,2) ^ int(num2,2))

if __name__ == "__main__":
    app.run(debug = True)

