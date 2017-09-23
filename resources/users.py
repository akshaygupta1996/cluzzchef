from flask_restful import Resource, reqparse
from flask import request, jsonify,make_response
from models.users import UsersModel
from flask_restful_swagger import swagger
from db import db

import requests
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

class Users(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('fname',
			type = str,
			required = True,
			help = "First Name is Required"
			)
	parser.add_argument('lname',
			type = str,
			required = True,
			help = "Last Name is Required")
	parser.add_argument('phone_number',
			type = str,
			required = True,
			help = "Phone Number Required")
	parser.add_argument('email',
			type = str,
			required = True,
			help = "Email Required")
	parser.add_argument('password',
		type = str,
		required = True,
		help = "Password Required")



	@swagger.operation(
		notes = "Get All Registered Users",
		nickname='GET')

	def get(self):

		return {'users': [user.json() for user in UsersModel.query.all()]}

	
	@swagger.operation(
		notes='Register a User',
		nickname='POST',
		parameters=[
			{
				"name": "fname",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "lname",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "email",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "phone_number",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "password",
				"required": True,
				"dataType": "String"
			}

		])
	def post(self):


		data = Users.parser.parse_args()

		if UsersModel.find_by_email(data['email']):
			return {'data':{'status': False,
							'message': "Email Already Regsitered"}}, 201

		if UsersModel.find_by_phone(data['phone_number']):
			return {'data':{'status': False,
							'message': "Phone Number Already Registered"}}, 201
			# return {'error': "Phone Number Already Registered"}, 400

		user = UsersModel(data['fname'], data['lname'], data['email'], data['phone_number'], data['password'])
		user.save_to_db()


		return {'data':{'status': True, 'message': "Registration Successful"}}, 201


		
		

class LoginUsers(Resource):

		@swagger.operation(
			notes='Login User',
			nickname='GET',
			parameters=[
			{
				"name": "phone_number",
				"required": True,
				"dataType": "String",
				"description": "Phone Number Required For Login"
			},
			{
				"name": "password",
				"required": True,
				"dataType": "String"
			}

		])

		def get(self, phone_number,password):

			user_phone = UsersModel.find_by_phone(phone_number)
			if user_phone:
				if user_phone.password == password:

					user_phone.save_to_db()
						# return user_phone.json()
					return {'status': True, 'user': user_phone.json()}
		
			return {'status': False}, 200


