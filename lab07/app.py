from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.debug = True
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
# SQLAlchemy instance for DB
db = SQLAlchemy(app)

#This is used to create the table in the sqliter database
class UserDataBase(db.Model):
    __tablename__ = "usertable"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    confirm_password = db.Column(db.String(20), unique=False, nullable=False)

@app.route('/')
def home():
    return render_template('loginpage.html')

@app.route('/redirectregisterscreen')
def redirectregisterscreen():
    return render_template('registerpage.html')

def checkEmailIsAvailable(email):
    emailCheck = UserDataBase.query.filter_by(email=email).first()
    if emailCheck!=None:
        return True
    else:
        return False

@app.route('/userregistration', methods=["POST","GET"])
def userregistration():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            return render_template('registerpage.html' , pwd_cpwd = True)
        
        if checkEmailIsAvailable(email):
            return render_template('registerpage.html' , email_check = True)

        if first_name != '' and last_name != '':
            if is_strong_password(confirm_password):
                p = UserDataBase(first_name=first_name, last_name=last_name,email=email,password=password,confirm_password=confirm_password)
                db.session.add(p)
                db.session.commit()
                return render_template('Thankyou.html')
            else:
                return render_template('registerpage.html' , password_check = True)
        else:
            return "Please enter the first name and last name"
        
    return render_template('registerpage.html')

@app.route('/userloginredirect')
def userloginredirect():
    return render_template('loginpage.html')

@app.route('/userlogin', methods=["POST"])
def userlogin():
    username = request.form.get("email")
    password = request.form.get("password")
 
    if username != '' and password != '':
        data = UserDataBase.query.filter_by(email=username, password=password).first()
        if data == None:
            return  "The Username and password entered doesnot exist in the database. Kindly register first and try again"

        if data.email == username and data.password == password:
            return render_template('SecretPage.html')
        else:
            return render_template('loginpage.html')
    else:
        return render_template('loginpage.html')
    
def is_strong_password(password):
    # Check if the password length is at least 8 characters
    if len(password) < 8:
        return False

    # Check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check if the password contains at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check if the password contains at least one digit (number)
    if not any(char.isdigit() for char in password):
        return False

    # Check if the password contains at least one special character
    special_chars = "!@#$%^&*()-_=+~`[]{}|\\:;'<>,.?/"
    if not any(char in special_chars for char in password):
        return False

    # All checks passed, the password is strong
    return True



if __name__ == '__main__':
    app.run()