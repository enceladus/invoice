import web
import config
import app.db

# Fetch settings from database
t_globals = {
	'settings': app.db.get_settings()
}

def logged():
	if session.login == 1:
		return True
	else:
		return False
		

def render(base=config.base_template):
	#if !logged():
	#	return web.template.render(config.template_dir + '/login', cache=config.cache, globals=t_globals)
	return web.template.render(config.template_dir, base=base, cache=config.cache, globals=t_globals)