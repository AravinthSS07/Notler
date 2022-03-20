from flask import *
from flask_mysqldb import *

#custom module
from mysqlcreate import accounttable
from mysqlcreate import notetittletable
from mysqlcreate import notetable
from gravatar import avatar

#creating tables and running it
accounttable()
notetittletable()
notetable()

app = Flask(__name__)

app.secret_key = 'Ar7'

#mysql database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'notler'

mysql = MySQL(app) #Hello

@app.route('/')
def main():
    username = request.cookies.get('username')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM account WHERE username = %s', (username, ))
    account = cursor.fetchone()
    if account:
        session['loggedin'] = True
        session['username'] = account['username']
        resume = make_response(redirect('/home'))
        return resume
    return render_template('home.html')

# Basic Sign In Sign Up Sign Out System

@app.route('/signin', methods = ['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = %s and password = %s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            msg = 'Logged In Sucessfully'          
            res = make_response(redirect('/home'))
            res.set_cookie('username',f'{username}',max_age=60*60*24*30)
            res.set_cookie('password',f'{password}',max_age=60*60*24*30)
            return res
        else:
            msg = 'Incorrect username/password'
            return render_template('signin.html', msg=msg)
    return render_template('signin.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    msg = ''
    color = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'cnfrmpassword' in request.form:
        username = request.form['username']
        email_id = request.form['email']
        password = request.form['password']
        note1tittle = 'Empty Note. Edit to add something'
        note2tittle = 'Empty Note. Edit to add something'
        note3tittle = 'Empty Note. Edit to add something'
        note4tittle = 'Empty Note. Edit to add something'
        note5tittle = 'Empty Note. Edit to add something'
        note1 = 'Empty Note. Edit to add something'
        note2 = 'Empty Note. Edit to add something'
        note3 = 'Empty Note. Edit to add something'
        note4 = 'Empty Note. Edit to add something'
        note5 = 'Empty Note. Edit to add something'
        cnfrmpassword = request.form['cnfrmpassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists'
            color = 'red-text'
        else:
            if password == cnfrmpassword:
                cursor.execute('INSERT INTO account VALUES (%s, %s, %s)', (username, email_id, password))
                cursor.execute('INSERT INTO notetittle VALUES (%s, %s, %s, %s, %s, %s)', (username, note1tittle, note2tittle, note3tittle, note4tittle, note5tittle))
                cursor.execute('INSERT INTO notes VALUES (%s, %s, %s, %s, %s, %s)', (username, note1, note2, note3, note4, note5))
                cursor.connection.commit()
                msg = 'Account created sucessfully'
                color = 'green-text'
                return render_template('home.html', msg=msg, color=color)
            else:
                color = 'red-text'
                msg = 'You have either not confirmed the password or you might have entered wrong password'
                return render_template('signup.html', color=color, msg=msg)
    return render_template('signup.html', msg=msg, color=color)

@app.route('/signout')
def singout():
    session.pop('loggedin', None)
    session.pop('username', None)
    res = make_response(redirect('/'))
    res.delete_cookie('username')
    res.delete_cookie('password')
    return res

#sign functions end here

# Functional Features Start here

@app.route('/home')
def home():
    if 'loggedin' in session:
        username = session['username']
        notecur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        notecur.execute('SELECT * FROM notes WHERE username = %s', (username, ))
        notes = notecur.fetchone()
        notecur.execute('SELECT * FROM notetittle WHERE username = %s', (username, ))
        tittle = notecur.fetchone()
        return render_template("todo.html", notes=notes, tittle=tittle)
    else:
        return redirect('/')

@app.route('/update1', methods = ['GET', 'POST'])
def updatenote1():
    notenum = '1'
    if 'loggedin' in session:
        if request.method == 'POST' and 'noteupdate' in request.form and 'notetittleupdate' in request.form:
            notetittle = request.form['notetittleupdate']
            noteupdate = request.form['noteupdate']
            username = session['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM notes WHERE username = %s', (username, ))
            cursor.execute('UPDATE notetittle SET note1tittle = %s WHERE username = %s', (notetittle, username))
            cursor.execute('UPDATE notes SET note1 = %s WHERE username = %s', (noteupdate, username))
            mysql.connection.commit()
            return redirect('/home')
        return render_template('update1.html', notenum=notenum)
    return redirect('/')

@app.route('/update2', methods = ['GET', 'POST'])
def updatenote2():
    notenum = '2'
    if 'loggedin' in session:
        if request.method == 'POST' and 'noteupdate' in request.form and 'notetittleupdate' in request.form:
            notetittle = request.form['notetittleupdate']
            noteupdate = request.form['noteupdate']
            username = session['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM notes WHERE username = %s', (username, ))
            cursor.execute('UPDATE notetittle SET note2tittle = %s WHERE username = %s', (notetittle, username))
            cursor.execute('UPDATE notes SET note2 = %s WHERE username = %s', (noteupdate, username))
            mysql.connection.commit()
            return redirect('/home')
        return render_template('update2.html', notenum=notenum)
    return redirect('/')

@app.route('/update3', methods = ['GET', 'POST'])
def updatenote3():
    notenum = '3'
    if 'loggedin' in session:
        if request.method == 'POST' and 'noteupdate' in request.form and 'notetittleupdate' in request.form:
            notetittle = request.form['notetittleupdate']
            noteupdate = request.form['noteupdate']
            username = session['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM notes WHERE username = %s', (username, ))
            cursor.execute('UPDATE notetittle SET note3tittle = %s WHERE username = %s', (notetittle, username))
            cursor.execute('UPDATE notes SET note3 = %s WHERE username = %s', (noteupdate, username))
            mysql.connection.commit()
            return redirect('/home')
        return render_template('update3.html', notenum=notenum)
    return redirect('/')

@app.route('/update4', methods = ['GET', 'POST'])
def updatenote4():
    notenum = '4'
    if 'loggedin' in session:
        if request.method == 'POST' and 'noteupdate' in request.form and 'notetittleupdate' in request.form:
            notetittle = request.form['notetittleupdate']
            noteupdate = request.form['noteupdate']
            username = session['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM notes WHERE username = %s', (username, ))
            cursor.execute('UPDATE notetittle SET note4tittle = %s WHERE username = %s', (notetittle, username))
            cursor.execute('UPDATE notes SET note4 = %s WHERE username = %s', (noteupdate, username))
            mysql.connection.commit()
            return redirect('/home')
        return render_template('update4.html', notenum=notenum)
    return redirect('/')

@app.route('/update5', methods = ['GET', 'POST'])
def updatenote5():
    notenum = '5'
    if 'loggedin' in session:
        if request.method == 'POST' and 'noteupdate' in request.form and 'notetittleupdate' in request.form:
            notetittle = request.form['notetittleupdate']
            noteupdate = request.form['noteupdate']
            username = session['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM notes WHERE username = %s', (username, ))
            cursor.execute('UPDATE notetittle SET note5tittle = %s WHERE username = %s', (notetittle, username))
            cursor.execute('UPDATE notes SET note5 = %s WHERE username = %s', (noteupdate, username))
            mysql.connection.commit()
            return redirect('/home')
        return render_template('update5.html', notenum=notenum)
    return redirect('/')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = %s', (session['username'], ))
        account = cursor.fetchone()
        pfp = avatar(account['email_id'])
        return render_template('profile.html', account=account, pfp=pfp)
    return redirect('/home')

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if 'loggedin' in session:
        msg = ''
        color = ''
        if request.method == 'POST' and 'email_up' in request.form and 'cn_pass' in request.form:
            email_id = request.form['email_up']
            cnfrmpassword = request.form['cn_pass']
            username = session['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM account WHERE username = %s', (username, ))
            account = cursor.fetchone()
            if cnfrmpassword == account['password']:
                cursor.execute('UPDATE account SET email_id = %s WHERE username = %s', (email_id, username, ))
                msg = 'Email-id Updated'
                color = 'green-text'
                mysql.connection.commit()
                return render_template('settings.html', msg=msg, color=color)
            else:
                msg = 'Incorrect Password Entered'
                color = 'red-text'
                return render_template('settings.html', msg=msg, color=color)
        elif request.method == 'POST' and 'c_pass' in request.form and 'pass_up' in request.form and 'n_pass' in request.form:
            username = session['username']            
            new_password = request.form['n_pass']
            old_password = request.form['c_pass']
            password = request.form['pass_up']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM account WHERE username = %s', (username, ))
            account = cursor.fetchone()
            if old_password == account['password']:
                if password == new_password:
                    cursor.execute('UPDATE account SET password = %s WHERE username = %s', (password, username, ))
                    mysql.connection.commit()
                    msg = 'Password Updated'
                    color = 'green-text'
                    return render_template('settings.html', color2=color, msg2=msg)
                else:
                    msg = 'Your new password and conformation password dose not match retry again'
                    color = 'red-text'
                    return render_template('setting.html', msg2=msg, color2=color)
            else:
                msg = 'Your old password dose not match retry again'
                color = 'red-text'
                return render_template('settings.html', msg2=msg, color2=color)
        return render_template('settings.html')
    return redirect('/')

if __name__ == '__main__':
	app.run(threaded=True, port=5000, debug=True)