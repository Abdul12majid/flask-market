from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from market.models import user
from flask import flash

class reg(FlaskForm):
	def validate_username(self, username_to_check):
		username = user.query.filter_by(username_db=username_to_check.data).first()
		if username:
			flash("Username exists")
			
	def validate_email(self, email_to_check):
		email = user.query.filter_by(email_db=email_to_check.data).first()
		if email:
			flash("Email exists")
			raise ValidationError("Email already exists, kindly pick another one")
			
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=30)])
	email = StringField("Email Address", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), EqualTo('password2')])
	password2 = PasswordField("Confirm Password", validators=[DataRequired()])
	submit = SubmitField("Create Account")
	
class loginform(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=30)])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")
	
class SellForm(FlaskForm):
	submit = SubmitField("Sell item")
	
class PurchaseForm(FlaskForm):
	submit = SubmitField("Purchase item")
	