#-*- encoding:utf-8 -*-
# Bitly pys60v2.0 app by gauravssnl
# Requires simplejson v2.1.6 compatible with Python 2.5.4 fixed and ported by me
#thanks to Jehiah Czebotar who is author of bitly_api
# based on bitly_api v0.3

import appuifw
import e32
import Console
import os
import globalui
import bitly_api
__author__ = 'gauravssnl'
__version__ = '1.0.0'
lock = e32.Ao_lock()
sleep = e32.ao_sleep
config = 'bitlysettings.ini'
ru=lambda x: x.decode("utf8","ignore")
ur=lambda x: x.encode("utf8","ignore")
title = ru("Bit.ly")
console = Console.Console(True)
try :
    ACCESS_TOKEN = open(config).read().replace(" ", "").strip()
    
except:
    ACCESS_TOKEN = ""
def startup():
    global bd
    appuifw.app.title = title
    bd = console.text
    appuifw.app.body = bd
    bd.font = 'title',22
    bd.color = 255,0,0
    write('Bit.ly app v1.00.0 by gauravssnl ')
    bd.font = 'title',20
    bd.color = 0,0,255
    write('(I am just a student who failed)')
    bd.color = 255,0,255
    write('Thanks to bitly_api Author Jehiah Czebotar')
    bd.color =0,0,0
    write('---------------------------------------')
    
    
    
def clear():
    global bd
    bd.clear()
    start()    

def write(text):
    global bd
    console.write(ru(text))
    console.write(ru("\n"))

def app():
    startup()
    global bd
    bd.color = 100,0,100
    write('This is  bit.ly  URL shortener app for Symbian.')
    write('Short URLS can be used for sharing links on social networking sites like Twitter & Blogs.This app can expand bit.ly URL links also.To know more ,click on About')
    bd.color =0,0,0
    write('---------------------------------------')
    if ACCESS_TOKEN == "":
        appuifw.app.menu = [(ru("Settings"), settings),(ru('About'),about),(ru("Exit"), exit) ]
        
    else :
        appuifw.app.menu = [(ru("Connect"), connect_user),(ru('Settings'),settings),(ru('About'),about),(ru("Exit"), exit) ]
    

def connect_user():
    global bitly,ACCESS_TOKEN,bd
    bitly = bitly_api.Connection(access_token = ACCESS_TOKEN)
    try:
        data = bitly.user_info()
        bd.color = 100,0,0
        write("User Details")
        bd.color = 255,0,255
        console.write(ru('Username:  '))
        bd.color = 0,0,255
        write(ru(data['display_name'] ) )
        bd.color = 255,0,255
        console.write(ru('Full Name:  '))
        bd.color = 0,0,255
        write(ru(data['full_name'] ))
        bd.color = 0,0,0
        write('---------------------------------------')
        appuifw.app.menu = [(ru("Generate"), generate),(ru('Expand'),expand),(ru('About'),about),(ru("Exit"), exit) ]
    except :
        bd.color = 255,0,255
        write("Invalid Access Token or Connection Failed")
        write("Try Again.")
        bd.color = 0,0,0

def generate():
    global bitly 
    url = appuifw.query(ru("Enter URL:"),"text",ru("http://google.com/") ) 
    if url is not None and ur(url):
        url = ur(url).strip().replace(' ', '')
        
        bd.color = 255,0,255
        write("Original URL:")
        bd.color = 0,0,200
        write(url)
        bd.color = 255,0,255
        write("Generating bit.ly short link")
        if url.find('://') ==-1:
            url = 'http://'+url
        
        sleep(0.001)
        data = bitly.shorten(url)
        bd.color = 255,0,255
        write("bit.ly short URL :")
        bd.color = 0,0,200
        write (data["url"])
        bd.color = 0,0,0
        
def settings():
    global ACCESS_TOKEN
    q = appuifw.query(ru("Enter bit.ly Access Token "),'text', ru(ACCESS_TOKEN) )
    if q :
        ACCESS_TOKEN = ur(q).strip().replace(" ","")
        open(config,"w").write(ACCESS_TOKEN)
        appuifw.app.menu = [(ru("Connect"), connect_user),(ru('Settings'),settings),(ru('About'),about),(ru("Exit"), exit) ]

def expand():
    global bd,bitly
    url = appuifw.query(ru('Enter bit.ly link to expand:'),'text')
    e32.ao_sleep(0.0001)
    if url :
        url = ur(url).strip().replace(' ' ,'')
        
        bd.color = 255,0,255
        write('Bit.ly URL:')
        bd.color = 0,0,200
        write(url)
        if url.find('://') ==-1:
            url = 'http://'+url
        bd.color = 255,0,255
        write('Expanding bit.ly URL')
        e32.ao_sleep(0.0001)
        data = bitly.expand(link = url)
        
        
        if  'long_url' in data[0] :
            bd.color = 255,0,255
            write('Expanded Original URL:')
            bd.color = 0,0,200
            write(str(data[0]['long_url']))
        elif 'error' in data[0]:
             bd.color = 0,0,200
             write('Error')
            
            
                 
        
def exit():
    os.abort()
    
def about():
    globalui.global_msg_query(ru('Developer:gauravssnl\nThanks:Jehiah Czebotar(API),Brian Bustos(Icon)\nTo use this app ,you need to login to your bit.ly account &get your  Access Token.Use that Access token in this app.After that,you can generate bit.ly short links and expand bit.ly links to get original link'),ru('Bit ly app v1.00.0 '))                
          
e32.ao_yield()
appuifw.app.screen = 'normal'    
app()

lock.wait()



