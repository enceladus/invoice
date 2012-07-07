import web
from app import helpers
import app.db as db

render = helpers.render()

class list:
	def GET(self, id):
		items = db.get_invoice_items(int(id))
		type = 'item'
		title = 'All Invoice Items (you probably shouldn\'t be looking at this)'
		return render.list(items)
		
class new:

	form = web.form.Form(
		web.form.Textbox('description', web.form.notnull, size=60, description='Description:'),
		web.form.Textbox('rate', web.form.notnull, size=60, description='Rate:'),
		web.form.Textbox('hrs', web.form.notnull, size=60, description='Time:'),
		web.form.Textbox('date', web.form.notnull, size=60, description='Date:'),
		web.form.Button('Submit Item')
	)

	def GET(self, id):
		form = self.form()
		invoice = get_from_table('invoice', int(id))
		return render.new(invoice, form)
		
	def POST(self, id):
		form = self.form()
		invoice = get_from_table('invoice', int(id))
		if not form.validates():
			return render.new(invoice, form)
		db.new('item', 
			description=form.d.description, 
			rate=form.d.rate, 
			hrs=form.d.hrs, 
			date=form.d.date, 
			invoice_id=int(id)
		)
		raise web.seeother('/invoices/' + id)
		
class edit:

	title = 'Edit Invoice Item'
	type = 'item'

	def GET(self, id):
		item = db.get_from_table('item', int(id))[0]
		form = new.form()
		form.fill(item)
		return render.edit(form, item, self.title, self.type, [])
		
	def POST(self, id):
		item = db.get_from_table('item', int(id))[0]
		form = new.form()
		if not form.validates():
			form.fill(item)
			return render.edit(form, item, self.title, self.type, [])
		db.update('item', id,
			description=form.d.description, 
			rate=form.d.rate, 
			hrs=form.d.hrs, 
			date=form.d.date
		)
		raise web.seeother('/invoices/' + str(item.invoice_id))
		
class delete:
	def GET(self, id):
		db.delete('item', int(id))
		raise web.seeother('/invoices/' + id)