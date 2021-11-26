from flask import Flask, render_template, request
import cgi
import time
import pymonetdb
import psycopg2


# cursor.execute("Select * FROM people LIMIT 0")
# colnames = [desc[0] for desc in cursor.description]


query_runner = Flask(__name__)

@query_runner.route('/')
def enter_query() :
    return render_template('enter_query.html')

@query_runner.route('/runmyquery', methods=['POST'])
def runmyquery() :
    connection = psycopg2.connect(host="localhost",database="Flight_tracking",user="postgres",password="admin")
    cursor=connection.cursor()
    print_line = request.form['query']
    cursor.execute(print_line)
    mssg = cursor.fetchall()
    cursor.execute("Select * FROM (" + print_line + ") as xyz LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    connection.commit()
    return render_template('show_result.html', cols=colnames, mssg=mssg)

@query_runner.route('/userinsert', methods=['GET', 'POST'])
def userinsert() :
    newuser_id = request.form['userid'] 
    newuser_name = request.form['name']
    newuser_emailid = request.form['email']
    newuser_psswd = request.form['password']    
    connection = psycopg2.connect(host="localhost",database="Flight_tracking",user="postgres",password="admin")
    cursor=connection.cursor()
    print_line="insert into ft.user_details values(" + str(newuser_id) + ",\'"+ str(newuser_name) + "\',\'" + str(newuser_emailid) + "\',\'" + str(newuser_psswd) + "\')"
    cursor.execute(print_line)
    connection.commit()
    return render_template('pass.html') 

@query_runner.route('/pilotinsert', methods=['GET', 'POST'])
def pilotinsert() :
    newuser_id = request.form['pilotid'] 
    newuser_name = request.form['name']
    newuser_psswd = request.form['password']    
    newuser_hours = request.form['hours']    
    connection = psycopg2.connect(host="localhost",database="Flight_tracking",user="postgres",password="admin")
    cursor=connection.cursor()
    print_line="insert into ft.pilot values(" + str(newuser_id) + ",\'"+ str(newuser_name) + "\',\'" + str(newuser_psswd) + "\',\'" + str(newuser_hours) + "\')"
    cursor.execute(print_line)
    connection.commit()
    return render_template('pass.html') 

@query_runner.route('/getroute', methods=['GET', 'POST'])
def getroute() :
    fortripid = request.form['tripid']
    connection = psycopg2.connect(host="localhost",database="Flight_tracking",user="postgres",password="admin")
    cursor=connection.cursor()
    # print_line="set search_path to ft"
    # cursor.execute(print_line)
    print_line="select * from ((select trip_id, checkpoint_no, longitude, latitude, time from ft.sensor_details where trip_id = 2015) union (select * from ft.trip_checkpoints where trip_id = 2015 and checkpoint_no not in (select checkpoint_no from ft.sensor_details where trip_id = " + str(fortripid) + ") )) as t1 order by checkpoint_no"
    cursor.execute(print_line)    
    mssg = cursor.fetchall()
    cursor.execute("Select * FROM (select * from ((select trip_id, checkpoint_no, longitude, latitude, time from ft.sensor_details where trip_id = 2015) union (select * from ft.trip_checkpoints where trip_id = 2015 and checkpoint_no not in (select checkpoint_no from ft.sensor_details where trip_id = " + str(fortripid) + ") )) as t1 order by checkpoint_no) as xyz LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    connection.commit()
    return render_template('show_result.html', cols=colnames, mssg=mssg)


# @app.route('/user')
# @app.route('/user', methods=['POST'])
# def user() :
#     newuser_id = request.form['firstName'] 
#     newuser_name = request.form['lastName']
#     newuser_emailid = request.form['email']
#     newuser_psswd = request.form['password']    
#     return render_template('pass.html', id=newuser_id, n=newuser_name, eid=newuser_emailid, pss=newuser_psswd)


if __name__ == '__main__' :
    query_runner.run(debug=True)

# form_inputs = cgi.FieldStorage()
# newuser_id = form_inputs.getvalue('firstName')
# newuser_name = form_inputs.getvalue('lastName')
# newuser_emailid = form_inputs.getvalue('email')
# newuser_psswd = form_inputs.getvalue('password')
# print(newuser_id)
# print(newuser_name)
# print(newuser_emailid)
# print(newuser_psswd)

# connection = psycopg2.connect(host="localhost",database="Flight_tracking",user="postgres",password="admin")
# cursor=connection.cursor()
# cursor.execute('SELECT version()')
# db_version=cursor.fetchone()
# print(db_version)
# print_line="insert into ft.user_details values(221,'Henry Fogat','henry123@gmail.com','ghwfhu')"
# print_line="insert into ft.user_details values(" + str(newuser_id) + ",\'myname\', \'myemailid@gmail.com\', \'mypass\')" #, abc ",'henry123@gmail.com','ghwfhu')"
# print(print_line)
# cursor.execute(print_line)
# connection.commit()
# newuser_id = int(input('Enter your user id : '))
# newuser_name = input('Enter your name : ')
# newuser_emailid = input('Enter your email address : ')
# newuser_psswd = input('Enter your password : ')
# # print_line="insert into ft.user_details values(221,'Henry Fogat','henry123@gmail.com','ghwfhu')"
# print_line="insert into ft.user_details values(" + str(newuser_id) + ",\'myname\', \'myemailid@gmail.com\', \'mypass\')" #, abc ",'henry123@gmail.com','ghwfhu')"
# print(print_line)
# cursor.execute(print_line)
# connection.commit()

# print_line="select * from ft.user_details"
# print(print_line)
# cursor.execute(print_line)
# rows=cursor.fetchall()
# for r in rows:
#     # print(r)
#     print(str(r[0]) + " " + r[1] + " " + r[2] + " " + r[3])