### Asennus- ja käynnistysohjeet

Ennen kuin aloitat, varmista että Pythonin versio 3.5 (tai uudempi) sekä Pythonin PIP-kirjasto ovat asennettuna. Lataa tämä repositorio koneellesi ja mene kloonattuun kansioon komentoriviltä. Kaikki komennot on ajettava saman hakemiston sisältä, eli projektin juuresta!

Luo sitten virutaaliympäristö komennolla
```
python3 -m venv venv
```
Aktivoi tämän jälkeen virtuaaliympäristö, komento riippuu käyttöjärjestelmästäsi:

Linux & Mac:
```
source venv/bin/activate
```
Windows:
```
venv/bin/activate
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


### Käyttöohjeet

Ohjelmaan on mahdollista luoda uusi käyttäjä ja kirjautua sisään luodun käyttäjän tunnuksella ja salasanalla. Sisäänkirjautunut käyttäjä voi lukea olemassa olevia muistiinpanoja, luoda uusia muistiinpanoja ja myös muokata ja poistaa jo olemassa olevia muistiinpanoja. Jotta muistiinpano näkyy käyttäjälle, on hänellä oltava tähän lukuoikeus. Muokkaaminen ja poistaminen vaativat lisäksi kirjoitusoikeuden. Muistiinpanon luojalla on aina luku- ja kirjoitusoikeus luomiinsa muistiinpanoihin, eikä niitä voi poistaa häneltä. Käyttäjällä on kontaktilista muista käyttäjistä, jolle voi kutsua uusia käyttäjiä viisikirjaimisen käyttäjäkohtaisen tunnusmerkkijonon avulla. Toisen käyttäjän on hyväksyttävä kutsu jotta kontakti vahvistetaan. Kun kontakti on vahvistettu, voivat nämä kaksi käyttäjää jakaa luomiaan muistiinpanoja toisilleen. Toiselle käyttäjälle voi antaa vain lukuoikeuden, tai halutessaan myös kirjoitusoikeuden jaettuun muistiinpanoon. Oikeudet voi myös poistaa muistiinpanokohtaisesti, paitsi muistiinpanon omistajalta, eli sen luoneelta käyttäjältä.

##### Etusivu
Kirjautumattomalle käyttäjälle etusivulla on kirjautumislomake. Oikeassa yläkulmassa on myös linkki uuden käyttäjän rekisteröintilomakkeeseen.

##### List notes
List notes -välilehden alla listataan kaikki muistiinpanot, joihin käyttäjällä on lukuoikeus. Sivulla on myös hakufunktio, jolla voi etsiä käyttäjälle näkyviä muistiinpanoja niiden sisältämien tagien perusteella. Tagit erotetaan välilyönnillä, ja haku ottaa huomioon myös tiettyyn tagiin liittyvät osittaiset merkkijonot. Tageja, joihin käyttäjällä on kirjoitusoikeus, voi muokata tai poistaa muistiinpanokohtaisilla Edit- ja Delete-nappuloilla.

##### New note
New note -välilehdeltä voi lisätä uuden muistiinpanon. Muistiinpanolle täytyy antaa otsikko, mutta muu sisältö, jakaminen ja tagit ovat vapaaehtoisia. Muistiinpanon voi jakaa joko luku- tai kirjoitusoikeuksilla toiselle käyttäjälle, mikäli kyseinen käyttäjä on kirjautuneen käyttäjän kontaktilistassa (kts. Account & Contacts). Tageja voi lisätä alimpaan tekstikenttään, tagit erotellaan toisistaan välilyönnillä. Tämä sama lomake on käytössä myös jo luotua muistiinpanoa muokattaessa (jos siihen on kirjoitusoikeudet käyttäjällä). Lisäksi muistiinpanon omistaja, eli luoja, näkee listan käyttäjistä joille tämä muistiinpano on jaettu. Muistiinpanon jakamisen voi poistaa toiselta käyttäjältä klikkaamalla tämän nimeä listassa.

##### Account & Contacts
Account & Contacts -välilehdellä käyttäjä voi tarkastella oman tilinsä tietoja, vaihtaa salasanansa, nähdä omat kontaktinsa listattuna, nähdä vahvistusta odottavat kontaktipyynnöt, sekä lähettää kontaktipyynnön toiselle käyttäjälle.

Kontaktipyynnön lähettäminen tapahtuu siten, että jompikumpi käyttäjä kertoo ensin toiselle oman viisikirjaimisen yksilöivän tunnuksensa (joka näkyy Account & Contacts -välilehdellä), jolloin toinen voi lähettää kontaktipyynnön tällä tunnuksella. Jos tunnusmerkkijono vastaa jotain käyttäjää, saa tämä käyttäjä kontaktipyynnön joka on vielä hyväksyttävä, ennen kuin kontakti on vahvistettu. Kun kontakti on vahvistettu, voivat nämä kaksi käyttäjää jakaa muistiinpanoja toisilleen joko pelkällä lukuoikeudella tai myös kirjoitusoikeudella.