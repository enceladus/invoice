import web
from app import helpers
import app.db as db

render = helpers.render()
render_print = helpers.render('')

class list:
	def GET(self):
		items = db.get_all('invoice')
		title = 'All Invoices'
		type = 'invoice'
		return render.list(items, title, type)
		
class new:

	clients = db.get_all('client')
	client_names = []
	for client in clients:
		client_names.append(client.name)
	
	form = web.form.Form(
		web.form.Textbox('title', web.form.notnull, size=60, description='Project title:'),
		web.form.Textbox('description', web.form.notnull, size=60, description='Project description:'),
		web.form.Dropdown('client', args=client_names, description='Client:'),
		web.form.Textbox('date', web.form.notnull, size=60, description='Date (YYYY-MM-DD):'),
		web.form.Button('Submit Invoice')
	)	

	def GET(self):
		form = self.form()
		title = 'New Invoice'
		type = 'invoice'
		return render.new(form, title, type)
		
	def POST(self):
		form = self.form()
		if not form.validates():
			title = 'New Invoice'
			type = 'invoice'
			return render.new(form, title, type)
		client = db.get_client_id(form.d.client)
		db.new('invoice', 
			project_title=form.d.title, 
			description=form.d.description, 
			client_id=client, 
			date=form.d.date
		)
		raise web.seeother('/invoices')
		
class edit:

	title = 'Edit Invoice'
	type = 'invoice'

	def GET(self, id):
		item = db.get_from_table('invoice', int(id))[0]
		client = db.get_from_table('client', item.client_id)[0]
		form = new.form()
		form.fill({
			'title': item.project_title,
			'description': item.description,
			'client': client.name,
			'date': item.date,
		})
		
		invoice_items = []
		if (db.get_invoice_items(id)[0]):
			invoice_items = db.get_invoice_items(id)
		return render.edit(form, item, self.title, self.type, invoice_items)
		
	def POST(self, id):
		form = new.form()
		invoice = db.get_from_table('invoice', int(id))
		if not form.validates():
			return render.edit(invoice, form)
		client = db.get_client_id(form.d.client)
		db.update('invoice', id,
			project_title=form.d.title,
			description=form.d.description,
			client_id=client,
			date=form.d.date
		)
		raise web.seeother('/invoices')
		
class delete:
	def GET(self, id):
		db.delete('invoice', int(id))
		raise web.seeother('/invoices')
		
class print_view:
	def GET(self, id):
		invoice = db.get_from_table('invoice', int(id))[0]
		client = db.get_from_table('client', invoice.client_id)[0]
		items = db.get_invoice_items(int(id))
		return render_print.print_view(invoice, client, items)
		
class add:
	form = web.form.Form(
			web.form.Textbox('description', web.form.notnull, size=60, description='Description:'),
			web.form.Textbox('rate', web.form.notnull, size=60, description='Rate:'),
			web.form.Textbox('hrs', web.form.notnull, size=60, description='Time:'),
			web.form.Textbox('date', web.form.notnull, size=60, description='Date:'),
			web.form.Button('Add Item')
		)
	
	empty = {
		'description': '',
		'rate': '',
		'hrs': '',
		'date': '',
		'project_id': ''
	}

	def GET(self, id):
		invoice = db.get_from_table('invoice', int(id))[0]
		form = self.form
		form.fill(self.empty)
		return render.add(invoice, form)
		
	def POST(self, id):
		invoice = db.get_from_table('invoice', int(id))[0]
		form = self.form
		if not form.validates():
			form.fill(self.empty)
			return render.add(invoice, form)
		
		db.new('item',
			description=form.d.description,
			rate=float(form.d.rate),
			hrs=float(form.d.hrs),
			date=form.d.date,
			invoice_id=id
		)
		raise web.seeother('/invoices/' + str(id) + '/add')