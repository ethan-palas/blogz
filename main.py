from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:root@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'nugnios'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(220))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index','blogs']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')

@app.route('/signup', methods=['GET','POST'])
def signup():   
    if request.method == 'POST':

        username = request.form['user-name']
        password = request.form['pass-word']
        verify_pw = request.form['verify-pw']

        username_error = False
        password_error = False
        verify_pw_error = False

        if username == '' or (len(username) < 3) or (len(username) > 20) or " " in username:
            flash('Username creation error','error')
            username_error = True
        else:
            pass

        if password == '' or (len(password) < 3) or (len(password) > 20) or " " in password:
            flash('Password creation error', 'error')
            password_error = True
        else:
            pass

        if verify_pw == '' or (len(password) < 3) or (len(password) > 20) or " " in verify_pw:
            flash('Password verification error', 'error')
            verify_pw_error = True
        else:
            pass

        if verify_pw != password:
            flash('Passwords must match', 'error')
            verify_pw_error = True
        else:
            pass

        if password_error == False and username_error == False and verify_pw_error == False:
            user_username = request.form['user-name']
            user_password = request.form['pass-word']
            new_user = User(user_username, user_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')

    return render_template('signup.html')

@app.route('/', methods=['POST','GET'])
def index():
    users = User.query.all()
    return render_template('index.html',users=users)

@app.route('/blog', methods=['GET'])
def blogs():
    if request.args.get('user'):
        user = User.query.get(request.args.get('user'))
        return render_template('main-page.html', blogs=user.blogs)

    blogs = Blog.query.all()
    return render_template('main-page.html',blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def blog_post():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['name']
        blog_body = request.form['posted']
        title_error = ''
        body_error = ''
        if blog_title == '':
            title_error = 'Please add a title'
        if blog_body == '':
            body_error = 'Please add a body'
        if not title_error and not body_error:
            newpost = Blog(blog_title,blog_body,owner)
            db.session.add(newpost)
            db.session.commit()
            url = './blog-post?id=' + str(newpost.id)
            return redirect(url)
        else:
            return render_template('newpost.html',title_error=title_error, body_error=body_error)
    
    return render_template('newpost.html')

@app.route('/blog-post', methods=['POST','GET'])
def blogpost():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('blog-post.html',blog=blog)
    
if __name__ == '__main__':
    app.run()