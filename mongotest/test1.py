import pymongo
import json
import random


class StoreObjectBase:
	def __init__(self, **args):
		for k, v in args.items():
			setattr(self, k, v)
	
	def __new__(self, input):
		for k, v in input.items():
			setattr(self, k, v)
		return self

	def save(self):
		return self.__dict__
	
	def load(self, input):
		obj = self.__new__(input)
		return obj

class StoreCollectionBase:
	def __init__(self, connection, db):
		self.connection = connection
		self.db = db
		self.collection = db[self.__class__.__name__]
		
	def save(self, storeObjectBase):
		if isinstance(storeObjectBase, StoreObjectBase):
			self.collection.save(storeObjectBase.save())
		else:
			self.collection.save(json.dumps(storeObjectBase))
			
	def find(self, storeObjectBase):
		for obj in self.collection.find(storeObjectBase.save()):
			yield storeObjectBase.load(obj)

class User(StoreObjectBase):
	pass

class Users(StoreCollectionBase):
	pass

class Task(StoreObjectBase):
	pass

class Tasks(StoreCollectionBase):
	pass

class Projects(StoreCollectionBase):
	pass

class Project(StoreObjectBase):
	pass
	

connection = pymongo.Connection('flame.mongohq.com', 27044)
# connection = pymongo.Connection('localhost', 27017)
db = connection['ughani-mongo']

userId = 'usman.ghani'
pwd = 'Mugga25.'

if not db.authenticate(userId, pwd):
	raise 'Authentication Failure'

myusers = Users(connection, db)
mytasks = Tasks(connection, db)
myprojects = Projects(connection, db)

myusers.save(User(name=random.choice(['really', 'blah', 'gotcha']), age=random.randint(30,100)))
mytasks.save(Task(title='my Task Title', priority=random.randint(1, 3)))
myprojects.save(Project(title='My Project Title', priority=random.randint(1,3), members='ughani;ppatwa;ritwikt'))
myprojects.save(Project(title='My Project Title', priority=random.randint(1,3), members='ughani;ppatwa;ritwikt', status='Blocked'))

for u in myusers.find(User(name='blah')):
	print u.name, u.age

print '----------------'

for u in myusers.find(User(name='really')):
		print u.name, u.age

print '----------------'		
for u in myusers.find(User(name='gotcha')):
			print u.name, u.age
			
print '--------------------------'
for t in mytasks.find(Task(priority=1)):
	print t.title, t.priority


for p in myprojects.find(Project(priority=1)):
	print p.title, p.members, p.priority, p.status
