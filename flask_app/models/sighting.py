from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash
from flask_app.models import user

class Sighting:
    db_name = 'sasquatch_web_db'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.Location = db_data['Location']
        self.Comments = db_data['Comments']
        self.sighting_date = db_data['sighting_date']
        self.sasquatch_number = db_data['sasquatch_number']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None

    @classmethod
    def get_all_sightings_with_users(cls):
        query = "SELECT * FROM sightings LEFT JOIN users on sightings.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        sighting_list = []
        for row in results:
            sighting_list.append(cls(row))
        return sighting_list

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (Location, Comments, sighting_date, sasquatch_number, user_id) VALUES (%(Location)s,%(Comments)s,%(sighting_date)s,%(sasquatch_number)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET Location=%(Location)s, Comments=%(Comments)s, sighting_date=%(sighting_date)s, sasquatch_number=%(sasquatch_number)s,user_id =%(user_id)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sightings LEFT JOIN users on sightings.user_id = users.id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        one_sighting = cls( results[0])        
        one_user = {
            "id":results[0]['users.id'],
            "first_name":results[0]['first_name'],
            "last_name":results[0]['last_name'],
            "email":results[0]['email'],
            "password":results[0]['password'],
            "created_at":results[0]['users.created_at'],
            "updated_at":results[0]['users.updated_at']
        }
        user_instance = user.User(one_user)   
        print(user_instance)     
        one_sighting.creator = user_instance
        print(one_sighting.creator)
        print(one_sighting)
        return one_sighting

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_sightings(sightings):
        is_valid = True
        if len(sightings['Location']) < 1:
            is_valid = False
            flash("Location must be at least 1 characters","add")
        if len(sightings['Comments']) < 10:
            is_valid = False
            flash("Comments must be at least 3 characters","add")
        if int(sightings['sasquatch_number']) < 1:
            is_valid = False
            flash("# of Sasquatches must be at least 1 character","add")
        if sightings['sighting_date'] == "":
            is_valid = False
            flash("Please enter a date","add")
        return is_valid
