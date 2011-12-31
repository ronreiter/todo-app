#!/usr/bin/env python
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
import simplejson

class Todos(db.Model):
	content = db.StringProperty()
	done = db.BooleanProperty()
	order = db.IntegerProperty()

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render("index.html", {}))

class TodosHandler(webapp.RequestHandler):
	def get(self):
		todos = []
		for todo in Todos.all():
			todos.append({
				"id" : todo.key().id(),
				"content" : todo.content,
				"done" : todo.done,
				"order" : todo.order,
			})
		self.response.out.write(simplejson.dumps(todos))

	def post(self):
		data = simplejson.loads(self.request.body)

		todo = Todos(
			content = data["content"],
			done = data["done"],
			order = data["order"],
		).put()

		self.response.out.write(simplejson.dumps({
			"id" : todo.id(),
			"content" : data["content"],
			"done" : data["done"],
			"order" : data["order"],
		}))
		
class TodoHandler(webapp.RequestHandler):
	def put(self, id):
		data = simplejson.loads(self.request.body)

		todo = Todos.get_by_id(int(id))
		todo.content = data["content"]
		todo.done = data["done"]
		todo.order = data["order"]
		todo.put()

		self.response.out.write(simplejson.dumps({
			"id" : id,
			"content" : todo.content,
			"done" : todo.done,
			"order" : todo.order,
		}))

	def delete(self, id):
		todo = Todos.get_by_id(int(id))
		todo.delete()

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/todos', TodosHandler),
		('/todos/(\d+)', TodoHandler),
	], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
