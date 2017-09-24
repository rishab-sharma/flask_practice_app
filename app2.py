from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request , redirect , url_for , render_template
from flask.ext.security import Security , SQLAlchemyUserDatastore , UserMixin , RoleMixin , login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bond@localhost/flask_db'
app.debug=True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,   primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self,username,email):
        self.username = username
        self.email = email
    def __repr__(self):
        return '<User %r>' %self.username

@app.route('/')
def index():
    myuser = User.query.all()
    oneItem = User.query.filter_by(username="test1").first()
    return render_template('add_user2.html' , myuser = myuser , oneItem = oneItem)

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html' , user = user)


@app.route('/post_user',methods=['POST'])
def post_user():
    user = User(request.form['username'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
