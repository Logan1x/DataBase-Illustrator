from flask import Flask, request, render_template, redirect
import csv
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courseregistration.db'
db = SQLAlchemy(app)

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

@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/registered")
def registered():
    users = User.query.all()
    return render_template('registered.html', users=users)
    # with open("registered.csv", "r") as file :
    #     reader = csv.reader(file)
    #     students = list(reader)
       
    # return render_template("registered.html", students = students)
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