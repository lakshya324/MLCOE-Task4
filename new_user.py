#This file is used to add new user to the database

from system import app, db, admin

user_name ='lakshya'
user_email='lakshya@akgec.ac.in'
pass_word = '1234'
new_user = admin(username=user_name, email=user_email, password=pass_word)

with app.app_context():
    try:
        db.session.add(new_user)
        db.session.commit()
        print('New User Registered Successfully!')
    except:
        print('Error Occured while adding new user to database!')
        db.session.rollback()