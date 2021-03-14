from bottle import route, post, run, request
import bottle
from phe import paillier
import pickle
import requests as rq
import sqlite3

app = bottle.Bottle()
# Configure db
conn = sqlite3.connect('test.db')
cur=conn.cursor()
try:
  cur.execute('''CREATE TABLE PRINTS
          (RNo CHAR(9) PRIMARY KEY NOT NULL,
          PRINT       CHAR(500));''')
  conn.commit()
except:
  print("table already exist")


# # # dbhost is optional, default is localhost
# plugin = bottle_mysql.Plugin(dbuser='root', dbpass='root', dbname='db')
# app.install(plugin)

@app.route('/',)
def front_page():
    return 'welcome to attendance management server'


@app.post('/register')  
def do_register():
    request_data = request.body.read()
    unpickled_data = pickle.loads(request_data)
    roll_number= unpickled_data['roll_number']
    enc_fingerprint = unpickled_data['fingerprint']
    # print(roll_number,enc_fingerprint)
    pickled_print=pickle.dumps(enc_fingerprint)
    
    #conn.execute("INSERT INTO PRINTDB (RNo,PRINT) \
    #  VALUES ('B170226CS','28,32,24,85,65,75,15');");

    """
    Example format :

    query = u'''insert into testtable VALUES(?)'''
    b = sqlite3.Binary(binarydata)
    cur.execute(query,(b,))
    con.commit()

    """

    
    query = '''INSERT INTO PRINTS (RNo,PRINT) VALUES (?,?);'''
    b = sqlite3.Binary(pickled_print)
    cur.execute(query,(roll_number,b))

    # .format(roll_number,pickled_print)
    #print(query)
    # print(type(roll_number))
    # print(type(pickled_print))
    #query = "INSERT INTO PRINTS (RNo,PRINT) VALUES ("+ roll_number +","+pickled_print+");"

    #print(query)
    # cur.execute(query);

    conn.commit()
    # do mysql creation and data addition
    
    # arr = [enc_fingerprint[i]+enc_fingerprint[i] for i in range(len(enc_fingerprint))]
    # print(arr)




@app.post('/mark')  # or @route('/login', method='POST')
def do_mark():
    request_data = request.body.read()
    unpickled_data = pickle.loads(request_data)
    roll_number= unpickled_data['roll_number']
    enc_fingerprint = unpickled_data['fingerprint']
    #print(roll_number,enc_fingerprint)
    
    #query = "select PRINT from PRINTS where RNo = \'{0}\';".format(roll_number)
    #print(query)
    """
    example format:

    curr.execute("select data from table limit 1")
    for row in curr:
       data = cPickle.loads(str(row['data'])) 

    """
    query = "select PRINT from PRINTS where RNo= ?"
    it=cur.execute(query,(roll_number,))
    for row in it:
      unpickled_fp_from_db = pickle.loads(row[0])
      # print(unpickled_fp_from_db)
    fingerprint_sums = [unpickled_fp_from_db[i]+enc_fingerprint[i] for i in range(len(enc_fingerprint))]
    print("fingerprint sums ",fingerprint_sums)
    #need to send back the fingerprint sums
    # storing send data in a dictionary
    send_data = {"roll_number": roll_number,"fingerprint":fingerprint_sums}
    # pickle the dictionary
    data = pickle.dumps(send_data, protocol=2)
    # post url
    url = "https://pallierattendanceclient.justinepdevasia.repl.co/verification"
    # post
    # print(data)
    post_result=rq.post(url,data=data)
    print(post_result)
    if post_result.status_code == 200:
      print("data send successfully")
    else:
      print("error in sending data")
    return 'fine'

    # do mysql querying and sending back the additon of paillier object
    # to the topic /verification

app.run(host='0.0.0.0', port=8080, debug=True)
