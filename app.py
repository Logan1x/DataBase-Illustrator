from flask import Flask, request, render_template, redirect
import csv
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courseregistration.db'
db = SQLAlchemy(app)

database={'khushal': '1234' , 'khush' :'1234' , 'Khushal' : '1234' }

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.course}')"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth",methods=['POST','GET'])
def auth():
    return render_template("auth.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    users = User.query.all()
    if name1 not in database:
	    return render_template('auth.html',info='Invalid Username')
    else:
        if database[name1]!=pwd:
            return render_template('auth.html',info='Invalid Username or Password')
        else:
	        return render_template("registered.html", users=users)

    
@app.route("/registered")
def registered():
    if not request.form.get("username") or not request.form.get("password"):
        return render_template("auth.html")
    else:
        users = User.query.all()
        return render_template('registered.html', users=users)
     
@app.route("/register" , methods = ["POST"])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        email =request.form.get("email")
        course = request.form.get("course")
        
        user = User(name=name,email= email, course = course)
        db.session.add(user)
        db.session.commit()
        return redirect("/registered")
    # if not request.form.get("name") or not request.form.get("email"):
    #     return "failure"

    # with open("registered.csv", "a") as file :
    #     writer = csv.writer(file)
    #     writer.writerow((request.form.get("name"), request.form.get("email")))
    # return redirect("/registered")

if __name__ == "__main__":
    app.run(debug=True)