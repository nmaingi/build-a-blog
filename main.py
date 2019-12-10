from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://build-a-blog:Lingima@1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)

class Blogs(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    text=db.Column(db.String(255))

    def __init__(self, title, text):
        self.title=title
        self.text=text

app.route("/")
def home():
    return render_template('/home')

app.route("/entry", methods=['POST', 'GET'])
def add():
    new_title=request.form['title']
    new_post=request.form['blog-post']
    title_error=""
    blog_error=""
    blank=""

    if title_error==blank:
        title_error="Please give a title to your blog"
    
    if blog_error==blank:
        blog_error="Please write a post"

    if title_error and blog_error:
        return render_template('entry.html', title_error=title_error, blog_error=blog_error )

    else:
        new_entry=Blogs(new_title,new_post)
        db.session.add(new_entry)
        db.session.commit()
        redirect('/home?id={0}'.format(new_entry))

app.route("/home")
def main_page():
    entry_id= request.args.get('id')

    if entry_id<0:
        posts=Blogs.query.all()
        return render_template("home.html", blogs=blogs, title='My Blog')

    else:
        entry = Blogs.query.get(entry_id)
        return render_template("each_blog.html", entry=entry, title="Entry Title")


if __name__=='__main__':
    app.run()