CREATE TABLE item (
	id integer primary key,
	description TEXT,
	rate FLOAT,
	hrs FLOAT,
	invoice_id integer,
	date DATE
);

CREATE TABLE invoice (
	id integer primary key,
	client_id integer,
	project_title TEXT,
	description TEXT,
	date DATE
);

CREATE TABLE client (
	id integer primary key,
	name TEXT,
	address TEXT,
	city TEXT,
	state TEXT,
	zip_code TEXT,
	contact TEXT,
	phone TEXT,
	email TEXT
);

CREATE TABLE settings (
	name TEXT,
	email TEXT,
	phone TEXT,
	logo_path TEXT,
	company_name TEXT,
	use_company_name BOOLEAN
);
	