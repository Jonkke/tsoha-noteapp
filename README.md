# Note app for tsoha course

This is a note taking / time tracing app that will be built as part of a university course project on databases. More detailed specification below in finnish.

A running Heroku instance of the app can be viewed [here](https://tsoha-noteapp.herokuapp.com/)

Test account credentials for the Heroku app:  
Username: testi  
Password: passu

## Dokumentaatio

[Aihekuvaus & käyttäjätarinat](docs/userstories.md)

## Asennus (Linux & Mac)

Ennen kuin aloitat, varmista että Pythonin versio 3.5 (tai uudempi) sekä Pythonin PIP-kirjasto ovat asennettuna. Kloonaa tämä repositorio koneellesi ja mene kloonattuun kansioon komentoriviltä. Luo sitten virutaaliympäristö komennolla
```
python3 -m venv venv
```
Aktivoi tämän jälkeen virtuaaliympäristö komennolla
```
source venv/bin/activate
```
Virtuaaliympäristön pitäisi olla nyt aktivoitu, minkä voit nähdä komentoriville rivin eteen ilmestyvästä (venv) -tekstistä. Asenna seuraavaksi projektin riippuvuudet, jotka siis asentuvat vain tähän aktiiviseen virtuaaliympäristöön. Tee tämä komennolla
```
pip install -r requirements.txt
```
Kaiken pitäisi nyt olla valmiina ohjelman ajamista varten. Aja ohjelma komennolla
```
python run.py
```
Tämän jälkeen voit avata selaimen ja kirjoittaa osoiteriville "127.0.0.1:5000". Ohjelman pitäisi nyt avautua tarkasteltavaksi.