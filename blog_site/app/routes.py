from flask import render_template, flash, redirect, url_for, request
from . import app
from .forms import LoginForm, RegisterForm, PostForm, CommentForm, UserEditForm
from .models import User, Post, Comment
from . import db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    all_posts = Post.query.all()
    posts = []
    for post in all_posts:
        new_post = {
            "id": post.id,
            "title": post.title,
            "author": User.query.get(post.user_id),
            "date": post.date,
            "content": post.content,
        }
        posts.append(new_post)
    return render_template("home.html", posts=posts)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if User.query.filter_by(username=form.username.data).first():
            if User.query.filter_by(username=form.username.data).first().password == form.password.data:
                user = User.query.filter_by(username=form.username.data).first()
                if form.remember_me.data:
                    login_user(user, remember=True)
                else:
                    login_user(user, remember=False)
                flash("Successfully logged In", "alert alert-success")
                return redirect(url_for("home"))
            else:
                flash("Password doesn't match", "alert alert-warning")
        else:
            flash("Check your username and password", "alert alert-warning")
    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        if validate_user(user):
            db.session.add(user)
            db.session.commit()
            if form.remember_me.data:
                login_user(user, remember=True)
            else:
                login_user(user, remember=False)
            flash("Account created successfully", "alert alert-success")
            return redirect(url_for("home"))
        else:
            flash("Username or Email already exists", "alert alert-warning")
    return render_template("register.html", form=form)


def validate_user(user):
    if User.query.filter_by(username=user.username).first() is None and User.query.filter_by(email=user.email).first() is None:
        return True
    return False


@app.route("/account")
@login_required
def account():
    posts = Post.query.filter_by(user=current_user)
    return render_template("account.html", posts=posts)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/create_post", methods=["POST", "GET"])
@login_required
def create_post():
    form = PostForm(request.form)
    if request.method == "POST" and form.validate():
        user = current_user
        post = Post(
            content=form.content.data,
            user=user,
            title=form.title.data
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("account"))
    return render_template("create_post.html", form=form)


@app.route('/post/<int:post_id>', methods=["POST", "GET"])
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = CommentForm(request.form)
    comment_list = Comment.query.filter_by(post_id=post.id)
    params = {
        "post": post,
        "comment": form,
        "comments": comment_list
    }
    if request.method == "POST" and form.validate():
        if current_user.is_authenticated:
            comment = Comment(comment_content=form.content.data, author=current_user.username, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("You must log in first to post a comment", "alert alert-warning")
    return render_template("post.html", params=params)


@app.route('/post/<int:post_id>/edit', methods=["POST", "GET"])
@login_required
def edit(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = PostForm(request.form)
    if current_user.username == post.user.username:
        if request.method == "POST" and form.validate():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Your post is edited", "alert alert-success")
            return redirect(url_for("show_post", post_id=post_id))
    else:
        flash("You are not authorized to perform this action", "alert alert-warning")
    params = {
        "form": form,
        "post": post
    }
    return render_template("edit.html", params=params)


@app.route('/post/<int:post_id>/delete', methods=["POST", "GET"])
@login_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if current_user.username == post.user.username:
        Comment.query.filter_by(post_id=post_id).delete()
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        flash("Your post is deleted", "alert alert-success")
        return redirect(url_for("account"))
    else:
        flash("You are not authorized to perform this action", "alert alert-warning")
    return render_template("delete.html")


@app.route("/edit_profile", methods=["POST", "GET"])
@login_required
def edit_profile():
    form = UserEditForm(request.form)
    if request.method == "POST" and form.validate():
        user = current_user
        if form.previous_password.data == user.password:
            user.password = form.password.data
            if form.username.data == user.username:
                pass
            else:
                if User.query.filter_by(username=form.username.data):
                    flash("Username already taken", "alert alert-warning")
                else:
                    user.username = form.username.data
            if form.email.data == user.email:
                pass
            else:
                if User.query.filter_by(email=form.email.data):
                    flash("Email already used", "alert alert-warning")
                else:
                    user.email = form.email.data
            db.session.commit()
            return redirect(url_for("account"))
        else:
            flash("Incorrect password", "alert alert-warning")
    return render_template("edit_profile.html", form=form)
