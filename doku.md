Wadharkka
=========

Lyhyt kuvaus
------------
Harjoitustyöni on Markdown-dokumenttiditori, jossa on tuki dokumenttien jakamiselle ja WYSIWYG-Markdown editori.

Alkuperäissuunitelma
--------------------

Web-sovellusohjelmoinnin harjoitustyön aiheena on online-tekstieditori.
Sovellus on Google Docs tyylinen dokumenttieditori.
Sovellukseen voi luoda useita käyttäjiä, jotka tunnistautuvat OpenID- tai OAuth-palvelun avulla.
Käyttäjä voi luoda useita dokumentteja ja jakaa niitä muiden käyttäjien kanssa.
Muille käyttäjille voi halutessaan myös antaa käyttöoikeuden oman dokumentin muokkaamiseen.
Editorina käytän joko HTML:n textarea-tagia ja tallennan dokumentit tekstimuodossa tai HTML5:n contenteditable-attribuutin tarjoamaa WYSIWYG-editoria jolloin tallennan dokumentit HTML-muodossa.
Sovellus arkistoi dokumenttien vanhan versiot, kuten esim. Wikipedia tekee.
Sovellus ei tule todennäköisesti tukemaan dokumenttien samanaikaista muokkausta, muuten kuin antamalla Wikipedia-tyylisiä virheviestejä, ellei ylimääräistä aikaa jää tuen toteuttamiseen.

Projektin toteuttamiseen käytän web-sovelluskehyksenä Djangoa.
Tietokantana tulen ainakin alustavasti käyttämään Postgresia, koska Heroku näyttäisi tarjoavan ainoastaan sen oletuksena.
Joka tapauksessa, käytän Djangon ORMia tietokantakutsuihin, joten tietokantaa voi todennäköisesti vaihtaa jälkikäteenkin.
Näkymien toteuttamiseen käytän Djangon omaa template-systeemiä.

Selainpuolen toteutukseen käytän todennäköisesti vain HTML/CSS ja Javascript/JQuery.
En usko, että aion käyttää mitään kehittyneempiä javascript käyttöliittymäkirjastoja, mutta  en osaa sanoa vielä varmasti. Twitter bootstrap näyttää tosin kiinnostavalta.

Palvelimen testaamiseen käytän Pythonin mukana tulevaa unittest pakettia.
Selainpuolen integraatiotestaukseen käyttänen Seleniumia.

Ominaisuuksien priorisointi:
1. käyttäjien rekistöröinti ja tunnistus
2. dokumentin luonti ja muokkaus
3. dokumenttiversioiden arkistointi
4. dokumenttien käyttöoikeuksien muokkaus ja jakaminen
5. WYSIWYG/HTML-editori
6. dokumenttien samanaikainen muokkaus

Aikataulu:
viikko 1: Tietokannan tarkempi määrittely; käyttäjien rekistöröinti ja tunnistus; testien kirjoittelua
viikko 2: prototyyppieditorin toteutus ja testien kirjoittelua
viikko 3: dokumenttiversioiden arkistointi ja testien kirjoittelua
viikko 4: dokumenttien käyttöoikeudet ja jakaminen; testien kirjoittelua
viikko 5: WYSIWYG-editori, käyttöliittymän kohentelua ja muita selainpuolen asioita;
Seleniumiin tutustuminen; (integraatio)testausta
viikko 6: viimeistelyä, dokumentointia ja testausta

Toteutetut ominaisuudet
-----------------------
+ Käyttäjien tunnistus OpenIDllä (tai tunnistus ja rekistöröinti ylläpito-paneelin kautta)
+ Dokumenttien luonti ja muokkaus
+ Dokumenttien jakaminen muiden käyttäjien kesken email-osoitteiden perusteellay
+ WYSIWYG-Markdown editori
+ Samanaikaisten muokkauksien konfliktitilanteiden hallinta
+ Yksikkötestejä djangon testimoduuleilla
+ Cross site scripting -hyökkäyksien esto

Toteutamatta jääneet ominaisuudet
---------------------------------
+ Viestien arkistointi


Havaitut bugit
--------------
+ Lomakkeiden virheviestit ovat välillä melko hyödyttömiä (esim. pelkkä "404").
+ Javascript-palikka dokumenttien jakamislomakkeessa generoi epävalidia HTMLää.
+ Cross site scripting -esto on poistettu Markitdown javascript editorin preview nappulan näkymästä, koska en saanut sitä toimimaan ilman javascriptiin kajoamista.
+ Ylläpitopaneelin automaattisesti generoidut lomakkeet eivät validoi aina oikein tai muutenkaan ole kovinkaan hiottuja.
+ Postgresql bugailee ihmeellisesti herokussa joten asetin oletuksena sqlite3 tietokannan. Tietokantaa voi vaihtaa settings.py:stä.
+ DEBUG-moodia ei kannata kytkeä pois koska staattisen tiedostojen palvelua ei ole konfiguroitu sen pois päällä ollessa.

Testit
------
Yksikkötestit sijaitsevat tests.py tiedostossa ja ne voi ajaa komennolla 

    ./manage.py test wadharkka

Heroku
------

http://fierce-dawn-8749.herokuapp.com/

Ylläpitopaneelin tunnukset:
käyttäjänimi: testi123
salasana:  123qwe

Asennusohjeet lokaalisti
------------------------

    git clone git@github.com:fzzbt/wadharkka.git
    cd wadharkka/wadharkka

Tietokannan voi konfiguroida DATABASEa muuttelemalla.
Oletusasetukset pitäisi toimia kunhan sqlite on asennettuna.

Asenna tarvittavat python2 paketit pip:llä.
(Voi olla järkevää käyttää virtualenviä
kts. heroku-ohjeet https://devcenter.heroku.com/articles/django)

    pip install   Django==1.4 distribute==0.6.24  django-social-auth==0.6.9 httplib2==0.7.4 misaka==1.0.2  oauth2==1.5.211 psycopg2==2.4.4 python-openid==2.2.5 wsgiref==0.1.2

pip on joillakin systeemeissä pip2 tai pip-2.7 tms.

käynnistys:

    ./manage.py runserver
