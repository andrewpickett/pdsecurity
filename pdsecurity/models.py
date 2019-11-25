class ApplicationUser:
	"""Class representing a user of the application.

	Attributes:
		id: The id of the user
		name: The name of the user
		password: The password of the user
		email: The email of the user
	"""

	def __init__(self, user_id=None, name=None, password=None, email=None):
		self.id = user_id if user_id else None
		self.name = name
		self.password = password
		self.email = email

	def __str__(self):
		return "ApplicationUser(id=%s, name=%s)" % (self.id, self.name)
