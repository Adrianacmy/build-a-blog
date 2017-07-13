from flask import Flask, request, redirect, render_template, session, flash, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = '123'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pub_data = db.Column(db.DateTime)

    def __init__(self, title, body, pub_data=None):
        self.title = title
        self.body = body
        if pub_data is None:
            pub_data = datetime.utcnow()
        self.pub_data = pub_data


@app.route('/')
def index():
    count = int(request.cookies.get('visit_count', 0))
    count += 1

    # resp = make_response(message)
    # resp.set_cookie('visit-count', str(count))
    # return resp

    resp = make_response(redirect('/blog'))
    resp.headers['visit_count'] = str(count)
    return resp


@app.route('/blog', methods=['GET'])
def display_blog():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route("/newpost", methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        pub_date = request.form['pub_date']

        if title and body:
            newpost = Post(title, body)
            db.session.add(newpost)
            db.session.commit()
            return redirect('/single_post?id='+str(newpost.id))
        else:
            flash("Title and body can not be empty.", "warning")
            return render_template("newpost.html", title=title, body=body, pub_date=pub_date)

    else:
        return render_template("newpost.html")


@app.route('/single_post', methods=['GET'])
def single_post():
    id = request.args.get('id')
    single_post = Post.query.filter_by(id=id).first()

    return render_template('single_post.html', post=single_post)


if __name__ == "__main__":
    app.run()