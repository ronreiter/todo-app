#!/usr/bin/env python
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
import simplejson

# the Todo model.
class Todo(db.Model):
	content = db.StringProperty()
	done = db.BooleanProperty()
	order = db.IntegerProperty()

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render("index.html", {}))

# the Todos collection handler - used to handle requests
# on the Todos collection.
class TodosHandler(webapp.RequestHandler):
	# get all todos
	def get(self):
		# serialize all Todos, include the ID in the response
		todos = []
		for todo in Todo.all():
			todos.append({
				"id" : todo.key().id(),
				"content" : todo.content,
				"done" : todo.done,
				"order" : todo.order,
			})
		# send them to the client as JSON
		self.response.out.write(simplejson.dumps(todos))

	# create a todo
	def post(self):
		# load the JSON data of the new object
		data = simplejson.loads(self.request.body)

		# create the todo item
		todo = Todo(
			content = data["content"],
			done = data["done"],
			order = data["order"],
		).put()

		# send it back, and include the new ID.
		self.response.out.write(simplejson.dumps({
			"id" : todo.id(),
			"content" : data["content"],
			"done" : data["done"],
			"order" : data["order"],
		}))

# The Todo model handler - used to handle requests with
# a specific ID.
class TodoHandler(webapp.RequestHandler):
	def put(self, id):
		# load the updated model
		data = simplejson.loads(self.request.body)

		# get it model using the ID from the request path
		todo = Todo.get_by_id(int(id))

		# update all fields and save to the DB
		todo.content = data["content"]
		todo.done = data["done"]
		todo.order = data["order"]
		todo.put()

		# send it back using the updated values
		self.response.out.write(simplejson.dumps({
			"id" : id,
			"content" : todo.content,
			"done" : todo.done,
			"order" : todo.order,
		}))

	def delete(self, id):
		# find the requested model and delete it.
		todo = Todo.get_by_id(int(id))
		todo.delete()

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),

		# REST API requires two handlers - one with an ID and one without.
		('/todos', TodosHandler),
		('/todos/(\d+)', TodoHandler),
	], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
