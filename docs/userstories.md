## Muistiinpano- ja ajanseuraamisohjelma

Ohjelma jolla voi tehdä ja tarkastella muistiinpanoja ja jakaa niitä muille käyttäjille joko vain lukuoikeuksin, tai myös kirjoitusoikeuksin. Ohjelman käyttötapaukset ovat seuraavat (SQL-lauseissa voi olla epätarkkuuksia eivätkä ne välttämättä toimi täysin samoin kuin SQLAlchemyn generoimat SQL-lausekkeet,joita ohjelmassa enimmäkseen käytetään. Näiden tarkoitus on lähinnä demonstroida ohjelman toimintaa yleisellä tasolla):

### Käyttötapaukset

#### Käyttäjät

- Käyttäjä voi luoda itselleen käyttäjätunnuksen ja salasanan
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
INSERT INTO account (date_created, date_modified, username, password_hash, five_letter_identifier) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?);
```
</p></details>
</blockquote>

- Käyttäjä voi vaihtaa oman salasanansa
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
UPDATE account SET date_modified=CURRENT_TIMESTAMP, password_hash=? WHERE account.id = ?
```
</p></details>
</blockquote>

- Käyttäjä voi kirjautua sisään tai ulos luodulla tunnuksella ja salasanalla
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.username AS account_username, account.password_hash AS account_password_hash, account.five_letter_identifier AS account_five_letter_identifier 
FROM account 
WHERE account.username = ?
LIMIT ? OFFSET ?;
```
</p></details>
</blockquote>

#### Muistiinpanot

- Käyttäjä voi nähdä listattuna kaikki muistiinpanot, joihin hänellä on lukuoikeus. Hän voi myös etsiä tagien perusteella muistiinpanoja niiden joukosta.
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
SELECT * FROM (note n INNER JOIN user_note_read unr ON n.id = unr.note_id) WHERE user_id = ?;
```
</p></details>
</blockquote>

- Käyttäjä voi luoda uusia muistiinpanoja, jotka ovat oletuksena vain ne luoneen käyttäjän muokattavissa ja luettavissa
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
INSERT INTO note (date_created, date_modified, creator_id, last_editor_id, title, content) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?)
INSERT INTO user_note_read (user_id, note_id) VALUES (?, ?)
INSERT INTO user_note_write (user_id, note_id) VALUES (?, ?)
```
</p></details>
</blockquote>

- Käyttäjä voi muokata muistiinpanon sisältöä, mikäli hänellä on siihen kirjoitusoikeus
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
UPDATE note SET date_modified=CURRENT_TIMESTAMP, content=? WHERE note.id = ?;
INSERT INTO tag (date_created, date_modified, name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?);
INSERT INTO note_tag (note_id, tag_id) VALUES (?, ?);
INSERT INTO user_note_read (user_id, note_id) VALUES (?, ?);
INSERT INTO user_note_write (user_id, note_id) VALUES (?, ?);
```
</p></details>
</blockquote>

- Käyttäjä voi poistaa muistiinpanon, mikäli hänellä on siihen kirjoitusoikeus
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
DELETE FROM user_note_read WHERE user_note_read.user_id = ? AND user_note_read.note_id = ?;
DELETE FROM note_tag WHERE note_tag.note_id = ? AND note_tag.tag_id = ?;
DELETE FROM user_note_write WHERE user_note_write.user_id = ? AND user_note_write.note_id = ?;
DELETE FROM note WHERE note.id = ?;
```
</p></details>
</blockquote>

- Käyttäjä voi liittää muistiinpanoon tageja, mikäli hänellä on siihen kirjoitusoikeus
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
INSERT INTO tag (date_created, date_modified, name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?);
INSERT INTO note_tag (note_id, tag_id) VALUES (?, ?);
```
</p></details>
</blockquote>

#### Kontaktit

- Käyttäjä voi lähettää kontaktipyyntöjä toiselle käyttäjälle, mikäli hänellä on hallussaan tämän viisikirjaiminen tunnistusmerkkijono
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
INSERT INTO user_contact (user_id, contact_id, inviter, confirmed) VALUES (?, ?, ?, ?);
```
</p></details>
</blockquote>

- Käyttäjä voi hyväksyä tai hylätä hänelle tulleen kontaktipyynnön. Hyväksyminen vahvistaa kahden käyttäjän välisen kontaktin
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
UPDATE user_contact SET confirmed='1' WHERE user_id=:uid1 AND contact_id=:uid2
DELETE FROM user_contact WHERE user_id = :uid1 AND contact_id = :uid2
```
</p></details>
</blockquote>

- Käyttäjä voi jakaa muistiinpanon kontaktilistallaan olevan käyttäjän kanssa, joko pelkällä lukuoikeudella tai myös kirjoitusoikeudella
<blockquote>
<details><summary> Näytä SQL </summary>
<p>

```SQL
INSERT INTO user_note_read (user_id, note_id) VALUES (?, ?);
INSERT INTO user_note_write (user_id, note_id) VALUES (?, ?);
```
</p></details>
</blockquote>

### Tietokantakaavio

Alla on tietokantakaavio, josta ilmenee taulut ja niiden relaatiot muistiinpanoihin liittyvälle toiminnallisuudelle. Tämä kaavio voi laajentua myöhemmin, jos/kun ohjelmaan tulee lisää toiminnallisuutta:

![Tietokantakaavio](relations.png)

### Puutteet ohjelmassa

Ohjelma on ajanpuutteen ja muiden tekosyiden takia jäänyt aika raakileeksi siitä, mitä sen alun perin piti olla. Ulkoasu on paikoin aika järkyttävä, mutta myös toiminnallisuuksissa on joitakin puutteita:

- Luotua käyttäjää ei pysty poistamaan
- Käyttäjä ei voi valita itselleen erillistä näyttönimeä
- Muistiinpanolistassa ei ole sivutusta
- Muistiinpanolistaa ei voi suodattaa muuten kuin tagihaulla. Myöskään esim. päivämäärän tai jaetun käyttäjän perusteella järjestäminen ei onnistu
- Muistiinpanojen sisältöä ei voi muotoilla mitenkään
- Kontaktikäyttäjien profiileja tms. tietoja ei voi tarkastella, muutenkin tämä "kaveriominaisuus" on aika hiomaton ja pelkistetty
- Kontaktia ei myöskään pysty poistamaan kun se on hyväksytty
- Myös koodi sisältää paikoin purkkaratkaisuja ja refaktoroitavaa riittäisi
