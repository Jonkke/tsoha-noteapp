### CREATE TABLES -lauseet
Tässä on listattuna ohjelman käyttämät CREATE TABLE -lauseet tietokantataulujen luomiseen. Käytännössä näitä ei käytetä tällaisenaan suoraan koodissa, vaan ohjelma käyttää flask-SQLAlchemy -kirjastoa tietokantataulujen ja ohjelmassa esiintyvien luokkien yhdistämiseen, ja nämä lauseet on generoitu näiden yhteyksien pohjalta:

```
CREATE TABLE tag (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(32) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	username VARCHAR(144) NOT NULL, 
	password_hash VARCHAR(144) NOT NULL, 
	five_letter_identifier VARCHAR(5) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE note (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	creator_id INTEGER NOT NULL, 
	last_editor_id INTEGER NOT NULL, 
	title VARCHAR, 
	content VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(creator_id) REFERENCES account (id), 
	FOREIGN KEY(last_editor_id) REFERENCES account (id)
);
CREATE TABLE user_contact (
	user_id INTEGER NOT NULL, 
	contact_id INTEGER NOT NULL, 
	inviter INTEGER NOT NULL, 
	confirmed BOOLEAN, 
	date_contacted DATETIME, 
	PRIMARY KEY (user_id, contact_id), 
	FOREIGN KEY(user_id) REFERENCES account (id), 
	FOREIGN KEY(contact_id) REFERENCES account (id), 
	FOREIGN KEY(inviter) REFERENCES account (id), 
	CHECK (confirmed IN (0, 1))
);
CREATE TABLE note_tag (
	note_id INTEGER NOT NULL, 
	tag_id INTEGER NOT NULL, 
	PRIMARY KEY (note_id, tag_id), 
	FOREIGN KEY(note_id) REFERENCES note (id), 
	FOREIGN KEY(tag_id) REFERENCES tag (id)
);
CREATE TABLE user_note_read (
	user_id INTEGER NOT NULL, 
	note_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id, note_id), 
	FOREIGN KEY(user_id) REFERENCES account (id), 
	FOREIGN KEY(note_id) REFERENCES note (id)
);
CREATE TABLE user_note_write (
	user_id INTEGER NOT NULL, 
	note_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id, note_id), 
	FOREIGN KEY(user_id) REFERENCES account (id), 
	FOREIGN KEY(note_id) REFERENCES note (id)
);
```