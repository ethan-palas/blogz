from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(220))

    def __init__(self,title,body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()
    return render_template('main-page.html',title="Build a Blog!",blogs=blogs)

@app.route('/newpost', methods=['POST','GET'])
def blog_post():

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
            newpost = Blog(blog_title,blog_body)
            db.session.add(newpost)
            db.session.commit()
            url = './blog-post?id=' + str(newpost.id)
            return redirect(url)
        else:
            return render_template('newpost.html',title_error=title_error, body_error=body_error)
    
    return render_template('newpost.html')

@app.route('/blog-post', methods=['POST','GET'])
def blogpost():
    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('blog-post.html',blog=blog)


    
if __name__ == '__main__':
    app.run()