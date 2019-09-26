# Note app for tsoha course

This is a note taking / time tracing app that will be built as part of a university course project on databases. More detailed specification below in finnish.

A running Heroku instance of the app can be viewed [here](https://tsoha-noteapp.herokuapp.com/)

Test account credentials for the Heroku app:  
Username: testi  
Password: passu

## Muistiinpano- ja ajanseuraamisohjelma

Tarkoituksena on luoda ohjelma, jolla voi tehdä ja tarkastella muistiinpanoja, kuin myös seurata esimerkiksi kursseihin ja opiskeluun käytettyä aikaa tietyllä aikavälillä. Tässä vaiheessa tietokantakaaviossa on vasta pelkkiin muistiinpanoihin liittyvät taulut ja relaatiot. Alla listattuna ohjelmaan tässä vaiheessa liittyviä toiminnallisuuksia:

- Käyttäjä voi luoda itselleen käyttäjätunnuksen ja salasanan
- Käyttäjä voi kirjautua sisään tai ulos luodulla tunnuksella ja salasanalla
- Käyttäjä voi luoda uusia muistiinpanoja, jotka ovat oletuksena vain ne luoneen käyttäjän muokattavissa ja luettavissa
- Kirjoitusoikeudet olemassa olevaan muistiinpanoon omaava käyttäjä voi muokata muistiinpanon sisältöä
- Muistiinpanoihin voi liittää tageja (WIP)
- Käyttäjä voi halutessaan jakaa muistiinpanon muiden käyttäjien kanssa, joko pelkällä lukuoikeudella tai myös kirjoitusoikeudella (WIP)
- Käyttäjä voi etsiä tagien avulla muistiinpanoja, joihin hänellä on lukuoikeus (WIP)

Ominaisuuksia jotka saatetaan toteuttaa, käytettävissä olevasta ajasta ym. riippuen:
- Muistiinpanoon lukuoikeudet omaava käyttäjä voi liittää muistiinpanoon muistutuksen, joka käytännössä aiheuttaa jonkinnäköisen muistiinpanoon liittyvän pop-upin ohjelman käyttöliittymässä määriteltynä ajanhetkenä
- Käyttäjän muistiinpanot ja muut arkaluontoiset tiedot salakirjoitetaan tietokantaan

Alla on tietokantakaavio, josta ilmenee taulut ja niiden relaatiot muistiinpanoihin liittyvälle toiminnallisuudelle. Tämä kaavio voi laajentua myöhemmin, jos/kun ohjelmaan tulee lisää toiminnallisuutta:

![Tietokantakaavio](docs/initialDiagram.png)

