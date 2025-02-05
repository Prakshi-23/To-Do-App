# #  FIRST FLASK APP

from flask import Flask,render_template,request,redirect,url_for   

app = Flask(__name__)

import pymysql
#Global Variable, will use in different functions
db=None
cur=None

def connectDB():
    global db
    global cur

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='root',
                         database='flask_app')

    cur = db.cursor()

def disconnectDB():
    cur.close()
    db.close()   

def readallrecords():
    connectDB()
    insertquery='select * from todo'
    cur.execute(insertquery)
    result=cur.fetchall()
    disconnectDB
    return result

def insertrecord(task,status):
    connectDB()
    insertquery = f'insert into todo(task,status) values("{task}","{status}")'
    cur.execute(insertquery)
    db.commit()
    disconnectDB

def deleterecord(tid):
    connectDB()
    deletequery = f'delete from todo where sr_no={tid}'
    cur.execute(deletequery)
    db.commit()
    disconnectDB()
    
@app.route('/')
def index():
    data=readallrecords()
    #print(data)
    return render_template('index.html',data=data)

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/inserttask')
def inserttask():
    task = request.args.get('task')
    status = request.args.get('status')
    insertrecord(task,status)
    return redirect(url_for('index'))

@app.route('/delete/<tid>')
def delete(tid):
    deleterecord(tid)
    return redirect(url_for('index'))

@app.route('/update/<tid>')
def update(tid):
    data = readonerecord(tid)
    return render_template('update.html',data=data)

def readonerecord(tid):
    connectDB()
    selectquery = f'select * from todo where sr_no={tid}'
    cur.execute(selectquery)
    result = cur.fetchone()
    disconnectDB()
    return result

@app.route('/updatetask/<tid>')
def updatetask(tid):
    task = request.args.get('task')
    status = request.args.get('status')
    updaterecord(tid,task,status)
    return redirect(url_for('index'))

def updaterecord(tid,task,status):
    connectDB()
    updatequery=f'update todo set task="{task}", status="{status}" where sr_no={tid}'
    cur.execute(updatequery)
    db.commit()
    disconnectDB()
    

if __name__=='__main__':
    app.run(debug=True)                    
                    
    

    

