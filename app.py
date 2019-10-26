from flask import Flask, render_template, redirect, url_for,request, session, g
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='/static')
mongo = PyMongo(app,uri="mongodb://127.0.0.1:27017/User")


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':n
        session.pop('user',None)

        if request.form['password'] =='password':
            session['user'] = request.form['username']
            return redirect(url_for('protected'))
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':
            error ="Please enter all the credentials!"
            return render_template('main.html', error=error)

        
                
                    return redirect('proctected.html')
        else:
            mongo.db.user_collection.insert_one({
                "Username": username,
                "Password": password
            })
            return redirect(url_for('login'))

    return render_template('main.html')


@app.route('/result', methods=['POST','GET'])
def result():
    output = []
    users = mongo.db.user_collection.find()
    for user in users:
        output.append({
            "Username": user['Username'],
            "Password": user['Password']
        })
    print(output)
    return render_template("result.html", output= output)
    
@app.route('/login', methods=['POST','GET'])
def login():
    pwd = ""
    users = mongo.db.user_collection.find()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':
            error ="Please enter all the credentials!"
            return render_template('login.html', error=error)
        else:
            for user in users:
                if user['Username'] == username:
                    pwd = user['Password']
            if pwd == '':
                error ="User not found!"
                return render_template('login.html', error=error)
            elif pwd == password:
                return redirect(url_for('result'))
            else:
                error ="Incorrect Password!!"
                return render_template('login.html', error=error)  
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)