from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.app_context().push()
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect("/users")

@app.route("/users")
def list_users():

    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_form():
    return render_template('newform.html')

@app.route("/users/new", methods=["POST"])
def form_submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    newbie = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(newbie)
    db.session.commit()

    return redirect("/")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def save_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def post_form(user_id):
     user = User.query.get_or_404(user_id)
     return render_template('posts/new.html', user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_content(user_id):
    user = User.query.get_or_404(user_id)
    new = Post(title=request.form['title'],
               content=request.form['content'],
               user=user)
    db.session.add(new)
    db.session.commit()
    flash(f"Post '{new.title}' added. ")
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def posts_show(post_id):
    post= Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete(post_id):
   

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")