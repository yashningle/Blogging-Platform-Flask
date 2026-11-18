
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Post, Category, Comment
from app.forms import PostForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint("main", __name__)


# Home Page with Pagination, Search and Category Filter
@main.route("/")
def home():

    search = request.args.get("search", "").strip()
    category_id = request.args.get("category", type=int)
    page = request.args.get("page", 1, type=int)

    query = Post.query

    # Search by Post Title
    if search:
        query = query.filter(
            Post.title.ilike(f"%{search}%")
        )

    # Filter by Category
    if category_id:
        query = query.filter(
            Post.category_id == category_id
        )

    posts = query.order_by(
        Post.id.desc()
    ).paginate(
        page=page,
        per_page=5
    )

    categories = Category.query.order_by(
        Category.name
    ).all()

    return render_template(
        "home.html",
        posts=posts,
        categories=categories,
        search=search,
        selected_category=category_id
    )


# Register Page
@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("Username or Email already exists!")
            return redirect(url_for("main.register"))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful!")

        return redirect(url_for("main.login"))

    return render_template("register.html")


# Login Page
@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash("Login successful!")

            return redirect(url_for("main.home"))

        flash("Invalid username or password!")

    return render_template("login.html")


# Logout Page
@main.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out!")

    return redirect(url_for("main.login"))


# Create Blog Post
@main.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():

    if Category.query.count() == 0:

        default_categories = [
            "Technology",
            "Python",
            "Flask",
            "AI / ML",
            "Electronics"
        ]

        for name in default_categories:
            db.session.add(Category(name=name))

        db.session.commit()

    categories = Category.query.order_by(Category.name).all()

    form = PostForm()

    form.category_id.choices = [
        (category.id, category.name)
        for category in categories
    ]

    if form.validate_on_submit():

        category = db.session.get(
            Category,
            form.category_id.data
        )

        post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            category=category
        )

        db.session.add(post)
        db.session.commit()

        flash("Blog post created successfully!")

        return redirect(url_for("main.home"))

    return render_template(
        "create_post.html",
        form=form,
        categories=categories
    )


# Edit Blog Post
@main.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:

        flash("You are not allowed to edit this post!")

        return redirect(url_for("main.home"))

    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":

        post.title = request.form["title"]
        post.content = request.form["content"]

        category_id = request.form.get("category_id")

        post.category = (
            db.session.get(Category, int(category_id))
            if category_id else None
        )

        db.session.commit()

        flash("Blog post updated successfully!")

        return redirect(url_for("main.home"))

    return render_template(
        "edit_post.html",
        post=post,
        categories=categories
    )


# Delete Blog Post
@main.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:

        flash("You are not allowed to delete this post!")

        return redirect(url_for("main.home"))

    db.session.delete(post)
    db.session.commit()

    flash("Blog post deleted successfully!")

    return redirect(url_for("main.home"))


# Add Comment
@main.route("/add_comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):

    post = Post.query.get_or_404(post_id)

    content = request.form.get("content", "").strip()

    if not content:
        flash("Comment cannot be empty!")
        return redirect(url_for("main.home"))

    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post.id
    )

    db.session.add(comment)
    db.session.commit()

    flash("Comment added successfully!")

    return redirect(url_for("main.home"))


# Delete Comment
@main.route("/delete_comment/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):

    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != current_user.id:

        flash("You are not allowed to delete this comment!")

        return redirect(url_for("main.home"))

    db.session.delete(comment)
    db.session.commit()

    flash("Comment deleted successfully!")

    return redirect(url_for("main.home"))
