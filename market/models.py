from market import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_db = db.Column(db.String(40), nullable=False, unique=True)
	price_db = db.Column(db.Integer(), nullable=False)
	barcode_db = db.Column(db.String(), nullable=False, unique=True)
	description_db = db.Column(db.String(1024), nullable=False)
	owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
	
	def buy(self, user):
		self.owner = user.id
		user.budget -= self.price_db
		db.session.commit()

class user(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username_db = db.Column(db.String(length=30), nullable=False, unique=True)
	email_db= db.Column(db.String(length=50), nullable=False, unique=True)
	password_hash_db= db.Column(db.String(length=60), nullable=False)
	budget= db.Column(db.Integer, nullable=False, default=1000)
	items = db.relationship('item', backref='owned_user', lazy=True)
	
	@property
	def nice_budget(self):
		if len(str(self.budget)) >= 4:
			return f'${str(self.budget)[:-3]}, {str(self.budget)[-3:]}'
		else:
			return f'${self.budget}'
	
	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute')
	
	@password.setter
	def password(self, password):
		self.password_hash_db = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash_db, password)
		
	def can_purchase(self, item_obj):
		return self.budget >= item_obj.price_db
	
	