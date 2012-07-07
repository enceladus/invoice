import web
from app import helpers
import app.db as db

render = helpers.render()

class list:
	def GET(self):
		items = db.get_all('client')
		title = 'All Clients'
		type = 'client'
		return render.list(items, title, type)
		
class new:

	form = web.form.Form(
		web.form.Textbox('name', web.form.notnull, size=60, description='Name:'),
		web.form.Textbox('address', web.form.notnull, size=60, description='Address:'),
		web.form.Textbox('city', web.form.notnull, size=60, description='City:'),
		web.form.Textbox('state', web.form.notnull, size=60, description='State:'),
		web.form.Textbox('zip_code', web.form.notnull, size=60, description='Zip:'),
		web.form.Textbox('phone', web.form.notnull, size=60, description='Phone:'),
		web.form.Textbox('email', web.form.notnull, size=60, description='Email:'),
		web.form.Textbox('contact', web.form.notnull, size=60, description='Contact name:'),
		web.form.Button('Submit Client')
	)

	def GET(self):
		form = self.form()
		type = 'client'
		title = 'New Client'
		return render.new(form, title, type)
		
	def POST(self):
		form = self.form()
		if not form.validates():
			type = 'client'
			title = 'New Client'
			return render.new(form, title, type)
		db.new('client', 
			name=form.d.name, 
			address=form.d.address, 
			city=form.d.city, 
			state=form.d.state, 
			zip_code=form.d.zip_code, 
			phone=form.d.phone, 
			email=form.d.email, 
			contact=form.d.contact
		)
		raise web.seeother('/clients')
		
class edit:

	title = 'Edit Client'
	type = 'client'

	def GET(self, id):
		client = db.get_from_table('client', int(id))[0]
		form = new.form()
		form.fill(client)
		return render.edit(form, client, self.title, self.type, [])
		
	def POST(self, id):
		client = db.get_from_table('client', int(id))[0]
		form = new.form()
		if not form.validates():
			form.fill(client)
			return render.edit(form, client, self.title, self.type, [])
		db.update('client', id,
			name=form.d.name, 
			address=form.d.address, 
			city=form.d.city, 
			state=form.d.state, 
			zip_code=form.d.zip_code, 
			phone=form.d.phone, 
			email=form.d.email, 
			contact=form.d.contact
		)
		raise web.seeother('/clients')
		
class delete:
	def GET(self, id):
		db.delete('client', int(id))
		raise web.seeother('/clients')