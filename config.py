import web

## Admin Login
username = 'admin'
password = 'password'

## Database Configuration
db_type = 'sqlite'
db_name = 'invoice'
db_user = 'db_user'			# Not needed for sqlite
db_pass = 'db_password'		# Not needed for sqlite

## Template Configuration
template_dir = 'templates'
base_template = 'base'

## Other Settings
debug = True 			# True if in development
cache = False			# False if in development

#### -- touch nothing below here -- ####
if db_type == 'sqlite':
	db = web.database(dbn=db_type, db=db_name)
else:
	db = web.database(dbn=db_type, db=db_name, user=db_user, passwd=db_pass)