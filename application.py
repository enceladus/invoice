import web
import app
import config
from app import helpers

render = helpers.render()

## url definitions
urls = (
	'/', 						'index',
	'/login',					'login',
	'/logout',					'logout',				
	'/settings',				'settings',
	
	'/clients', 				'app.client.list',
	'/clients/(\d+)/del', 		'app.client.delete',
	'/clients/new', 			'app.client.new',
	'/clients/(\d+)',			'app.client.edit',
	
	'/invoices',				'app.invoice.list',
	'/invoices/(\d+)', 			'app.invoice.edit',
	'/invoices/new',			'app.invoice.new',
	'/invoices/(\d+)/del', 		'app.invoice.delete',
	'/invoices/(\d+)/print', 	'app.invoice.print_view',
	'/invoices/(\d+)/add', 		'app.invoice.add',
	
	'/item/(\d+)',				'app.item.edit',
	'/item/(\d+)/del',			'app.item.delete',
)

## render front page
class index:
	def GET(self):
		return render.index()


## user auth classes: work on this later	
class login:
	def GET(self):
		return render.index()
		
	def POST(self):
		pass
		
class logout:
	def GET(self):
		return render.index()
		
class settings:
	form = web.form.Form(
		web.form.Textbox('name', description='Name:'),
		web.form.Textbox('email', description='Email:'),
		web.form.Textbox('phone', description='Phone:'),
		web.form.Textbox('logo_path', description='Logo file path:'),
		web.form.Textbox('company_name', description='Company:'),
		web.form.Checkbox('use_company_name', description='Use company name?'),
		web.form.Button('Update Settings')
	)
	
	def fill_settings_form(self):
		form = self.form
		settings = app.db.get_settings()
		form.fill({
			'name': settings.name,
			'email': settings.email,
			'phone': settings.phone,
			'logo_path': settings.logo_path,
			'company_name': settings.company_name,
			'use_company_name': settings.use_company_name
		})
		return form

	def GET(self):
		form = self.fill_settings_form()
		return render.settings(form)
		
	def POST(self):
		form = self.fill_settings_form()
		if not form.validates():
			return render.settings(form)
		config.db.update('settings', where='enabled=1',
			name=form.d.name,
			email=form.d.email,
			phone=form.d.phone,
			logo_path=form.d.logo_path,
			company_name=form.d.company_name,
			use_company_name=form.d.use_company_name
		)
		raise web.seeother('/settings')
		

## run application
application = web.application(urls, globals())

if __name__ == '__main__': 
	application.run()
		
