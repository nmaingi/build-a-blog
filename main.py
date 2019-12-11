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

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/entry", methods=['POST','GET'])
def add():
    if request.method =='POST':
        new_title=request.form['title']
        new_post=request.form['blogpost']
        title_error=""
        blog_error=""
        blank=""

        if new_title==blank:
            title_error="Please give a title to your blog"
    
        if new_post==blank:
            blog_error="Please write a post"

        if title_error or blog_error:
            return render_template('entry.html', title_error=title_error, blog_error=blog_error )
        else:
            new_entry=Blogs(new_title,new_post)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/home?id={0}'.format(new_entry.id))

    return render_template('entry.html', blogs='', title='')

@app.route("/home")
def main_page():
    entry_id= request.args.get('id')

    if entry_id==None:
        blogs=Blogs.query.all()
        return render_template("home.html", blogs=blogs, title='My Blog')
    else:
        entry = Blogs.query.get(entry_id)
        return render_template("each_blog.html", entry=entry, title="Entry Title")


if __name__ == "__main__":
    app.run()