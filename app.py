from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import desc
from werkzeug.exceptions import HTTPException
import flask_admin.contrib.sqla

app = Flask(__name__)


#app config.. move to exeernatl config

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://courseadmin:monkey1019@coursestash.coebdsda39o3.us-west-2.rds.amazonaws.com:3306/coursestash'
app.config['SECRET_KEY'] = "mysecret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ADMIN_CREDENTIALS'] = ('admin', 'pa$$word')
#database setup

db = SQLAlchemy(app)

class Courses(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50))
   description = db.Column(db.String(1000))
   sub = db.Column(db.String(100))
   link = db.Column(db.String(100))
   price = db.Column(db.String(10))
   image = db.Column(db.String(100))
   featured = db.Column(db.String(3))
   category = db.Column(db.String(20))
   logo =db.Column(db.String(1000))


class Category(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name= db.Column(db.String(20))
   description = db.Column(db.String(400))
   image= db.Column(db.String(400))
   slug = db.Column(db.String(50))




def __init__(self, name, description, link,image,featured,category):
   self.name = name
   self.descritopn = description
   self.link = link
   self.image = image
   self.featured = featured
   self.category = category


#flask Admin Login


class ModelView(flask_admin.contrib.sqla.ModelView):
    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response(
                "Please log in.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True




# FLASK ADMIN
admin = Admin(app, name='coursestash', template_mode='bootstrap3')
admin.add_view(ModelView(Courses, db.session))
admin.add_view(ModelView(Category,db.session))



# Routing

# Views
@app.route('/')
def show_all():
    return render_template('index.html', categories = Category.query.all())

@app.route('/listing/<cat>')
def show_list(cat):
    return render_template('course.html' , courses = Courses.query.filter_by(category = cat).order_by("featured desc"), Heading = cat,categories = Category.query.filter_by(name = cat))


@app.route('/home')
def home():
   return render_template('home.html')


@app.route('/test')
def test():
    return render_template('test1.html')


if __name__ == '__main__':
    app.run(debug=True)

