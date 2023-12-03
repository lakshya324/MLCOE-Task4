#Run this file to create the database
from system import app,db

with app.app_context():
    db.create_all()
    print("Database created successfully")

#This file is not needed to run the application
#This file is only needed to create the database
#The database is already created and stored in data.db
#The database is created using SQLAlchemy