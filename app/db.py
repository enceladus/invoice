import web
from config import db

# GET FROM DATABASE
def get_all(table, limit=None):
	return db.select(table, order='id', limit=limit)

def get_from_table(table, id):
	return db.select(table, where='id=$id', vars=locals())
	
def get_client_id(name):
	client = db.select('client', where='name=$name', vars=locals())
	return client[0].id

def get_invoice_items(invoice_id):
	return db.select('item', order='date', where='invoice_id=$invoice_id', vars=locals())
	
def get_settings():
	return db.select('settings')[0]

# DELETE FROM DATABASE
def delete(table, id):
	db.delete(table, where='id=$id', vars=locals())
	if (table == 'invoice'):
		for item in get_invoice_items(id):
			delete_from_db('item', item.id)

# INSERT INTO DATABASE		
def new(table, **values):
	db.insert(table, **values)

# UPDATE DATABASE ENTRY	
def update(table, id, **values):
	db.update(table, where='id=$id', vars=locals(), **values)
	