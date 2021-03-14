from bottle import route, post, run, request
import bottle
from phe import paillier
import pickle
import requests as rq
import sqlite3
#import bottle_mysql
# Configure db
conn = sqlite3.connect('test.db')
cur=conn.cursor()
cur.execute('''CREATE TABLE PRINTS
         (RNo CHAR(9) PRIMARY KEY NOT NULL,
         PRINT       CHAR(500));''')

app = bottle.Bottle()
# # dbhost is optional, default is localhost
#plugin = bottle_mysql.Plugin(dbuser='root', dbpass='root', dbname='')
#app.install(plugin)

@app.route('/',)
def front_page():
    return 'welcome to attendance management server'


@app.post('/register')  
def do_register():
    request_data = request.body.read()
    unpickled_data = pickle.loads(request_data)
    roll_number= unpickled_data['roll_number']
    enc_fingerprint = unpickled_data['fingerprint']
    print(roll_number,enc_fingerprint)
    pickled_print=pickle.dumps(enc_fingerprint)
    
    query = "INSERT INTO PRINTS  (RNo,PRINT) VALUES (\'{0}\',\'{1}\'');".format(roll_number,pickled_print)
    conn.execute(query);

    # do mysql creation and data addition

    # arr = [enc_fingerprint[i]+enc_fingerprint[i] for i in range(len(enc_fingerprint))]
    # print(arr)




@app.post('/mark')  # or @route('/login', method='POST')
def do_mark():
    request_data = request.body.read()
    unpickled_data = pickle.loads(request_data)
    roll_number= unpickled_data['roll_number']
    enc_fingerprint = unpickled_data['fingerprint']
    print(roll_number,enc_fingerprint)

    # do mysql querying and sending back the additon of paillier object
    # to the topic /verification



