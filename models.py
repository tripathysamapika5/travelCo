from configs import db

class Users(db.Model):
    __tablename__ = 'Users'

    email = db.Column(db.String,primary_key=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    phone = db.Column(db.Integer)

    def __init__(self, email, password, name, phone) :
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone


class Posts(db.Model):
    __tablename__ = 'Posts'

    postId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    activities = db.Column(db.String)
    tripStartDate = db.Column(db.String)
    tripEndDate = db.Column(db.String)
    fromLocation = db.Column(db.String)
    destinationLocation = db.Column(db.String)
    primaryEmail = db.Column(db.String)
    memberEmails = db.Column(db.String)
    attachments = db.Column(db.String)

    def __init__(self, name, activities, tripStartDate, tripEndDate, fromLocation, destinationLocation, primaryEmail) :
        self.name = name
        self.activities = activities
        self.tripStartDate = tripStartDate
        self.tripEndDate = tripEndDate
        self.fromLocation = fromLocation
        self.destinationLocation = destinationLocation
        self.primaryEmail = primaryEmail
        self.memberEmails ="[]"
        self.attachments = "{}"

class modelService:

    @classmethod
    def createDatabase(cls):
        from models import Users;
        from models import Posts;
        db.create_all()

    @classmethod
    def getDb(cls):
        return db

    @classmethod
    def initialiseUsers(cls):
        try:
            db.session.add( Users("satripathy@expediagroup.com", "password", "samapika tripathy", 8895449796 ) )
            db.session.commit()
        except Exception:
            db.session.rollback()


        try:
            db.session.add(Users("ramalik@expediagroup.com", "password", "Ratika Malik", 9898877777) )
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            db.session.add( Users("amtanwar@expediagroup.com", "password", "Aman Tanwar", 9898877777 ))
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            db.session.add( Users("meagarwal@expediagroup.com", "password", "Megha", 9898877777 ))
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            db.session.add( Users("asmakhan@expediagroup.com", "password", "Asma", 9898877777 ))
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            db.session.add( Users("shubhkumar@expediagroup.com", "password", "Shubham", 9898877777 ))
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            db.session.add( Users("usaraswat@expediagroup.com", "password", "Ujjwal", 9898877777 ))
            db.session.commit()
        except Exception:
            db.session.rollback()

    @classmethod
    def initialisePosts(cls):
        try:
            db.session.query(Posts).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()


        try:
            db.session.add(
                Posts("Trip to Hyderabad",
                      '["shopping", "food, drink & nightlife", "gallery and museum", "sightseeing & city tours","history & culture", "theme park and water activities"]'
                      ,"2022-10-01"
                      ,"2022-10-05"
                      ,"Delhi"
                      ,"Hyderabad"
                      ,"satripathy@expediagroup.com"
                      )
            )
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            db.session.add(
                Posts("Weekend trip to Mysuru",
                      '["shopping", "food, drink & nightlife", "gallery and museum", "sightseeing & city tours","history & culture", "theme park and water activities"]'
                      ,"2022-10-03"
                      ,"2022-10-10"
                      ,"Bangalore"
                      ,"Mysuru"
                      ,"shubhkumar@expediagroup.com"
                      )
            )
            db.session.commit()
        except Exception:
            db.session.rollback()

        try:
            db.session.add(
                Posts("Weekend trip to ooty",
                      '["food, drink & nightlife", "sightseeing & city tours", "wildlife & nature", "cruises or boat rides", "adventure"]'
                      ,"2022-10-03"
                      ,"2022-10-10"
                      ,"Bangalore"
                      ,"ooty"
                      ,"asmakhan@expediagroup.com"
                      )
            )
            db.session.commit()
        except Exception:
            db.session.rollback()
