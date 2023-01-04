from market import app
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask import render_template, flash, url_for, redirect, request
from market.models import item, user
from market.webforms import reg, loginform, PurchaseForm, SellForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view="login"
@login_manager.user_loader
def load_user(user_id):
	return user.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def home():
	return render_template('base.html')
	
@app.route('/market', methods=["POST", "GET"])
@login_required
def market():
	purchase_form = PurchaseForm()
	
	if request.method == "POST":
		purchased_item = request.form.get('purchased_item')
		p_item_object = item.query.filter_by(name_db = purchased_item).first()
		
		if p_item_object:
			if current_user.can_purchase(p_item_object):
				p_item_object.buy(current_user)
				flash(f'You have successfully bought { p_item_object.name_db } for ${ p_item_object.price_db }')
			else:
				flash("Unfortunately, you don't have enough to purchase this item")
				
		return redirect(url_for('market'))
		
	if request.method == "GET":
		all_item = item.query.filter_by(owner = None)
		return render_template('market.html', purchase_form=purchase_form, all_item=all_item)
		
	return render_template('market.html', purchase_form=purchase_form)
	
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update_item(id):
	update = item.query.get_or_404(id)
	form = add()
	if form.validate_on_submit():
		update.name_db = form.name.data
		update.barcode_db=form.barcode.data
		update.description_db=form.description.data
		update.price_db=form.price.data
		db.session.add(update)
		db.session.commit()
	return render_template("update_item.html", form=form)
	
@app.route("/delete/<int:id>")
def delete_item(id):
	remove = item.query.get_or_404(id)
	db.session.delete(remove)
	db.session.commit()
	flash("Item Deleted")
	return redirect(url_for('market'))

@app.route("/register", methods=["POST", "GET"])
def register():
	form = reg()
	if form.validate_on_submit():
		one_user = user.query.filter_by(username_db=form.username.data).first()
		if one_user is None:
			hashed_password = generate_password_hash(form.password.data, "sha256")
			one_user = user(username_db=form.username.data, email_db = form.email.data, password_hash_db = hashed_password)
			db.session.add(one_user)
			db.session.commit()
			login_user(one_user)
			flash(f"Account created, you're logged in as {one_user.username_db}.", category="success")
		
		form.username.data=" "
		form.email.data=" "
		form.password.data=" "
		form.password2.data=" "
		
	users =user.query.order_by(user.id)
	return render_template('register.html', form=form, users=users)

@app.route("/login", methods=["POST", "GET"])
def login():
	form = loginform()
	if form.validate_on_submit():
		one_user = user.query.filter_by(username_db=form.username.data).first()
		if one_user:
			if check_password_hash(one_user.password_hash_db, form.password.data):
				login_user(one_user)
				flash(f"you're logged in as {one_user.username_db}. ")
				return redirect(url_for('market'))
			else:
				flash("Wrong password, try again", category="warning")
		else:
			flash("User does not exist, sign up below", category="warning")
			return redirect(url_for('register'))
	return render_template("login.html", form=form)
	
@app.route('/logout')
def logout():
	logout_user()
	flash("You have been logged out")
	return redirect(url_for('login'))

@app.route('/modal')
def mode():
	return render_template("modal.html")