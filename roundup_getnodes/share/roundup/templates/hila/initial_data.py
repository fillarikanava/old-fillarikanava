#!/usr/bin/python
# -*- coding: UTF-8 -*-
from roundup import install_util, password
from roundup.date import Date

#
# TRACKER INITIAL PRIORITY AND STATUS VALUES
#
pri = db.getclass('priority')
pri.create(name=''"critical", order="1")
pri.create(name=''"urgent", order="2")
pri.create(name=''"bug", order="3")
pri.create(name=''"feature", order="4")
pri.create(name=''"wish", order="5")

stat = db.getclass('status')
stat.create(name=''"new", order="1") # Uusi
stat.create(name=''"discussion", order="3") # Keskustelu
stat.create(name=''"remarked", order="5") # Huomioitu
stat.create(name=''"request for comments", order="7") # Kommentteja toivotaan
stat.create(name=''"concluded", order="9") # Päättynyt



#stat.create(name=''"unread", order="1")
#stat.create(name=''"deferred", order="2")
#stat.create(name=''"chatting", order="3")
#stat.create(name=''"need-eg", order="4")
#stat.create(name=''"in-progress", order="5")
#stat.create(name=''"testing", order="6")
#stat.create(name=''"done-cbb", order="7")
#stat.create(name=''"resolved", order="8")

organisations = {}

organisation = db.getclass('organisation')
organisations['hila'] = organisation.create(screenname='HILA', name='HILA')
organisations['anonymous'] = organisation.create(screenname='', name='Anonymous')
organisations['citizen'] = organisation.create(screenname='', name='Citizen') # Kansalainen
organisations['kaupunkisuunnitteluvirasto'] = organisation.create(screenname='Kaupunkisuunnitteluvirasto', name='Kaupunkisuunnitteluvirasto', css='background-color:#FFFFFF;')
organisations['uservoice_citizen'] = organisation.create(screenname=u'uservoice-käyttäjä'.encode('utf-8'), css='background-color:#FFFFFF;', name=u'Kaupunkifillari uservoice user'.encode('utf-8'), homeurl="http://kaupunkifillari.uservoice.com/", signature=u'Tämä viesti on vanhasta Kaupunkifillari-blogin Uservoice-kyselystä.'.encode('utf-8'))


language = db.getclass('language')
language.create(name='finnish', order="1")
language.create(name='swedish', order="2")
language.create(name='english', order="3")

# create the two default users


user = db.getclass('user')
user.create(username="admin", password=adminpw,
                address=admin_email, roles='Admin', screenname="Anonymous", organisation=['hila'])
anon_id = user.create(username="anonymous", roles='Anonymous', screenname="Anonymous User", organisation=['anonymous'])

users = {'anonymous':anon_id}
users['reima'] = user.create(username="reima", screenname="Reima Karhila", password=password.Password('bb'),
                address="reima@openfeedback.org", roles='Admin', organisation=['hila'])



# add any additional database creation steps here - but only if you
# haven't initialised the database with the admin "initialise" command

msg = db.getclass('msg')
#
issue = db.getclass('issue')


usercounter = 0

message_ids = []
users["fillariehdokkaat"] = db.user.create(username="fillariehdokkaat",screenname="fillariehdokkaat", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Hämeentielle pyöräkaista. Itäisestä kantakaupungista on vaikeaa päästä keskustaan, kun Hämeentien joutuu aina kiertämään. Olemme ajaneet tätä valtuustossa, mutta muut puolueet vastustavat.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Hämeentielle väliä Hakaniemi - Sörnäinen on ehdottomasti saatava pyöräkaistat'.encode('utf-8'))
message_ids.append (str(id))
users["apoikola"] = db.user.create(username="apoikola",screenname="apoikola", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["apoikola"],\
      content=u'Haemme vastausta siihen, miksi uusimmassa Helsingin pyöräreittiverkoston päivityksessä ei vieläkään saatu Hämeentietä mukaan, vaan ainoastaan pyöräilijöille annettiin lohdutuspalkintona lupaus parantaa Kauppatorin Katajanokan puoleisen kulman pyöräilyjärjestelyitä\
Asiaa hoitaa: Martti Tulenheimo'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Hämeentie on Helsingin pyörätieverkoston musta aukko. Molemmille puolille ajoväylää tulisi tehdä korokkeella erotetut pyöräilykaistat.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräilykaista Hämeentielle Kurvista Hakaniemeen'.encode('utf-8'),\
date=Date('2008-03-11.19:29:54'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Periaatteessa uusien väylien suunnittelusta vastaa kaupunkisuunnitteluvirasto ja rakentamisesta ja korjaamisesta rakennusvirasto. Näidenkin virastojen sisällä on valtaisa mahdollisuus hukata palaute väärään osoitteeseen. Tästä syystä olemme juurikin selvittämässä tätä, että kuka (yksittäinen henkilö) vastaa, vai vastaako.\
Odotellessa voit ilmiantaa pahoja paikkoja tänne, niin ne eivät unohdu.'.encode('utf-8'))
message_ids.append (str(id))
users["Vuokko"] = db.user.create(username="Vuokko",screenname="Vuokko", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["Vuokko"],\
      content=u'Onko tietoa, mille tahoille pk-seudun kaupungeissa tästä asiasta voi antaa palautetta? Jos yksittäinen risteys on erityisen häiritsevä tai rakennustöiden seurauksena "hyvä" risteys muuttuu hankalasti reunakiveykselliseksi, keneen voi suoraan ottaa yhteyttä?'.encode('utf-8'))
message_ids.append (str(id))
users["pirjo"] = db.user.create(username="pirjo",screenname="pirjo", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["pirjo"],\
      content=u'Hienoa, että asia on saanut kannatusta ja etenee!\
Jossain paikoissa on loivennettu kiveystä puoliksi niin, että toiseen suuntaan mennessä on hyvä pyöräillä, mutta toiseen suuntaan joutuu pompauttamaan pyörää tai koukkaamaan vastaantulijan kaistalta. En ymmärrä logiikkaa, kun pyörällä pitää kuitenkin ajaa oikeaa reunaa noissa paikoissa. Olen muuten saanut kerran renkaankin hajoamaan reunakiveen.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["apoikola"],\
      content=u'Mitkä ohjeistukset ohjaavat reunakivien laittoa, millä niitä perustellaan, kuka vastaa, jos alunperin matala reunakivi on muuttunut kadun painuman myötä korkeaksi. Entä jos reunakivi on hyvin matala reunastaan vain 2cm, mutta kuitenkin niin jyrkkä, että pyörä siihen töksähtää. Reunakivettömyys auttaisi rullatuoleilla ja lastenrattailla liikkuvia.\
Asiaa hoitaa: Reima Karhila'.encode('utf-8'))
message_ids.append (str(id))
users["ipaloniemi"] = db.user.create(username="ipaloniemi",screenname="ipaloniemi", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["ipaloniemi"],\
      content=u'Espooseen Kilon ja Leppävaaran välille rakenettiin vast\'ikään uusi tie, pyöräteineen. Friisinmäentie. Käsitämätöntä että edelleen tehdään näitä 5-8cm reunoja. Joka kerta kun pudottaa ensinnä vauhdin lähelle nollaa ja sitten pompauttaa korokkeen yli niin miettii että onko todellakin niin että tämä apina on käynyt kuussakin kun näin järkevästi teitä edelleenkin tehdään.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["apoikola"],\
      content=u'Reunakivillä on funktio sokeille, jotka siten paremmin havaitsevat tien, mutta toisaalta ne ovet esteellistä suunnittelua lähes kaikille muille, pyöräilijät etunenässä, mutta pyörätuolit, lastenrattaat, ostoskärryt ja terveet jalatkin saattavat tökätä reunakiviin.'.encode('utf-8'))
message_ids.append (str(id))
users["Otto Puolakka"] = db.user.create(username="Otto Puolakka",screenname="Otto Puolakka", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["Otto Puolakka"],\
      content=u'Todella hyvä huomio. Kanttikiveystä on usein loivennettu suojatien kohdalla, muttei lainkaan riittävästi. Renkaita näihin kiviin saa tosin tuskin hajoamaan, ennemminkin vaarana on vanteen vääntyminen iskusta.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["pirjo"],\
      content=u'Jalkakäytävä/pyörätie on yleensä erotettu ajoväylästä reunakorokkeella. Suojateiden kohdalla sitä ei kuitenkaan saisi olla, jotta pyörällä pääsisi sujuvammin suojatielle ja takaisin pyörätielle.\
\
Joissain paikoissa korokkeet ovat niin korkealla, että pyöränkumit ovat vaarassa hajota. Todellakin tahtoisin pyöräreittien olevan kauttaaltaan tasaisia ilman noita turhia töyssyjä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Reunakorokkeet pois suojateiden kohdalta'.encode('utf-8'),\
date=Date('2008-03-11.19:29:54'),\
author=u'pirjo'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["Vuokko"],\
      content=u'Tämän pitäisi olla lähtökohta koko liikennesuunnittelussa: kevyen liikenteen katkeamattomat, suorat ja nopeat yhteydet. Uskoakseni kaikki pyöräilijät kannattavat tätä koko kaupungin alueelle, ei ainoastaan keskustaan. Tämän yhtenäisyyden ja sujuvuuden alle kuuluvat oikeastaan liikennevalokysymyksetkin - jos reitti on hyvin suunniteltu, siihen eivät kuulu pysähdykset nappeja painelemaan.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Silloin kun pyörätietä pääsee käyttämään, se useimmiten katkeaa jossakin kohtaa. Uusi pätkä alkaa jossakin muutaman sadan metrin päässä. Jos tämän pätkän ajaa kävelytiellä saa aikaan murinaa. Autotielle kurvaaminen yhtäkkiä parin sadan metrin matkalle aiheuttaa vaaratilanteita. Lentääkö pitäisi? Pyörätieverkko pitäisi saada yhtenäiseksi, tämä vaatisi hiukan suunnittelua, tarkistelua ja tahtoa.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Keskustan pyörätieverkko yhtenäisiksi'.encode('utf-8'),\
date=Date('2008-09-20.05:57:18'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["Vuokko"],\
      content=u'Keskuspuistossa olisi tarpeen käydä kaikki reitit läpi ja tarkistaa kaikki suuntaviitat ja niiden kattavuus. Uusia reittejä pyöräillessäni kiroilen itse, kun alkupäästä viitoitetun reitin opasteet loppuvat kesken matkaa eikä pyöräilykartta tuo apua pienestä mittakaavasta johtuen. Yksittäisten risteysten puutteita puistossa pitäisi kerätä vaikka GPS:llä, kun väylillä ja risteyksillä ei ole nimiä.'.encode('utf-8'))
message_ids.append (str(id))
users["Esko Lius"] = db.user.create(username="Esko Lius",screenname="Esko Lius", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["Esko Lius"],\
      content=u'Tiedot hölmöistä tai puutteellisista viitoituksista sekä parannusehdotukset tähän ketjuun. Saan hoidettua hommaa kaupungin suuntaan tehokkaammin, kun meillä on tukevasti dataa kerättynä.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["apoikola"],\
      content=u'Ai mihin tämä tie katosikaan?? Paljonko maksaa viittojen ylläpito, kenen budjettiin tarvitaan lisärahoja tätä varten? Vai voisiko viitoitusta parantaa nykyresursseillakin, jos siihen vain panostettaisiin?\
Asiaa hoitaa: Esko Lius'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Kevyen liikenteen väylille tarvitaan kattava viitoitusjärjestelmä, jota myös säännöllisesti ylläpidetään. Nykyinen satunnaisia viittoja siellä täällä sisältävä järjestelmä on hyvä pohja, mutta viittoja tarvitaan paljon enemmän. Erityisesti Keskuspuiston alueella ja muualla missä kevyen liikenteen väylä kulkee erillään nimettyjen katujen varsista, risteyksissä tulisi olla suuntaviitat.\
\
Tätä voi verrata autojen opastusjärjestelmään: Kuinka moni autoilija hyväksyisi tilanteen, jossa esimerkiksi kehäteiden varsilla ainoastaan noin joka viides liittymä olisi viitoitettu, ja näiden jäljellejäävienkin viittojen oikeaan suuntaan ei voisi luottaa ylläpidon puutteessa?\
Puhumattakaan pienemmistä risteyksistä, joissa viittoja ei olisi lainkaan.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräteiden viitoitus'.encode('utf-8'),\
date=Date('2008-03-11.19:29:54'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Kolme eri nappivaloja koskevaa ehdotusta kiilaavat yhteisäänillään aivan ehdotusten kärkipäähän. Selvitämme, mistä liikenteenohjauksen filosofisesta suuntauksesta juontavat juurensa joskus aivan käsittämättömästi sijoitellut ja väärin toimivat, matkaa hidastavat, maailman kuuluistat, iki-ihanat NAPPIVALOT?\
Asiaa hoitaa: Antti Poikola'.encode('utf-8'))
message_ids.append (str(id))
users["righa"] = db.user.create(username="righa",screenname="righa", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["righa"],\
      content=u'Napit ovat nöyryyttäviä jalankulkijoille sekä pyöräilijöille, mutta erityisen harmillisia ne ovat pyöräilijöille. En halua mennä siksakkia, kun olen kerran sattunut suojatien eteen. Napit voisivat sen sijaan laittaa autoilijoille, että pääsisivät jossain vaiheessa etenemään kun sattuvat suojatien eteen.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Napit liikennevaloista kokonaan pois'.encode('utf-8'),\
date=Date('2008-03-11.19:29:54'),\
author=u'righa'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Pyörätie, joka kiertää bussipysäkin takaa, lisää turvallisuutta, mutta hyöty menetetään, jos pysäkin mainokset peittävät näkyvyyden. Varsinkaan pimeällä ei voi nähdä, tuleeko joku vastaan pysäkin takaa. Mainos on yleensä paremmin valaistu kuin pyörätie. Joillakin pysäkeillä näkee jo nyt läpinäkyviä laseja, jotka olisivat paikallaan useammassakin paikassa. http://www.hepo.fi/index.php?sivu=kyselyt'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Eräs yleisimmistä pyöräteiden näkyvyyttä haittaavista asioista ovat bussipysäkkien katosrakenteet. Katoksissa on useinmiten läpinäkyvät takaseinät, mutta pyörätien suuntaisen näkymän estävät sivuseinissä olevat mainokset.\
\
Luonnollisesti katokset omistava JCDecaux tavoittelee sivuseinien mainoksilla mainosten näkyvyyttä ohi ajaville autoilijoille, mutta eikö pyöräilijöiden ja jalankulkijoiden liikenneturvallisuus pitäisi mennä tämän ohi se. mainokset olisivat sallittuja vain katosten takaseinissä, missä ne eivät estä kenenkään näkyvyyttä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Bussipysäkkien mainokset sivuseinistä takaseiniin'.encode('utf-8'),\
date=Date('2008-09-09.06:22:02'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Tukholmankadulle on kautta aikain toivottu pyörätietä, mutta ilmeisesti sellaista ei ole luvassa. Yleisesti ottaen kannatan mieluiten pyöräkaistoja tai liikenteen rauhoittamista se. pyöräily autokaistoilla on turvallista. Tukholmankatu on kuitenkin niin keskeinen autoliikenteen reitti, että siellä pyörätie erotettuna autoista olisi paikallaan.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyörätie Tukholmankadulle'.encode('utf-8'),\
date=Date('2008-09-03.14:59:28'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Kyselin telineen hintaa...\
--CLIP--\
\
Heklucht is per unit : 2812 USD ex tax, ex transport\
\
1990 euro\
\
An order of ten units is 990 euro per unit.\
\
Kind regards,\
\
Jeroen Bruls\
designer\
heklucht.nl\
\
> Hello,\
> How much does the bikestand with airpump cost and is it possible to\
> order those to Finland?\
> http://www.heklucht.nl/\
>\
> BR,\
-Antti Poikola'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Tämä Hollannin malliin koristeellinen pyörätelinemalli, jonka avulla voi samalla täyttää lässähtäneen renkaan, sopisi hyvin edustavn ulkonäkönsä puolesta myös paraatipaikoille kaupunkikuvaan. http://www.springwise.com/transportation/bike_stand_doubles_as_tire_pum/'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pumppu/pyörätelineyhdistelmiä julkisille paikoille'.encode('utf-8'),\
date=Date('2008-09-19.10:37:50'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
users["tulenheimo"] = db.user.create(username="tulenheimo",screenname="tulenheimo", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["tulenheimo"],\
      content=u'Jotta liikenne sujuisi Helsingissä kaikkien kannalta mukavammin, sujuvammin ja turvallisemmin, Helsingin polkupyöräilijät ry voisi järjestää koulutusta ammattimaisille tavarankuljettajille. Lainvastaisesti pysäköidyt tavaroita kuljettavat autot ovat keskeisimpiä sekä pyöräteiden että kävelykatujen toimivuutta hankaloittavia tekijöitä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Koulutusta lastinkuljettajille pyöräilijöiden huomioimiseksi'.encode('utf-8'),\
date=Date('2008-09-10.07:54:19'),\
author=u'tulenheimo'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Mechelininkatu on niin vilkas että se tarvitsisi pyörä kaistan. Tilaa löytyisi kyllä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Mechelininkadulle pyöräkaista'.encode('utf-8'),\
date=Date('2008-09-20.05:12:32'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Olemme muutamien pyöräilyaktiiviystävieni kanssa ideoineet sellaista palautekanavaa, jossa eri ihmisten antama palaute näkyisi muille käyttäjille (toki moderoinnin jälkeen, ettei rivoudet pääse julki).\
\
On täysin ymmärrettävää, ettette pysty sähköpostitse vastaamaan kaikkeen saamaanne palautteeseen, mutta jos edes antamani palaute jäisi johonkin julkisesti näkyviin, saisin vahvemman luottamuksen tunteen, että joku on edes lukenut sen. Toisaalta samasta asiasta ei tarvitsisi nillittää, mistä jo 10 muuta on antanut palautetta (niin, olisihan se pyörätie Tukholmankadulla erittäin mukava).\
\
Saattaisimme jopa harkita kyseisen systeemin pystyttämistä omin voiminemme, mutta tällöin olisi erittäin mielenkiintoista voida käyttää reittioppaan karttoja. Toki avoimeen käyttöön annetulla Googlemaps-systeemillä saa saman aikaan, mutta yleisön luottamusta reittioppaan imago varmasti lisäisi.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Yhteisöllinen palautekanava Helsingin pyöräilyoloista'.encode('utf-8'),\
date=Date('2008-09-03.14:56:49'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["righa"],\
      content=u'Bussikaistoille pitäisi maalata pyörien kuvat, sillä bussikuskit luulevat omistavansa kaistat, vaikka pyöräilijöiden kuuluu pyöräillä tällä kaistalla silloin kun ei ole pyörätietä. \
\
Pyöräsuojateille pitäisi maalata pyörien kuvat, jotta nokkelimmat ihmiset tajuaisivat että suojatie on pyöriä varten.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Bussikaistalle ja pyöräsuojatielle pyörän kuvat'.encode('utf-8'),\
date=Date('2008-09-19.19:09:17'),\
author=u'righa'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
users["toma"] = db.user.create(username="toma",screenname="toma", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["toma"],\
      content=u'Kun rahtisatama poistuu länsisatamasta niin pyörätie junaradan tilalle.  Jätkäsaari kokonaan autottomaksi näyttämään uutta suuntaa ekologiselle viihtyisälle kaupunkielämiselle.  Automelun ja ruuhkien sijaan korkeateknologiaa ja etätyöskentelyä.  Parkkitilojen sijaan harrastustiloja ja puistoja - tilaa ihmisille.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyörätie rautatieasemalta ruoholahteen'.encode('utf-8'),\
date=Date('2008-09-22.19:00:11'),\
author=u'toma'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Eripuolilla pääkaupunkiseutua on liikennevaloja, jotka ovat pääsääntöisesti vihreällä autoille, mutta nappia painamalla pyöräilijä tai jalankulkija saa (ainakin teoriassa) itselleen vihreän valon. Nappisysteemi sinänsä on ihan ok, mutta napin painallusta vain useinmiten seuraa pitkä epätietoisuuden jakso siitä, tapahtuiko mitään, vai onko laite kenties rikki.\
\
Eikö napin painamisen jälkeen valo voisi vaihtua autoilijoille välittömästi ensin keltaiseksi ja sitten punaiseksi, lähteehän hissikin liikkumaan kohti oikeaa kerrosta heti tilaamisen jälkeen eikä vasta 20-30 sekunnin odottelun jälkeen. Toki järjestelmässä pitää olla joku karenssiaika, että jos valot ovat juuri olleet vihreinä jalankulkijoille, niin siinä tapauksessa uudelleen nappia painanut joutuisi odottelemaan hetken, mutta silloinkin vaikka jollain äänisignaalilla tms. voisi indikoida nappia painaneelle, että pyyntö on rekisteröity.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Nappiliikennevalot nopeammiksi'.encode('utf-8'),\
date=Date('2008-09-19.08:19:42'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["Vuokko"],\
      content=u'Ongelma on se, että tällä tavalla keinotekoisesti pidennettäisiin pyöräilyreittejä. Mitä jos kotikadulta pääsisi ajamaan vain yhteen suuntaan? Jos maitokauppa tai koulu on vastakkaisessa suunnassa parin korttelin päässä samalla kadulla, sääntöä vastaan rikkomiseen olisi turhan suuri kiusaus ja rikkeet olisivat yleisiä nimenomaan pyörillä. Entäpä kaksisuuntainen pyöräily ja yksisuuntainen autoilu?'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["apoikola"],\
      content=u'Yksisuuntaisilla teillä autoilijoilla on tapana ajaa lujempaa, kuin kaksisuuntaisilla, elleiu tätä erityisesti rajoiteta.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Helsingin kaikki kadut pääväyliä lukuunottamatta voitaisiin muuttaa yksisuuntaisiksi, niin että joka toinen katu kulkisi eri suuntiin. Kaikilla tällaisilla kaduilla olisi siis yksi autokaista ja pyöräkaista samaan suuntaan. Nykyisellä katuleveydellä rinnalle mahtuisi vielä vinopysäköinti ja parkkipaikatkaan eivät vähenisi. Kaksisuuntaisilla pääväylillä olisi pyörätiet molemmin puolin jalkakäytävien rinnalla.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Helsingin kadut yksisuuntaisiksi ja pyöräkaista joka kadulle'.encode('utf-8'),\
date=Date('2008-09-19.10:44:59'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Fredrikinkatu on keskustassa tärkeä väylä. Fredalle - ja muillekin kaksikaistaisille, yksisuuntaisille kaduille - voitaisiin hyvin rakentaa kaksisuuntainen pyöräkaista.  \
\
Lisäksi mukulakiviosuus on todella kenkkumainen ajaa pyörällä, etenkin kun saa samalla pelätä ratikkakiskoilla liukastumista.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Fredan ongelmat'.encode('utf-8'),\
date=Date('2008-09-20.05:28:57'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
users["aetelaah"] = db.user.create(username="aetelaah",screenname="aetelaah", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["aetelaah"],\
      content=u'on ihan välttämätön! Autojen seassa ei voi ajaa tuollaisella paikalla ainakaan ison fillarilla kuljetettavan lastin kanssa.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Kaisaniemenkadulle pyöräilykaista'.encode('utf-8'),\
date=Date('2008-09-22.14:03:44'),\
author=u'aetelaah'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Miten tämä olisi ollut vältettävissä?\
\
Jalankulkija kuoli polkupyöräturmassa Helsingissä\
\
http://www.hs.fi/kaupunki/artikkeli/Jalankulkija+kuoli+polkupy%C3%B6r%C3%A4turmassa+Helsingiss%C3%A4/1135240383887'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["apoikola"],\
      content=u'Sähköpostikirjeenvaihto aiheesta tuotti seuraavan tarkennuksen:\
\
sovun säilymistä jalankulkijoiden ja pyöräilijöiden välillä esitäisi myöskin se, että myös pyöräilijät kunnioittaisivat pelkästään jalankulkijoille tarkoitettuja väyliä, samoin vauhdin hidastaminen mäessä jalankulkijoiden kanssa yhteisillä väylillä olisi suotavaa kummankin ryhmän turvallisuuden vuoksi.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["apoikola"],\
      content=u'On kurjaa, kun kaksi ekologisesti toimivaa ryhmää pyöräilijät ja jalankulkijat ovat keskenään tukkanuottasilla ja kovin sanankääntein syyllistämässä toisiaan. Perussyyttet ovat seuraavat:\
\
-Pyöräilijät kaahaavat liian lujaa ja läheltä \
\
-Jalankulkijat eivät kunnioita pyöräteitä, vaan hoopoilevat miten sattuu.\
\
Autoilijat puolustavat saarekkeitaan sitkeästi, meidän kahden ryhmän kannattaisi säilyttää vähintäänkin linnarauha keskenämme niin, että autoväki saataisiin itsensä kokoiselle tontille yhteistuumin.\
\
Pyöräilijöiden pitää vahvempana osapuolena ottaa huomioon jalankulkijat, siinäkin tapauksessa, että jalankulkija seisoisi keskellä pyörätietä. Jalankulkijoiden taas pitää ymmärtää, että pyörätie ei ole osa jalkakäytävää (vaikka liikennesuunnittelu ei tätä selväksi tee), vaan paremmin rinnastettavissa ajorataan. Jos jompi kumpi rikkoo näitä sääntöjä pitäisi löytyä sitä yhteistä kevyen liikenteen ymmärrystä, että asiasta huomautetaan sadattelematta.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräilijät ja jalankulkijat sopuun'.encode('utf-8'),\
date=Date('2008-09-21.10:15:20'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Pyöräilijöille pitää saada pyöräkaistat katkonaisten pyöräteiden tai ylikuormitettujen jalkakäytävien sijaan. Näin autoilijatkin tottuvat kaksipyöräisiin, ja osaavat ottaa fillaristit huomioon. Nykyiset pyörätiet ovat valitettavasti lähinnä huoltoautojen parkkipaikkoja tai koiranulkoilutusalueita.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräkaistat katkonaisten pyöräteiden sijaan'.encode('utf-8'),\
date=Date('2008-10-01.14:31:55'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Otsikko kertoo kaiken, on harmillista, että ainoa ydinkeskustan pyöräkaista on päällystetty erittäin hostiileilla historiallisilla mukuloilla.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Mukulakivet pois Unioninkadun pyöräkaistoilta'.encode('utf-8'),\
date=Date('2008-09-22.18:20:21'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Kampin keskuksen Fredrikinkadun puoleiselle sisäänkäynnille tarvitsisi muutaman pyörän vetävän pyörätelineen, sillä nykyisin siinä seisoo aina noin 5 pyörää ravintola Bruuverin edessä. Annankadun päässä olevan sisäänkäynnin luokse on hiljattain ilmestynyt erittäin hyvät pyörätelineet, jotka ovat myös erittäin suosittuja.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyörätelineet Kampin keskuksen Fredan sisäänkäynnille'.encode('utf-8'),\
date=Date('2008-09-19.07:57:12'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Pyöräilen ekaluokkaisen poikani kanssa koulusta kotiin päivittäin ja yleensä mukana kulkevat myös 4-vuotias omalla pyörällään ja 1-vuotias kyydissäni. Kehä I:n vieressä kulkevalla kevyen liikenteen väylällä mopoilu on sallittu Pakilan yläasteelle saakka. Mopoja on paljon, ja usein mopoilijoiden matka jatkuu myös ala-asteelle asti (vaikka tämä tosiaan on erikseen kielletty). \
Kyseinen kevyen liikenteen reitti on turvallisin koulutie meille. \
Miksei mopoja voi ohjata viereisille teille, jotka Pakilassa ovat varsin hiljaisia? Näin pienemmät saisivat kulkea rauhassa pyörillään tai kävellen, sitten kun vanhemmat uskaltavat päästää yksin kulkemaan.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'mopot pois Pakilan pyöräteiltä'.encode('utf-8'),\
date=Date('2008-09-19.10:46:09'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Asennekampanjointi ei aina ole välttämättä kovin tehokasta, mutta jos poliisi ja pysäköinninvalvojat todella rupeaisivat sakottamaan pyörätielle pysäköiviä saattaisi toiminta muuttua. Jalankulkijoiden ja pyöräilijöiden välinen konflikti taas juontaa juurensa huonosta jalkapyörätörmäyskaistoja suosivasta liikennesuunnittelusta. Mielstäni paras ratkaisu olisi tähän pyöräkaistat.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Jalankulkijat eivät kunnioita pyöräkaistoja, eivätkä autotkaan, jotka pysäköivät niille varsin huolettomasti. Kun sen sijaan ajaa jalkakäytävällä vaikka kymmenenkin metriä saadakseen ajokkinsa parkkiin saajalankulkijoilta mitä epämiellyttävämpiä ja vihamielisempiä kommentteja. Autot kiilaavat ajoradalla ajavan pyöräilijän vaarallisesti. Pyöräilijä on todellista tienkäyttäjien paarialuokkaa! Tähän voitaisiin saada asennemuutos kampanjoinnilla ja pyörällä liikkuvien oikeuksien ja olojen parantamisella.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräilyn nostaminen pois lainsuojattoman asemasta'.encode('utf-8'),\
date=Date('2008-09-20.05:36:40'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
users["Jemina"] = db.user.create(username="Jemina",screenname="Jemina", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["Jemina"],\
      content=u'Helsingin jalkakäytävät ovat monessa paikassa epäkäytännöllisen suuret (esim. Mechelininkadulla). Otetaan mallia vaikka Saksasta tai Itävallasta: pienemmät jalkakäytävät ja pyöräkaista jalkakäytävästä erilleen autokaistan viereen kummallekin puolelle tietä. Kun pyörätie kulkisi ajoradan vieressä kaikilla suurilla kaduilla, edistettäisiin mm. sitä, että pyörätie ei vain yhtäkkiä loppuisi (vrt. esim. Mannerheimintie).'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Jalkakäytävistä puolet pois, pyöräkaista autokaistan viereen'.encode('utf-8'),\
date=Date('2008-10-05.10:06:53'),\
author=u'Jemina'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Kunnallisia tai työnantajien kustantamia tai henk koht kakkospyöriä asemien ja työpaikan/kodin liityntäpyöräksi, niin ei tarvitse raahat pyörää junassa kun sitä tarvitsee määränpäässä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'liityntäpyörät'.encode('utf-8'),\
date=Date('2008-09-19.19:31:55'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
users["Imppu"] = db.user.create(username="Imppu",screenname="Imppu", address="invalid@email"+ str(usercounter) +".no", organisation=['Kaupunkifillari uservoice user'])
usercounter += 1
id = msg.create(author=users["Imppu"],\
      content=u'Bulevardin pyörätie on varmaankin monille keskustan pyöräilijöille tuttu, kuten myös sen ongelmat - ohittaminen mahdotonta, raitiovaunuihin ja busseihin hyökkäävät jalankulkijat, autot parkissa keskellä pyöräkaistaa (muitakin autoja kuin se kukkaliikkeen citymaasturi ;-).\
Kaiken huippuna on kuitenkin pyörätien yläpäässä oleva yhteys Esplanadin puistoon..\
Erottajan kulmalla syttyy pyöräilijälle vihreä ja samalla vihreällä pääsee Esplanadin puiston etukulmaan, mutta lähes joka kerta pyörätien yli tunkee myös Bulevardilta Etelä-Esplanadille ajava auto!\
Autot voivat ajaa Bulevardilta joko pohjoisen suuntaan Mannerheimintielle tai etelän suuntaan Erottajalle, mutta Esplanadille on yhteys Yrjönkadun ja Diananpuiston kautta, ei suinkaan suoraan vihreällä olevan pyörätien yli.\
Aikuinen ehtii lähes aina yli kyseisen pyörätien ennen kuin se tai ne autot, mutta jos mukana on lapsi tai pyöräilijöitä useampia, muuttuu tilanne siten, että viimeisen ollessa pyörätiellä autoilija tunkee samaan kohtaan, samanaikaisesti kiertäen katukiven reunaa sekä varoen yhtä aikaa kahteen suuntaan kulkevia ratikoita ja Erottajalta alas tulevaa autovirtaa. Odotan kauhulla, koska tulee ensimmäinen uutinen, että pyöräilijä on jäänyt risteyksessä ajavan auton alle.\
Tästä on ilmoitettu kaupunkisuunnitteluvirastoon sekä poliisille, mutta toistaiseksi ei ole mitään tapahtunut.\
Ehdotankin, että pyörätien eteen Mannerheimintien nurkan puolelle rakennetaan puomi, joka laskeutuu alas siksi aikaa, kun pyörätiellä on vihreä valo. Puomi on aika järeä ratkaisu, mutta vaihtoehtona voi olla joko pyöräilijän kuolema tai vakava loukkaantuminen, jolloin puomi voisi sittenkin kuulostaa ihan järkevältä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Autojen ajo Bulevardilta Etelä-Esplanadille estettävä'.encode('utf-8'),\
date=Date('2008-10-25.13:32:57'),\
author=u'Imppu'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Haahuilevat, 10km nopeusrajoituksia ja räpättimiä vaativat jalankulkijat tulee sakon uhalla poistaa pyöräteiltä! Kyllä minä pyörällä väistän hitaampia, mutta pysyisivät omalla puolellaan, jos kerran nopeammat pelottavat. Pyöräilijät eivät saa ajaa jalkakäytävällä (no, eipä niitä pyöräteitäkään juuri ole), joten jalankulkijat pois tukkimasta niitä vähiäkin pyöräteitä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Jalankulkijat sakon uhalla pois pyörätieltä'.encode('utf-8'),\
date=Date('2008-09-22.08:49:33'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["toma"],\
      content=u'Voisi myös olla (kamera) valvontaa. Ystäväni pyörä varastettiin Elielin pyöräparkista. Varmaan on monen muunkin.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Lenkit joilla pyörän lukosta kiinni telineeseen, ovat hyviä mutta ne on usein rikki. Plussaa olisivat myös katetut pyörätelineet. Vanhat pyöränromut pitäisi myös aika ajoin poistaa, telineet eivät ole pitkäaikaissäilytykseen tarkoitettuja.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Juna-asemien säilytyksen parantaminen'.encode('utf-8'),\
date=Date('2008-09-22.09:35:25'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Uusia leveitä pyöräteitä ja parkkeja, citypyöriä! \
Koulutusta liikennesäännöistä, selkeät viitat, ja esim pyörätiet voisi olla punaisella merkitty ja joka paikassa omilla liikennevaloilla kuten kööpenhaminassa.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'pyöräteitä'.encode('utf-8'),\
date=Date('2008-09-21.07:49:16'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Pyöräilijät halutaan siivota pois autojen tieltä, ja helppo tapa siihen on merkitä viereinen jalkakäytävä yhdistetyksi kevyen liikenteen väyläksi. Siellä pyöräilijät joutuvat taistelemaan elintilastaan jalankulkijoiden, lastenrattaiden, rollaattoreiden, koirien, lasten ja seisoskelijoiden kiusana. Usein nämä "pyörätiet" ovat pyöräilyn pääväyliä kaupungissa. Samalla logiikalla Mannerheimintie voitaisiin laittaa kulkemaan päiväkodin pihan läpi. Pyöräilijöiden ei pidä suostua siihen, että heidät pakotetaan käyttökelvottomille reiteille. Kelvolliset väylät kuuluvat yhtä lailla pyöräilijöille.\
\
Ratkaisu: Yhdistetyllä kevyen liikenteen väylällä pyöräily vapaaehtoiseksi. Siellä saisivat ajaa ne, jotka eivät uskalla ajaa autojen seassa. Muut saavat pyöräillä laillisesti ajokaistalla.\
\
Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Yhdistetty kevyen liikenteen väylä ei aina sovellu ajamiseen'.encode('utf-8'),\
date=Date('2008-10-10.07:47:48'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Liikennemerkit ovat Salomonkadulla kadulla väärin koska sen kuuluisi olla myös pyöräilytie Runeberginkadulta Mannerheimintielle. Rakennusvirasto on tiennyt ainakin parin kuukauden ajan että merkit ovat virheelliset, ainakin YTV on ollut sinne päin yhteydessä. Miksi niitä oikeita merkkejä ei ole siis vieläkään siellä? On aika ikävää kun jalankulkijat luulee että pyöräilee jalankulkualuella kun pyöräilee siitä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Liikennemerkit Salomonkadulle'.encode('utf-8'),\
date=Date('2008-09-09.12:40:49'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Helsingissä on katuja, jotka pyöräilijät kokevat niin pelottaviksi, että useimmat eivät uskalla niillä ajaa. Jotkut polkevat henkensä uhalla autojen seassa, toiset taas sakon uhalla jalkakäytävillä. Ei ole hyväksyttävää, että pyöräilijä joutuu pelkäämään henkensä puolesta siellä, missä hänen liikennesääntöjen mukaan pitäisi ajaa. Hämeentie, Mechelininkatu, Mäkelänkatu ja Tukholmankatu ovat myös pyöräilijöiden pääreittejä: niiden varrella asuu ja työskentelee tuhansia pyöräilijöitä. Pyöräilyn tulee olla mahdollista ja turvallista kaikilla kaupungin kaduilla. Painosta päättäjiä, lähetä viestejä. Osallistu kriittisille pyöräretkille ja koe ilo polkea turvallisesti näilläkin kaduilla.\
\
Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Ajotiellä ei uskalla pyöräillä'.encode('utf-8'),\
date=Date('2008-10-10.07:54:55'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Rautateiden varsilla on mukavasti pyöräteitä. Matkan teon kannalta vauhti hiipuu ikävästi huonon suunnittelun takia. Mm Ilmalassa on hyväksi koetut reitit menty pilaamaan järjettömällä kaavoituksella.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'radanvarret vapaiksi'.encode('utf-8'),\
date=Date('2008-09-22.14:57:59'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Kaupunkikuvaan ja ihmisten arkeen vaikuttaa ikävimmin huonoksi osoittautuvat kaavoituspäätökset. Jotta "accountability" säilyisi pitkän aikavälinkin päätöksissä ehdottaisin tietokantaa, jossa  urpoimmat kaavoituspäätökset tehneet byrokraatit ja edustajat pantaisiin omalla nimellään ja naamallaan vastaamaan teoistaan.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Kaavoittajien mustalista'.encode('utf-8'),\
date=Date('2008-09-22.15:02:09'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Joissain paikoissa on liikennevaloja, jotka voisivat pääsääntöisesti vilkkua keltaisena. Jalankulkunappi voisi olla sitä varten, että jos on paljon autoja eikä pääse muuten yli, niin voisi painaa nappia jolloin valot toimisivat normaalisti'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Nappivalot keltaiselle'.encode('utf-8'),\
date=Date('2008-09-19.16:28:02'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["Vuokko"],\
      content=u'Kannatan tätä tasa-arvosyistä: autoliikenteen ei pitäisi olla etuoikeutetussa asemassa, joten sille ei pitäisi osoittaa huomattavasti enempää rahoja kuin joukko- tai kevyelle liikenteelle. Investointeja pitäisi tehdä ennen kaikkea sinne, missä se on suhteessa edullista ja hyödyttää mahdollisimman monia. Jalkakäytäville ja pyöräteille pääsy on lähes kaikilla, autoteille vain autoilijoilla.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["apoikola"],\
      content=u'Eli siis meinataanko tällä sitä, että jos suojatie korvataan liikenneturvallisuussyistä kevyen liikenteen alikululla olisi rahat otettava autoliikenteen potista, koska autoliikenne aiheuttaa liikenneturvallisuusriskin? Tai ehdotushan on, ettei olisi erillisiä potteja lainkaan.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Helsingin liikennemäärärahoja ei pitäisi eritellä kevyeeseen ja muuhun liikenteeseen. Tästä on seurannut se, että pyöräteihin ja alikulkutunneleihin ei ole ollut riittävästi varaa, vaikka ne tehdään pyöräilyn erottamiseksi muusta liikenteestä, joka on vaarallisempaa kuin pyöräily. Periaatteen kuitenkin pitäisi olla, että aiheuttaja maksaa.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Liikennemäärärahoja ei pidä eritellä kevyeeseen ja muuhun'.encode('utf-8'),\
date=Date('2008-10-01.14:41:49'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Pyöräteillä polkee sulassa sovussa ajamista harjoittelevia lapsia, vastuullisen rauhallisesti ajavia naisia,  kaltaisiani vauhdikkaita työmatkailijoita, vielä vauhdikkaampia pyöräilyn harrastajia, koululaisia ja monenlaisia muita pyöräilijöitä. Tärkeimmät pyöräilyoloja parantavat aloitteet ovat sellaisia, että niistä hyötyvät kaikki pyöräilijäryhmät. Helsingissä mielestäni etusijalle nousee pyöräilyreittien hoito.\
 \
Helsinki tarvitsee pyöräteiden hoitoon laatustandardin, jonka noudattamista myös valvotaan. Yhtäältä on huolehdittava siitä, että pyörätiet pidetään talvella aurattuina ja että hiekoitushiekat harjataan keväällä ripeästi pois. Toisaalta – ja tämä onkin isompi asia valvottavaksi – pyöräteille ei katutöitten tms. vuoksi saa jäädä kuoppia, terävää sepeliä tai muita pyöriä hidastavia esteitä. Nyt pyörätiet tuntuvat joskus kunnallisilta kuoppavarastoilta: kun jollekin tietyömaalle kaivettu kuoppa käy tarpeettomaksi, se siirretään sopivaan paikkaan keskelle pyörätietä.\
 \
Kun pyörätiet saadaan muutettua esteradoista ajoväyliksi, kaikenlaisten pyöräilijöiden liikkuminen tulee sekä mukavammaksi että turvallisemmaksi. Kunnossapitostandardi ei sitä paitsi edellytä juurikaan ylimääräistä rahaa.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Laatustandardi pyöräteiden hoitoon'.encode('utf-8'),\
date=Date('2008-10-01.15:02:43'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Nyt en ihan ymmärtänyt, mitä ehdotettiin?'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Helsingin kadut pääväyliä l'.encode('utf-8'),\
date=Date('2008-09-19.10:38:26'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Ehdotin vain tätä yhtä tiyttyä paikkaa, kun se tuli ensimmäisenä mieleen. Kun ehdotuksia viedään eteenpäin kaupunkisuunnitteluvirstoon on parempi, että kaikki toiveet on mahdollisimman tarkkaan spesifioitu.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["tulenheimo"],\
      content=u'Ryhmittymisalueita joka paikkaan, missä niitä tarvitaan! Liikennevalojen yhteydessä sekä vasemmalle kääntyvät pyöräilijät että ajotieltä oikealle erillään jatkuvalle pyörätielle kääntyvät pyöräilijät ovat vaarassa, koska autot eivät jätä tarpeeksi tilaa oikealle puolelle auton ja kadun reunan väliin.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["anonymous"],\
      content=u'Tänään Petri Sipilä esitteli valokuvia polkupyörille tarkoitetuista ryhmittymisalueista, joita liikennevaloristeyksissä on esim. Ruotsissa ja Englannissa. Eräs oivallinen paikka moiselle ryhmittymisalueelle olisi Telakkakadulla Hietalahden torin suuntaan mentäessä ennen Koffin alittavan tunnelin suuta.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Ryhmittymisalue Telakkakadulle'.encode('utf-8'),\
date=Date('2008-09-09.12:06:06'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["anonymous"],\
      content=u'Ajellessa pyörätietä Vanhankaupungin lahdelta Viikintietä pitkin kohti Viikkiä on vasemmalle kääntyvä tie lumikaatopaikalle, jota ennen löytyy tienviitta "Varokaa kääntyviä autoja". T-risteys on kuitenkin etuoikeutettu pyöräilijöille, sillä se on jopa varustettu stopilla ja pyöräilijöiden väistämis -merkillä. Eikö ennemminkin pitäisi laittaa autoteille kylttejä "Varokaa suoraan ajavia pyöräilijöitä"?'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Ylimääräinen liikennemerkki (?!)'.encode('utf-8'),\
date=Date('2008-09-23.19:32:12'),\
author=u'anonymous'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Päättyvän tien merkki ei läheskään aina tarkoita, ettei pyörällä pääsisi jatkamaan. Pahinta on, että tällaisia merkkejä on sijoiteltu pyöräilyn pääväylille. Pyöräilijä joutuu arvailemaan. Esimerkiksi Maamonlahdentien merkistä Lauttasaaressa on ilmoitettu kaupungin edustajille moneen kertaan, mutta merkkiä ei ole vaihdettu. Ilmoita virheellisistä merkeistä YTV:n palautelomakkeella tai kerro niistä HePolle. Pyrimme seuraamaan niiden korjaamista.\
\
Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Liikennemerkit unohtavat pyöräilijät'.encode('utf-8'),\
date=Date('2008-10-10.07:49:01'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Onko nämä kaikki nyt nimenomaan pyöräteitä, mitä tarkoitat, vai mahtuisiko mukaan muutama kunnon pyöräkaistakin?'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Helsinkiin on rakennettava kattava pyörätieverkosto. Polkupyöräily on liikennevaihtoehtona nostettava auton rinnalle. Alkuvaiheessa on rakennettava yhtenäiset, selkeästi merkityt, turvalliset ja ympärivuotisesti kunnossapidetyt pyörätiet Hämeentien, Lauttasaarentien, Mannerheimintien, Tukholmankadun varrelle sekä Pasilan, Vallilan ja ydinkeskustan alueelle. Pyörätiet on merkittävä kirkkaan punaisella tien laidalle.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Helsinkiin on rakennettava kattava pyörätieverkosto'.encode('utf-8'),\
date=Date('2008-10-01.12:41:45'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Helsingissä on yksisuuntaisia katuja paitsi keskustassa, myös Kalliossa, Vallilassa ja Munkkiniemessä. Monet niistä ovat hyvin hiljaisia, mutta pyörällä ei kuitenkaan saa ajaa vastasuuntaan. On kierrettävä autojen reittejä tai talutettava jalkakäytävällä.\
\
Kulosaaren Hopeasalmentie on yksisuuntainen. Hämmästyttävää on se, että tie on merkitty pyörämatkailureitiksi, ja YTV:n kevyen liikenteen reittiopas ohjaa tälle tielle myös kiellettyyn ajosuuntaan.\
\
Kaksisuuntainen pyöräily voidaan tehdä mahdolliseksi erilaisilla ratkaisuilla, jos niin halutaan. Tukholmassa ja monissa muissa eurooppalaisissa kaupungeissa näin on tehty.\
\
Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Yksisuuntaiset kadut haittaavat pyöräilyä'.encode('utf-8'),\
date=Date('2008-10-10.07:55:42'),\
author=u'apoikola'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Pyöräreitit pitää merkitä liikennemerkein paremmin kuin nykyään. Useinkaan kevyen liikenteen väylälle tullessa ei tiedä, että onkohan tämä pyörätie, kulkevatkohan kävelijät ja pyöräilijät samaa puolta vai onko tässä kaistat. Pyörätien voi katkaista rakennustyömaa ja opastus uudelle reitille puuttuu.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräreitit pitää merkitä liikennemerkein paremmin'.encode('utf-8'),\
date=Date('2008-10-01.14:34:30'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Työmatkapyöräilyä tulisi kannustaa yritysten pyörien muodossa eli luontaisetuna. Tähän liittyy katetut pyörätelineet. Pyörätelineen katos ei olisi suuri investointi.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Työmatkapyöräilyä tulisi kannustaa luontaisetuna'.encode('utf-8'),\
date=Date('2008-10-01.14:36:28'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Unelmakaupungissani joka paikkaan pääse pyörällä. Aloitteestamme Maankäytön ja asumisen ohjelmaan kirjattiin: ?Asemakaavoihin voidaan lisätä määräykset tonttikohtaisista polkupyöräpaikkojen vähimmäismääristä.? Tämä kirjaus on toteutettava. Pyöräilijän tarpeet on otettava huomioon rakentamisessa.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Unelmakaupungissani joka paikkaan pääse pyörällä'.encode('utf-8'),\
date=Date('2008-10-01.14:37:56'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Tavoite pyöräilyn tuplaamiseksi on vihdoin toteutettava rakentamalla pyöräilijöille turvalliset, sekä jalankulkijoista että autoista erotetut väylät: pyöräkaistat. Tämä tehdään merkitsemällä väylä kaistaviivan lisäksi huomiovärillä, kuvioinnilla, katumateriaalilla ja korkeusero reunakivellä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Tavoite pyöräilyn tuplaamiseksi'.encode('utf-8'),\
date=Date('2008-10-02.15:48:03'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Pyöräteitä voi edullisesti luoda liikennemerkeillä ja kaistamaalilla, niin että joka kaupunginosasta pääsisi yli 12-vuotiaat edes laillisesti liikkeelle joutumatta suoraan autojen sekaan. Tämä rohkaisee perheitä tarttumaan pyörään myös "kivikaupungin" alueella.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräteitä edullisesti liikennemerkeillä ja kaistamaalilla'.encode('utf-8'),\
date=Date('2008-10-01.14:43:32'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["apoikola"],\
      content=u'Huoltoasemilla yleensä on saatavilla adapteri, jolla pyöränkin renkaat saa täyteen. Voisihan näitä muuallakin olla, muistan aikanaan, kun kotikadullani ollut pyöräliike tarjosi paineilmaa postiluukusta tulevalla letkulla halukkaille ohikulkijoille.'.encode('utf-8'))
message_ids.append (str(id))
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Asemille tai kauppojen yhteyteen tai kaupungin rakennuksiin tai muihin sopiviin paikkoihin tarvitaan pummppuasemia pyörän kumin pumppaamiseksi. Onko jo saatavilla vuokrattavia peräkärryjä pyörään liitettäväksi?'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Asemille tai kauppojen yhteyteen pumppuasemia'.encode('utf-8'),\
date=Date('2008-10-01.14:45:08'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Helsingin pyöräilyverkon tulee olla kattava. Pyöräily töihin ja kouluun ei houkuta, jos välillä joutuu koukkaamaan autojen sekaan. Pyörätiet tulee valaista riittävästi. Jatkuvat tietyömaat ja pyörätielle väärin parkkeeratut autot haittaavat kulkua, tähän voisi puuttua ainakin autojen osalta sakottamalla (ja nostamalla pysäköintivirhemaksua). Työmatkapyöräilyyn voitaisiin kohdistaa markkinointikampanja, esimerkkinä Amsterdam tai Kööpenhamina.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Helsingin pyöräilyverkon tulee olla kattava'.encode('utf-8'),\
date=Date('2008-10-01.14:51:57'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Vähemmän autoja, enemmän turvallisia ja selkeästi merkittyjä pyöräteitä. Aamuisin on mahdotonta ylittää Pakilantie matkalla kouluun ja päiväkotiin. Alikulkutunnelissa saavat ajaa myös mopot, joita väistelen kahden pyöräilevän lapseni kanssa. Kolmas kiljuu kyydissä, kun mopot innostavat.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Enemmän turvallisia ja selkeästi merkittyjä pyöräteitä'.encode('utf-8'),\
date=Date('2008-10-01.14:56:04'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Pyöräreitit vapaaksi autoista pysäköinnin valvontaa tehostamalla. Helsingin villistä pysäköinnistä kärsivät niin pyöräilijät kuin jalankulkijatkin, eikä niin pientä esinettä ole, etteikö sen "lastaamiseksi" saisi pysäköidä jalkakäytävälle. Lisäksi poistaisin mopot pyöräteiltä ennen kuin sattuu pahasti. Asiat liittyvät toisiinsa siten, että molemmissa tapauksissa moottoriajoneuvo on sille kuulumattomalla paikalla.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräreitit vapaaksi autoista pysäköintiä valvomalla'.encode('utf-8'),\
date=Date('2008-10-01.15:08:10'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Haluan, että pyörien kuljettaminen joukkoliikennevälineissä olisi maksutonta. Metrossa näin jo on, mutta maksuttomuus tulisi laajentaa varsinkin juniin. Metroissa ja junissa tulisi olla pyörille merkatut paikat, jotta kuljetukselle olisi tilaa. Myös ratikka- ja bussikuljettamista olisi selvitettävä.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyörien kuljettaminen joukkoliikennevälineissä maksuttomaksi'.encode('utf-8'),\
date=Date('2008-10-01.15:11:35'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Erilliset pyöräkaistat ja oikeus ajaa myös ajoradalla. Kevyen liikenteen väylät ovat monesti heikkolaatuisia ja jopa turvattomia. Lisää ajatuksia Kesäfillari-blogini entryssä http://fillari.blogspot.com/2008/08/poliitikko-keksi-pyr.html" Poliitikko, keksi pyörä!'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Erilliset pyöräkaistat ja oikeus ajaa myös ajoradalla'.encode('utf-8'),\
date=Date('2008-10-03.13:28:39'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Pyörille omat kaistat autokaistojen reunaan, ei jalankulkijoiden sekaan.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyörille omat kaistat autokaistojen reunaan'.encode('utf-8'),\
date=Date('2008-10-03.14:36:19'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Yhtenäisiä pyöräilykaistoja tarvitaan lisää, ettei tien puolta tarvitsisi jatkuvasti vaihtaa. Esimerkiksi Kööpenhaminassa pyörällä pystyy helposti liikkumaan ihan ydinkeskustassakin. Pyöräilyyn kannattaa panostaa, koska se on ympäristöystävällistä ja hyvä tapa saada liikuntaa ja vireämpi mieli toimistotyöläisille.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Yhtenäisiä pyöräilykaistoja tarvitaan lisää'.encode('utf-8'),\
date=Date('2008-10-13.17:59:02'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'I innerstaden borde gatuparkering ersättas med cykelfiler på i medeltal varannan gata.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'I innerstaden borde gatuparkering ersättas med cykelfiler'.encode('utf-8'),\
date=Date('2008-10-13.18:03:17'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )

message_ids = []
id = msg.create(author=users["fillariehdokkaat"],\
      content=u'Pyöräteitä lisää nykyiseen tahtiin, keskustaan myös pyöräkaistoja (mm. Mansku pohjoiseen päin). Tulevaisuudessa poikittaisliikenteeseen ja lähiöihin suuntautuviin pikaratikoihin pyörienkuljetustilat.'.encode('utf-8'))
message_ids.append (str(id))
id=db.issue.create(title=u'Pyöräteitä lisää, keskustaan myös pyöräkaistoja'.encode('utf-8'),\
date=Date('2008-10-13.18:08:02'),\
author=u'fillariehdokkaat'.encode('utf-8'),\
                   status='2', priority='3', messages=message_ids, score='2' )







#
#usercounter = 0
#
#
#message_ids = []
#users["fillariehdokkaat"] = db.user.create(username="fillariehdokkaat", screenname="fillariehdokkaat", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Hämeentielle pyöräkaista. Itäisestä kantakaupungista on vaikeaa päästä keskustaan, kun Hämeentien joutuu aina kiertämään. Olemme ajaneet tätä valtuustossa, mutta muut puolueet vastustavat.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Hämeentielle väliä Hakaniemi - Sörnäinen on ehdottomasti saatava pyöräkaistat'.encode('utf-8'))
#message_ids.append (str(id))
#users["apoikola"] = db.user.create(username="apoikola", screenname="apoikola", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["apoikola"],\
#      content=u'Haemme vastausta siihen, miksi uusimmassa Helsingin pyöräreittiverkoston päivityksessä ei vieläkään saatu Hämeentietä mukaan, vaan ainoastaan pyöräilijöille annettiin lohdutuspalkintona lupaus parantaa Kauppatorin Katajanokan puoleisen kulman pyöräilyjärjestelyitä\
#Asiaa hoitaa: Martti Tulenheimo'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Hämeentie on Helsingin pyörätieverkoston musta aukko. Molemmille puolille ajoväylää tulisi tehdä korokkeella erotetut pyöräilykaistat.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräilykaista Hämeentielle Kurvista Hakaniemeen'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-03-11.19:29:54')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Periaatteessa uusien väylien suunnittelusta vastaa kaupunkisuunnitteluvirasto ja rakentamisesta ja korjaamisesta rakennusvirasto. Näidenkin virastojen sisällä on valtaisa mahdollisuus hukata palaute väärään osoitteeseen. Tästä syystä olemme juurikin selvittämässä tätä, että kuka (yksittäinen henkilö) vastaa, vai vastaako.\
#Odotellessa voit ilmiantaa pahoja paikkoja tänne, niin ne eivät unohdu.'.encode('utf-8'))
#message_ids.append (str(id))
#users["Vuokko"] = db.user.create(username="Vuokko", screenname="Vuokko", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["Vuokko"],\
#      content=u'Onko tietoa, mille tahoille pk-seudun kaupungeissa tästä asiasta voi antaa palautetta? Jos yksittäinen risteys on erityisen häiritsevä tai rakennustöiden seurauksena "hyvä" risteys muuttuu hankalasti reunakiveykselliseksi, keneen voi suoraan ottaa yhteyttä?'.encode('utf-8'))
#message_ids.append (str(id))
#users["pirjo"] = db.user.create(username="pirjo", screenname="pirjo", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["pirjo"],\
#      content=u'Hienoa, että asia on saanut kannatusta ja etenee!\
#Jossain paikoissa on loivennettu kiveystä puoliksi niin, että toiseen suuntaan mennessä on hyvä pyöräillä, mutta toiseen suuntaan joutuu pompauttamaan pyörää tai koukkaamaan vastaantulijan kaistalta. En ymmärrä logiikkaa, kun pyörällä pitää kuitenkin ajaa oikeaa reunaa noissa paikoissa. Olen muuten saanut kerran renkaankin hajoamaan reunakiveen.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["apoikola"],\
#      content=u'Mitkä ohjeistukset ohjaavat reunakivien laittoa, millä niitä perustellaan, kuka vastaa, jos alunperin matala reunakivi on muuttunut kadun painuman myötä korkeaksi. Entä jos reunakivi on hyvin matala reunastaan vain 2cm, mutta kuitenkin niin jyrkkä, että pyörä siihen töksähtää. Reunakivettömyys auttaisi rullatuoleilla ja lastenrattailla liikkuvia.\
#Asiaa hoitaa: Reima Karhila'.encode('utf-8'))
#message_ids.append (str(id))
#users["ipaloniemi"] = db.user.create(username="ipaloniemi", screenname="ipaloniemi", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["ipaloniemi"],\
#      content=u'Espooseen Kilon ja Leppävaaran välille rakenettiin vast\'ikään uusi tie, pyöräteineen. Friisinmäentie. Käsitämätöntä että edelleen tehdään näitä 5-8cm reunoja. Joka kerta kun pudottaa ensinnä vauhdin lähelle nollaa ja sitten pompauttaa korokkeen yli niin miettii että onko todellakin niin että tämä apina on käynyt kuussakin kun näin järkevästi teitä edelleenkin tehdään.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["apoikola"],\
#      content=u'Reunakivillä on funktio sokeille, jotka siten paremmin havaitsevat tien, mutta toisaalta ne ovet esteellistä suunnittelua lähes kaikille muille, pyöräilijät etunenässä, mutta pyörätuolit, lastenrattaat, ostoskärryt ja terveet jalatkin saattavat tökätä reunakiviin.'.encode('utf-8'))
#message_ids.append (str(id))
#users["Otto Puolakka"] = db.user.create(username="Otto Puolakka", address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["Otto Puolakka"],\
#      content=u'Todella hyvä huomio. Kanttikiveystä on usein loivennettu suojatien kohdalla, muttei lainkaan riittävästi. Renkaita näihin kiviin saa tosin tuskin hajoamaan, ennemminkin vaarana on vanteen vääntyminen iskusta.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["pirjo"],\
#      content=u'Jalkakäytävä/pyörätie on yleensä erotettu ajoväylästä reunakorokkeella. Suojateiden kohdalla sitä ei kuitenkaan saisi olla, jotta pyörällä pääsisi sujuvammin suojatielle ja takaisin pyörätielle.\
#\
#Joissain paikoissa korokkeet ovat niin korkealla, että pyöränkumit ovat vaarassa hajota. Todellakin tahtoisin pyöräreittien olevan kauttaaltaan tasaisia ilman noita turhia töyssyjä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Reunakorokkeet pois suojateiden kohdalta'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-03-11.19:29:54')
##db.issue.set(id, creator=users['pirjo'])
#message_ids = []
#id = msg.create(author=users["Vuokko"],\
#      content=u'Tämän pitäisi olla lähtökohta koko liikennesuunnittelussa: kevyen liikenteen katkeamattomat, suorat ja nopeat yhteydet. Uskoakseni kaikki pyöräilijät kannattavat tätä koko kaupungin alueelle, ei ainoastaan keskustaan. Tämän yhtenäisyyden ja sujuvuuden alle kuuluvat oikeastaan liikennevalokysymyksetkin - jos reitti on hyvin suunniteltu, siihen eivät kuulu pysähdykset nappeja painelemaan.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Silloin kun pyörätietä pääsee käyttämään, se useimmiten katkeaa jossakin kohtaa. Uusi pätkä alkaa jossakin muutaman sadan metrin päässä. Jos tämän pätkän ajaa kävelytiellä saa aikaan murinaa. Autotielle kurvaaminen yhtäkkiä parin sadan metrin matkalle aiheuttaa vaaratilanteita. Lentääkö pitäisi? Pyörätieverkko pitäisi saada yhtenäiseksi, tämä vaatisi hiukan suunnittelua, tarkistelua ja tahtoa.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Keskustan pyörätieverkko yhtenäisiksi'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-20.05:57:18')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["Vuokko"],\
#      content=u'Keskuspuistossa olisi tarpeen käydä kaikki reitit läpi ja tarkistaa kaikki suuntaviitat ja niiden kattavuus. Uusia reittejä pyöräillessäni kiroilen itse, kun alkupäästä viitoitetun reitin opasteet loppuvat kesken matkaa eikä pyöräilykartta tuo apua pienestä mittakaavasta johtuen. Yksittäisten risteysten puutteita puistossa pitäisi kerätä vaikka GPS:llä, kun väylillä ja risteyksillä ei ole nimiä.'.encode('utf-8'))
#message_ids.append (str(id))
#users["Esko Lius"] = db.user.create(username="Esko Lius", address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["Esko Lius"],\
#      content=u'Tiedot hölmöistä tai puutteellisista viitoituksista sekä parannusehdotukset tähän ketjuun. Saan hoidettua hommaa kaupungin suuntaan tehokkaammin, kun meillä on tukevasti dataa kerättynä.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["apoikola"],\
#      content=u'Ai mihin tämä tie katosikaan?? Paljonko maksaa viittojen ylläpito, kenen budjettiin tarvitaan lisärahoja tätä varten? Vai voisiko viitoitusta parantaa nykyresursseillakin, jos siihen vain panostettaisiin?\
#Asiaa hoitaa: Esko Lius'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Kevyen liikenteen väylille tarvitaan kattava viitoitusjärjestelmä, jota myös säännöllisesti ylläpidetään. Nykyinen satunnaisia viittoja siellä täällä sisältävä järjestelmä on hyvä pohja, mutta viittoja tarvitaan paljon enemmän. Erityisesti Keskuspuiston alueella ja muualla missä kevyen liikenteen väylä kulkee erillään nimettyjen katujen varsista, risteyksissä tulisi olla suuntaviitat.\
#\
#Tätä voi verrata autojen opastusjärjestelmään: Kuinka moni autoilija hyväksyisi tilanteen, jossa esimerkiksi kehäteiden varsilla ainoastaan noin joka viides liittymä olisi viitoitettu, ja näiden jäljellejäävienkin viittojen oikeaan suuntaan ei voisi luottaa ylläpidon puutteessa?\
#Puhumattakaan pienemmistä risteyksistä, joissa viittoja ei olisi lainkaan.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräteiden viitoitus'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-03-11.19:29:54')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Kolme eri nappivaloja koskevaa ehdotusta kiilaavat yhteisäänillään aivan ehdotusten kärkipäähän. Selvitämme, mistä liikenteenohjauksen filosofisesta suuntauksesta juontavat juurensa joskus aivan käsittämättömästi sijoitellut ja väärin toimivat, matkaa hidastavat, maailman kuuluistat, iki-ihanat NAPPIVALOT?\
#Asiaa hoitaa: Antti Poikola'.encode('utf-8'))
#message_ids.append (str(id))
#users["righa"] = db.user.create(username="righa", screenname="righa", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["righa"],\
#      content=u'Napit ovat nöyryyttäviä jalankulkijoille sekä pyöräilijöille, mutta erityisen harmillisia ne ovat pyöräilijöille. En halua mennä siksakkia, kun olen kerran sattunut suojatien eteen. Napit voisivat sen sijaan laittaa autoilijoille, että pääsisivät jossain vaiheessa etenemään kun sattuvat suojatien eteen.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Napit liikennevaloista kokonaan pois'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-03-11.19:29:54')
##db.issue.set(id, creator=users['righa'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Pyörätie, joka kiertää bussipysäkin takaa, lisää turvallisuutta, mutta hyöty menetetään, jos pysäkin mainokset peittävät näkyvyyden. Varsinkaan pimeällä ei voi nähdä, tuleeko joku vastaan pysäkin takaa. Mainos on yleensä paremmin valaistu kuin pyörätie. Joillakin pysäkeillä näkee jo nyt läpinäkyviä laseja, jotka olisivat paikallaan useammassakin paikassa. http://www.hepo.fi/index.php?sivu=kyselyt'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Eräs yleisimmistä pyöräteiden näkyvyyttä haittaavista asioista ovat bussipysäkkien katosrakenteet. Katoksissa on useinmiten läpinäkyvät takaseinät, mutta pyörätien suuntaisen näkymän estävät sivuseinissä olevat mainokset.\
#\
#Luonnollisesti katokset omistava JCDecaux tavoittelee sivuseinien mainoksilla mainosten näkyvyyttä ohi ajaville autoilijoille, mutta eikö pyöräilijöiden ja jalankulkijoiden liikenneturvallisuus pitäisi mennä tämän ohi se. mainokset olisivat sallittuja vain katosten takaseinissä, missä ne eivät estä kenenkään näkyvyyttä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Bussipysäkkien mainokset sivuseinistä takaseiniin'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-09.06:22:02')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Tukholmankadulle on kautta aikain toivottu pyörätietä, mutta ilmeisesti sellaista ei ole luvassa. Yleisesti ottaen kannatan mieluiten pyöräkaistoja tai liikenteen rauhoittamista se. pyöräily autokaistoilla on turvallista. Tukholmankatu on kuitenkin niin keskeinen autoliikenteen reitti, että siellä pyörätie erotettuna autoista olisi paikallaan.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyörätie Tukholmankadulle'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-03.14:59:28')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Kyselin telineen hintaa...\
#--CLIP--\
#\
#Heklucht is per unit : 2812 USD ex tax, ex transport\
#\
#1990 euro\
#\
#An order of ten units is 990 euro per unit.\
#\
#Kind regards,\
#\
#Jeroen Bruls\
#designer\
#heklucht.nl\
#\
#> Hello,\
#> How much does the bikestand with airpump cost and is it possible to\
#> order those to Finland?\
#> http://www.heklucht.nl/\
#>\
#> BR,\
#-Antti Poikola'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Tämä Hollannin malliin koristeellinen pyörätelinemalli, jonka avulla voi samalla täyttää lässähtäneen renkaan, sopisi hyvin edustavn ulkonäkönsä puolesta myös paraatipaikoille kaupunkikuvaan. http://www.springwise.com/transportation/bike_stand_doubles_as_tire_pum/'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pumppu/pyörätelineyhdistelmiä julkisille paikoille'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.10:37:50')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#users["tulenheimo"] = db.user.create(username="tulenheimo", screenname="tulenheimo", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["tulenheimo"],\
#      content=u'Jotta liikenne sujuisi Helsingissä kaikkien kannalta mukavammin, sujuvammin ja turvallisemmin, Helsingin polkupyöräilijät ry voisi järjestää koulutusta ammattimaisille tavarankuljettajille. Lainvastaisesti pysäköidyt tavaroita kuljettavat autot ovat keskeisimpiä sekä pyöräteiden että kävelykatujen toimivuutta hankaloittavia tekijöitä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Koulutusta lastinkuljettajille pyöräilijöiden huomioimiseksi'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-10.07:54:19')
##db.issue.set(id, creator=users['tulenheimo'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Mechelininkatu on niin vilkas että se tarvitsisi pyörä kaistan. Tilaa löytyisi kyllä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Mechelininkadulle pyöräkaista'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-20.05:12:32')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Olemme muutamien pyöräilyaktiiviystävieni kanssa ideoineet sellaista palautekanavaa, jossa eri ihmisten antama palaute näkyisi muille käyttäjille (toki moderoinnin jälkeen, ettei rivoudet pääse julki).\
#\
#On täysin ymmärrettävää, ettette pysty sähköpostitse vastaamaan kaikkeen saamaanne palautteeseen, mutta jos edes antamani palaute jäisi johonkin julkisesti näkyviin, saisin vahvemman luottamuksen tunteen, että joku on edes lukenut sen. Toisaalta samasta asiasta ei tarvitsisi nillittää, mistä jo 10 muuta on antanut palautetta (niin, olisihan se pyörätie Tukholmankadulla erittäin mukava).\
#\
#Saattaisimme jopa harkita kyseisen systeemin pystyttämistä omin voiminemme, mutta tällöin olisi erittäin mielenkiintoista voida käyttää reittioppaan karttoja. Toki avoimeen käyttöön annetulla Googlemaps-systeemillä saa saman aikaan, mutta yleisön luottamusta reittioppaan imago varmasti lisäisi.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Yhteisöllinen palautekanava Helsingin pyöräilyoloista'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-03.14:56:49')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["righa"],\
#      content=u'Bussikaistoille pitäisi maalata pyörien kuvat, sillä bussikuskit luulevat omistavansa kaistat, vaikka pyöräilijöiden kuuluu pyöräillä tällä kaistalla silloin kun ei ole pyörätietä. \
#\
#Pyöräsuojateille pitäisi maalata pyörien kuvat, jotta nokkelimmat ihmiset tajuaisivat että suojatie on pyöriä varten.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Bussikaistalle ja pyöräsuojatielle pyörän kuvat'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.19:09:17')
##db.issue.set(id, creator=users['righa'])
#message_ids = []
#users["toma"] = db.user.create(username="toma", screenname="toma", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["toma"],\
#      content=u'Kun rahtisatama poistuu länsisatamasta niin pyörätie junaradan tilalle.  Jätkäsaari kokonaan autottomaksi näyttämään uutta suuntaa ekologiselle viihtyisälle kaupunkielämiselle.  Automelun ja ruuhkien sijaan korkeateknologiaa ja etätyöskentelyä.  Parkkitilojen sijaan harrastustiloja ja puistoja - tilaa ihmisille.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyörätie rautatieasemalta ruoholahteen'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-22.19:00:11')
##db.issue.set(id, creator=users['toma'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Eripuolilla pääkaupunkiseutua on liikennevaloja, jotka ovat pääsääntöisesti vihreällä autoille, mutta nappia painamalla pyöräilijä tai jalankulkija saa (ainakin teoriassa) itselleen vihreän valon. Nappisysteemi sinänsä on ihan ok, mutta napin painallusta vain useinmiten seuraa pitkä epätietoisuuden jakso siitä, tapahtuiko mitään, vai onko laite kenties rikki.\
#\
#Eikö napin painamisen jälkeen valo voisi vaihtua autoilijoille välittömästi ensin keltaiseksi ja sitten punaiseksi, lähteehän hissikin liikkumaan kohti oikeaa kerrosta heti tilaamisen jälkeen eikä vasta 20-30 sekunnin odottelun jälkeen. Toki järjestelmässä pitää olla joku karenssiaika, että jos valot ovat juuri olleet vihreinä jalankulkijoille, niin siinä tapauksessa uudelleen nappia painanut joutuisi odottelemaan hetken, mutta silloinkin vaikka jollain äänisignaalilla tms. voisi indikoida nappia painaneelle, että pyyntö on rekisteröity.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Nappiliikennevalot nopeammiksi'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.08:19:42')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["Vuokko"],\
#      content=u'Ongelma on se, että tällä tavalla keinotekoisesti pidennettäisiin pyöräilyreittejä. Mitä jos kotikadulta pääsisi ajamaan vain yhteen suuntaan? Jos maitokauppa tai koulu on vastakkaisessa suunnassa parin korttelin päässä samalla kadulla, sääntöä vastaan rikkomiseen olisi turhan suuri kiusaus ja rikkeet olisivat yleisiä nimenomaan pyörillä. Entäpä kaksisuuntainen pyöräily ja yksisuuntainen autoilu?'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["apoikola"],\
#      content=u'Yksisuuntaisilla teillä autoilijoilla on tapana ajaa lujempaa, kuin kaksisuuntaisilla, elleiu tätä erityisesti rajoiteta.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Helsingin kaikki kadut pääväyliä lukuunottamatta voitaisiin muuttaa yksisuuntaisiksi, niin että joka toinen katu kulkisi eri suuntiin. Kaikilla tällaisilla kaduilla olisi siis yksi autokaista ja pyöräkaista samaan suuntaan. Nykyisellä katuleveydellä rinnalle mahtuisi vielä vinopysäköinti ja parkkipaikatkaan eivät vähenisi. Kaksisuuntaisilla pääväylillä olisi pyörätiet molemmin puolin jalkakäytävien rinnalla.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Helsingin kadut yksisuuntaisiksi ja pyöräkaista joka kadulle'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.10:44:59')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Fredrikinkatu on keskustassa tärkeä väylä. Fredalle - ja muillekin kaksikaistaisille, yksisuuntaisille kaduille - voitaisiin hyvin rakentaa kaksisuuntainen pyöräkaista.  \
#\
#Lisäksi mukulakiviosuus on todella kenkkumainen ajaa pyörällä, etenkin kun saa samalla pelätä ratikkakiskoilla liukastumista.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Fredan ongelmat'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-20.05:28:57')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#users["aetelaah"] = db.user.create(username="aetelaah", screenname="aetelaah", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["aetelaah"],\
#      content=u'on ihan välttämätön! Autojen seassa ei voi ajaa tuollaisella paikalla ainakaan ison fillarilla kuljetettavan lastin kanssa.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Kaisaniemenkadulle pyöräilykaista'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-22.14:03:44')
##db.issue.set(id, creator=users['aetelaah'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Miten tämä olisi ollut vältettävissä?\
#\
#Jalankulkija kuoli polkupyöräturmassa Helsingissä\
#\
#http://www.hs.fi/kaupunki/artikkeli/Jalankulkija+kuoli+polkupy%C3%B6r%C3%A4turmassa+Helsingiss%C3%A4/1135240383887'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["apoikola"],\
#      content=u'Sähköpostikirjeenvaihto aiheesta tuotti seuraavan tarkennuksen:\
#\
#sovun säilymistä jalankulkijoiden ja pyöräilijöiden välillä esitäisi myöskin se, että myös pyöräilijät kunnioittaisivat pelkästään jalankulkijoille tarkoitettuja väyliä, samoin vauhdin hidastaminen mäessä jalankulkijoiden kanssa yhteisillä väylillä olisi suotavaa kummankin ryhmän turvallisuuden vuoksi.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["apoikola"],\
#      content=u'On kurjaa, kun kaksi ekologisesti toimivaa ryhmää pyöräilijät ja jalankulkijat ovat keskenään tukkanuottasilla ja kovin sanankääntein syyllistämässä toisiaan. Perussyyttet ovat seuraavat:\
#\
#-Pyöräilijät kaahaavat liian lujaa ja läheltä \
#\
#-Jalankulkijat eivät kunnioita pyöräteitä, vaan hoopoilevat miten sattuu.\
#\
#Autoilijat puolustavat saarekkeitaan sitkeästi, meidän kahden ryhmän kannattaisi säilyttää vähintäänkin linnarauha keskenämme niin, että autoväki saataisiin itsensä kokoiselle tontille yhteistuumin.\
#\
#Pyöräilijöiden pitää vahvempana osapuolena ottaa huomioon jalankulkijat, siinäkin tapauksessa, että jalankulkija seisoisi keskellä pyörätietä. Jalankulkijoiden taas pitää ymmärtää, että pyörätie ei ole osa jalkakäytävää (vaikka liikennesuunnittelu ei tätä selväksi tee), vaan paremmin rinnastettavissa ajorataan. Jos jompi kumpi rikkoo näitä sääntöjä pitäisi löytyä sitä yhteistä kevyen liikenteen ymmärrystä, että asiasta huomautetaan sadattelematta.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräilijät ja jalankulkijat sopuun'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-21.10:15:20')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Pyöräilijöille pitää saada pyöräkaistat katkonaisten pyöräteiden tai ylikuormitettujen jalkakäytävien sijaan. Näin autoilijatkin tottuvat kaksipyöräisiin, ja osaavat ottaa fillaristit huomioon. Nykyiset pyörätiet ovat valitettavasti lähinnä huoltoautojen parkkipaikkoja tai koiranulkoilutusalueita.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräkaistat katkonaisten pyöräteiden sijaan'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:31:55')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Otsikko kertoo kaiken, on harmillista, että ainoa ydinkeskustan pyöräkaista on päällystetty erittäin hostiileilla historiallisilla mukuloilla.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Mukulakivet pois Unioninkadun pyöräkaistoilta'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-22.18:20:21')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Kampin keskuksen Fredrikinkadun puoleiselle sisäänkäynnille tarvitsisi muutaman pyörän vetävän pyörätelineen, sillä nykyisin siinä seisoo aina noin 5 pyörää ravintola Bruuverin edessä. Annankadun päässä olevan sisäänkäynnin luokse on hiljattain ilmestynyt erittäin hyvät pyörätelineet, jotka ovat myös erittäin suosittuja.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyörätelineet Kampin keskuksen Fredan sisäänkäynnille'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.07:57:12')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Pyöräilen ekaluokkaisen poikani kanssa koulusta kotiin päivittäin ja yleensä mukana kulkevat myös 4-vuotias omalla pyörällään ja 1-vuotias kyydissäni. Kehä I:n vieressä kulkevalla kevyen liikenteen väylällä mopoilu on sallittu Pakilan yläasteelle saakka. Mopoja on paljon, ja usein mopoilijoiden matka jatkuu myös ala-asteelle asti (vaikka tämä tosiaan on erikseen kielletty). \
#Kyseinen kevyen liikenteen reitti on turvallisin koulutie meille. \
#Miksei mopoja voi ohjata viereisille teille, jotka Pakilassa ovat varsin hiljaisia? Näin pienemmät saisivat kulkea rauhassa pyörillään tai kävellen, sitten kun vanhemmat uskaltavat päästää yksin kulkemaan.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'mopot pois Pakilan pyöräteiltä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.10:46:09')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Asennekampanjointi ei aina ole välttämättä kovin tehokasta, mutta jos poliisi ja pysäköinninvalvojat todella rupeaisivat sakottamaan pyörätielle pysäköiviä saattaisi toiminta muuttua. Jalankulkijoiden ja pyöräilijöiden välinen konflikti taas juontaa juurensa huonosta jalkapyörätörmäyskaistoja suosivasta liikennesuunnittelusta. Mielstäni paras ratkaisu olisi tähän pyöräkaistat.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Jalankulkijat eivät kunnioita pyöräkaistoja, eivätkä autotkaan, jotka pysäköivät niille varsin huolettomasti. Kun sen sijaan ajaa jalkakäytävällä vaikka kymmenenkin metriä saadakseen ajokkinsa parkkiin saajalankulkijoilta mitä epämiellyttävämpiä ja vihamielisempiä kommentteja. Autot kiilaavat ajoradalla ajavan pyöräilijän vaarallisesti. Pyöräilijä on todellista tienkäyttäjien paarialuokkaa! Tähän voitaisiin saada asennemuutos kampanjoinnilla ja pyörällä liikkuvien oikeuksien ja olojen parantamisella.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräilyn nostaminen pois lainsuojattoman asemasta'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-20.05:36:40')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#users["Jemina"] = db.user.create(username="Jemina", screenname="Jemina", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["Jemina"],\
#      content=u'Helsingin jalkakäytävät ovat monessa paikassa epäkäytännöllisen suuret (esim. Mechelininkadulla). Otetaan mallia vaikka Saksasta tai Itävallasta: pienemmät jalkakäytävät ja pyöräkaista jalkakäytävästä erilleen autokaistan viereen kummallekin puolelle tietä. Kun pyörätie kulkisi ajoradan vieressä kaikilla suurilla kaduilla, edistettäisiin mm. sitä, että pyörätie ei vain yhtäkkiä loppuisi (vrt. esim. Mannerheimintie).'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Jalkakäytävistä puolet pois, pyöräkaista autokaistan viereen'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-05.10:06:53')
##db.issue.set(id, creator=users['Jemina'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Kunnallisia tai työnantajien kustantamia tai henk koht kakkospyöriä asemien ja työpaikan/kodin liityntäpyöräksi, niin ei tarvitse raahat pyörää junassa kun sitä tarvitsee määränpäässä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'liityntäpyörät'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.19:31:55')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#users["Imppu"] = db.user.create(username="Imppu", screenname="Imppu", organisation=['Kaupunkifillari uservoice user'], address="invalid@email"+ str(usercounter) +".no")
#usercounter += 1
#id = msg.create(author=users["Imppu"],\
#      content=u'Bulevardin pyörätie on varmaankin monille keskustan pyöräilijöille tuttu, kuten myös sen ongelmat - ohittaminen mahdotonta, raitiovaunuihin ja busseihin hyökkäävät jalankulkijat, autot parkissa keskellä pyöräkaistaa (muitakin autoja kuin se kukkaliikkeen citymaasturi ;-).\
#Kaiken huippuna on kuitenkin pyörätien yläpäässä oleva yhteys Esplanadin puistoon..\
#Erottajan kulmalla syttyy pyöräilijälle vihreä ja samalla vihreällä pääsee Esplanadin puiston etukulmaan, mutta lähes joka kerta pyörätien yli tunkee myös Bulevardilta Etelä-Esplanadille ajava auto!\
#Autot voivat ajaa Bulevardilta joko pohjoisen suuntaan Mannerheimintielle tai etelän suuntaan Erottajalle, mutta Esplanadille on yhteys Yrjönkadun ja Diananpuiston kautta, ei suinkaan suoraan vihreällä olevan pyörätien yli.\
#Aikuinen ehtii lähes aina yli kyseisen pyörätien ennen kuin se tai ne autot, mutta jos mukana on lapsi tai pyöräilijöitä useampia, muuttuu tilanne siten, että viimeisen ollessa pyörätiellä autoilija tunkee samaan kohtaan, samanaikaisesti kiertäen katukiven reunaa sekä varoen yhtä aikaa kahteen suuntaan kulkevia ratikoita ja Erottajalta alas tulevaa autovirtaa. Odotan kauhulla, koska tulee ensimmäinen uutinen, että pyöräilijä on jäänyt risteyksessä ajavan auton alle.\
#Tästä on ilmoitettu kaupunkisuunnitteluvirastoon sekä poliisille, mutta toistaiseksi ei ole mitään tapahtunut.\
#Ehdotankin, että pyörätien eteen Mannerheimintien nurkan puolelle rakennetaan puomi, joka laskeutuu alas siksi aikaa, kun pyörätiellä on vihreä valo. Puomi on aika järeä ratkaisu, mutta vaihtoehtona voi olla joko pyöräilijän kuolema tai vakava loukkaantuminen, jolloin puomi voisi sittenkin kuulostaa ihan järkevältä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Autojen ajo Bulevardilta Etelä-Esplanadille estettävä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-25.13:32:57')
##db.issue.set(id, creator=users['Imppu'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Haahuilevat, 10km nopeusrajoituksia ja räpättimiä vaativat jalankulkijat tulee sakon uhalla poistaa pyöräteiltä! Kyllä minä pyörällä väistän hitaampia, mutta pysyisivät omalla puolellaan, jos kerran nopeammat pelottavat. Pyöräilijät eivät saa ajaa jalkakäytävällä (no, eipä niitä pyöräteitäkään juuri ole), joten jalankulkijat pois tukkimasta niitä vähiäkin pyöräteitä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Jalankulkijat sakon uhalla pois pyörätieltä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-22.08:49:33')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["toma"],\
#      content=u'Voisi myös olla (kamera) valvontaa. Ystäväni pyörä varastettiin Elielin pyöräparkista. Varmaan on monen muunkin.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Lenkit joilla pyörän lukosta kiinni telineeseen, ovat hyviä mutta ne on usein rikki. Plussaa olisivat myös katetut pyörätelineet. Vanhat pyöränromut pitäisi myös aika ajoin poistaa, telineet eivät ole pitkäaikaissäilytykseen tarkoitettuja.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Juna-asemien säilytyksen parantaminen'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-22.09:35:25')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Uusia leveitä pyöräteitä ja parkkeja, citypyöriä! \
#Koulutusta liikennesäännöistä, selkeät viitat, ja esim pyörätiet voisi olla punaisella merkitty ja joka paikassa omilla liikennevaloilla kuten kööpenhaminassa.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'pyöräteitä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-21.07:49:16')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Pyöräilijät halutaan siivota pois autojen tieltä, ja helppo tapa siihen on merkitä viereinen jalkakäytävä yhdistetyksi kevyen liikenteen väyläksi. Siellä pyöräilijät joutuvat taistelemaan elintilastaan jalankulkijoiden, lastenrattaiden, rollaattoreiden, koirien, lasten ja seisoskelijoiden kiusana. Usein nämä "pyörätiet" ovat pyöräilyn pääväyliä kaupungissa. Samalla logiikalla Mannerheimintie voitaisiin laittaa kulkemaan päiväkodin pihan läpi. Pyöräilijöiden ei pidä suostua siihen, että heidät pakotetaan käyttökelvottomille reiteille. Kelvolliset väylät kuuluvat yhtä lailla pyöräilijöille.\
#\
#Ratkaisu: Yhdistetyllä kevyen liikenteen väylällä pyöräily vapaaehtoiseksi. Siellä saisivat ajaa ne, jotka eivät uskalla ajaa autojen seassa. Muut saavat pyöräillä laillisesti ajokaistalla.\
#\
#Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Yhdistetty kevyen liikenteen väylä ei aina sovellu ajamiseen'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-10.07:47:48')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Liikennemerkit ovat Salomonkadulla kadulla väärin koska sen kuuluisi olla myös pyöräilytie Runeberginkadulta Mannerheimintielle. Rakennusvirasto on tiennyt ainakin parin kuukauden ajan että merkit ovat virheelliset, ainakin YTV on ollut sinne päin yhteydessä. Miksi niitä oikeita merkkejä ei ole siis vieläkään siellä? On aika ikävää kun jalankulkijat luulee että pyöräilee jalankulkualuella kun pyöräilee siitä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Liikennemerkit Salomonkadulle'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-09.12:40:49')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Helsingissä on katuja, jotka pyöräilijät kokevat niin pelottaviksi, että useimmat eivät uskalla niillä ajaa. Jotkut polkevat henkensä uhalla autojen seassa, toiset taas sakon uhalla jalkakäytävillä. Ei ole hyväksyttävää, että pyöräilijä joutuu pelkäämään henkensä puolesta siellä, missä hänen liikennesääntöjen mukaan pitäisi ajaa. Hämeentie, Mechelininkatu, Mäkelänkatu ja Tukholmankatu ovat myös pyöräilijöiden pääreittejä: niiden varrella asuu ja työskentelee tuhansia pyöräilijöitä. Pyöräilyn tulee olla mahdollista ja turvallista kaikilla kaupungin kaduilla. Painosta päättäjiä, lähetä viestejä. Osallistu kriittisille pyöräretkille ja koe ilo polkea turvallisesti näilläkin kaduilla.\
#\
#Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Ajotiellä ei uskalla pyöräillä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-10.07:54:55')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Rautateiden varsilla on mukavasti pyöräteitä. Matkan teon kannalta vauhti hiipuu ikävästi huonon suunnittelun takia. Mm Ilmalassa on hyväksi koetut reitit menty pilaamaan järjettömällä kaavoituksella.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'radanvarret vapaiksi'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-22.14:57:59')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Kaupunkikuvaan ja ihmisten arkeen vaikuttaa ikävimmin huonoksi osoittautuvat kaavoituspäätökset. Jotta "accountability" säilyisi pitkän aikavälinkin päätöksissä ehdottaisin tietokantaa, jossa  urpoimmat kaavoituspäätökset tehneet byrokraatit ja edustajat pantaisiin omalla nimellään ja naamallaan vastaamaan teoistaan.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Kaavoittajien mustalista'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-22.15:02:09')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Joissain paikoissa on liikennevaloja, jotka voisivat pääsääntöisesti vilkkua keltaisena. Jalankulkunappi voisi olla sitä varten, että jos on paljon autoja eikä pääse muuten yli, niin voisi painaa nappia jolloin valot toimisivat normaalisti'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Nappivalot keltaiselle'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.16:28:02')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["Vuokko"],\
#      content=u'Kannatan tätä tasa-arvosyistä: autoliikenteen ei pitäisi olla etuoikeutetussa asemassa, joten sille ei pitäisi osoittaa huomattavasti enempää rahoja kuin joukko- tai kevyelle liikenteelle. Investointeja pitäisi tehdä ennen kaikkea sinne, missä se on suhteessa edullista ja hyödyttää mahdollisimman monia. Jalkakäytäville ja pyöräteille pääsy on lähes kaikilla, autoteille vain autoilijoilla.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["apoikola"],\
#      content=u'Eli siis meinataanko tällä sitä, että jos suojatie korvataan liikenneturvallisuussyistä kevyen liikenteen alikululla olisi rahat otettava autoliikenteen potista, koska autoliikenne aiheuttaa liikenneturvallisuusriskin? Tai ehdotushan on, ettei olisi erillisiä potteja lainkaan.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Helsingin liikennemäärärahoja ei pitäisi eritellä kevyeeseen ja muuhun liikenteeseen. Tästä on seurannut se, että pyöräteihin ja alikulkutunneleihin ei ole ollut riittävästi varaa, vaikka ne tehdään pyöräilyn erottamiseksi muusta liikenteestä, joka on vaarallisempaa kuin pyöräily. Periaatteen kuitenkin pitäisi olla, että aiheuttaja maksaa.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Liikennemäärärahoja ei pidä eritellä kevyeeseen ja muuhun'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:41:49')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Pyöräteillä polkee sulassa sovussa ajamista harjoittelevia lapsia, vastuullisen rauhallisesti ajavia naisia,  kaltaisiani vauhdikkaita työmatkailijoita, vielä vauhdikkaampia pyöräilyn harrastajia, koululaisia ja monenlaisia muita pyöräilijöitä. Tärkeimmät pyöräilyoloja parantavat aloitteet ovat sellaisia, että niistä hyötyvät kaikki pyöräilijäryhmät. Helsingissä mielestäni etusijalle nousee pyöräilyreittien hoito.\
# \
#Helsinki tarvitsee pyöräteiden hoitoon laatustandardin, jonka noudattamista myös valvotaan. Yhtäältä on huolehdittava siitä, että pyörätiet pidetään talvella aurattuina ja että hiekoitushiekat harjataan keväällä ripeästi pois. Toisaalta – ja tämä onkin isompi asia valvottavaksi – pyöräteille ei katutöitten tms. vuoksi saa jäädä kuoppia, terävää sepeliä tai muita pyöriä hidastavia esteitä. Nyt pyörätiet tuntuvat joskus kunnallisilta kuoppavarastoilta: kun jollekin tietyömaalle kaivettu kuoppa käy tarpeettomaksi, se siirretään sopivaan paikkaan keskelle pyörätietä.\
# \
#Kun pyörätiet saadaan muutettua esteradoista ajoväyliksi, kaikenlaisten pyöräilijöiden liikkuminen tulee sekä mukavammaksi että turvallisemmaksi. Kunnossapitostandardi ei sitä paitsi edellytä juurikaan ylimääräistä rahaa.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Laatustandardi pyöräteiden hoitoon'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.15:02:43')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Nyt en ihan ymmärtänyt, mitä ehdotettiin?'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Helsingin kadut pääväyliä l'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-19.10:38:26')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Ehdotin vain tätä yhtä tiyttyä paikkaa, kun se tuli ensimmäisenä mieleen. Kun ehdotuksia viedään eteenpäin kaupunkisuunnitteluvirstoon on parempi, että kaikki toiveet on mahdollisimman tarkkaan spesifioitu.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["tulenheimo"],\
#      content=u'Ryhmittymisalueita joka paikkaan, missä niitä tarvitaan! Liikennevalojen yhteydessä sekä vasemmalle kääntyvät pyöräilijät että ajotieltä oikealle erillään jatkuvalle pyörätielle kääntyvät pyöräilijät ovat vaarassa, koska autot eivät jätä tarpeeksi tilaa oikealle puolelle auton ja kadun reunan väliin.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["anonymous"],\
#      content=u'Tänään Petri Sipilä esitteli valokuvia polkupyörille tarkoitetuista ryhmittymisalueista, joita liikennevaloristeyksissä on esim. Ruotsissa ja Englannissa. Eräs oivallinen paikka moiselle ryhmittymisalueelle olisi Telakkakadulla Hietalahden torin suuntaan mentäessä ennen Koffin alittavan tunnelin suuta.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Ryhmittymisalue Telakkakadulle'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-09.12:06:06')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["anonymous"],\
#      content=u'Ajellessa pyörätietä Vanhankaupungin lahdelta Viikintietä pitkin kohti Viikkiä on vasemmalle kääntyvä tie lumikaatopaikalle, jota ennen löytyy tienviitta "Varokaa kääntyviä autoja". T-risteys on kuitenkin etuoikeutettu pyöräilijöille, sillä se on jopa varustettu stopilla ja pyöräilijöiden väistämis -merkillä. Eikö ennemminkin pitäisi laittaa autoteille kylttejä "Varokaa suoraan ajavia pyöräilijöitä"?'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Ylimääräinen liikennemerkki (?!)'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-09-23.19:32:12')
##db.issue.set(id, creator=users['anonymous'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Päättyvän tien merkki ei läheskään aina tarkoita, ettei pyörällä pääsisi jatkamaan. Pahinta on, että tällaisia merkkejä on sijoiteltu pyöräilyn pääväylille. Pyöräilijä joutuu arvailemaan. Esimerkiksi Maamonlahdentien merkistä Lauttasaaressa on ilmoitettu kaupungin edustajille moneen kertaan, mutta merkkiä ei ole vaihdettu. Ilmoita virheellisistä merkeistä YTV:n palautelomakkeella tai kerro niistä HePolle. Pyrimme seuraamaan niiden korjaamista.\
#\
#Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Liikennemerkit unohtavat pyöräilijät'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-10.07:49:01')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Onko nämä kaikki nyt nimenomaan pyöräteitä, mitä tarkoitat, vai mahtuisiko mukaan muutama kunnon pyöräkaistakin?'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Helsinkiin on rakennettava kattava pyörätieverkosto. Polkupyöräily on liikennevaihtoehtona nostettava auton rinnalle. Alkuvaiheessa on rakennettava yhtenäiset, selkeästi merkityt, turvalliset ja ympärivuotisesti kunnossapidetyt pyörätiet Hämeentien, Lauttasaarentien, Mannerheimintien, Tukholmankadun varrelle sekä Pasilan, Vallilan ja ydinkeskustan alueelle. Pyörätiet on merkittävä kirkkaan punaisella tien laidalle.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Helsinkiin on rakennettava kattava pyörätieverkosto'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.12:41:45')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Helsingissä on yksisuuntaisia katuja paitsi keskustassa, myös Kalliossa, Vallilassa ja Munkkiniemessä. Monet niistä ovat hyvin hiljaisia, mutta pyörällä ei kuitenkaan saa ajaa vastasuuntaan. On kierrettävä autojen reittejä tai talutettava jalkakäytävällä.\
#\
#Kulosaaren Hopeasalmentie on yksisuuntainen. Hämmästyttävää on se, että tie on merkitty pyörämatkailureitiksi, ja YTV:n kevyen liikenteen reittiopas ohjaa tälle tielle myös kiellettyyn ajosuuntaan.\
#\
#Kaksisuuntainen pyöräily voidaan tehdä mahdolliseksi erilaisilla ratkaisuilla, jos niin halutaan. Tukholmassa ja monissa muissa eurooppalaisissa kaupungeissa näin on tehty.\
#\
#Idea on kopioitu Helsingin Polkupyöräilijöiden sivulta: http://www.hepo.fi/index.php?sivu=ongelmapaikat'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Yksisuuntaiset kadut haittaavat pyöräilyä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-10.07:55:42')
##db.issue.set(id, creator=users['apoikola'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Pyöräreitit pitää merkitä liikennemerkein paremmin kuin nykyään. Useinkaan kevyen liikenteen väylälle tullessa ei tiedä, että onkohan tämä pyörätie, kulkevatkohan kävelijät ja pyöräilijät samaa puolta vai onko tässä kaistat. Pyörätien voi katkaista rakennustyömaa ja opastus uudelle reitille puuttuu.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräreitit pitää merkitä liikennemerkein paremmin'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:34:30')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Työmatkapyöräilyä tulisi kannustaa yritysten pyörien muodossa eli luontaisetuna. Tähän liittyy katetut pyörätelineet. Pyörätelineen katos ei olisi suuri investointi.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Työmatkapyöräilyä tulisi kannustaa luontaisetuna'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:36:28')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Unelmakaupungissani joka paikkaan pääse pyörällä. Aloitteestamme Maankäytön ja asumisen ohjelmaan kirjattiin: ?Asemakaavoihin voidaan lisätä määräykset tonttikohtaisista polkupyöräpaikkojen vähimmäismääristä.? Tämä kirjaus on toteutettava. Pyöräilijän tarpeet on otettava huomioon rakentamisessa.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Unelmakaupungissani joka paikkaan pääse pyörällä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:37:56')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Tavoite pyöräilyn tuplaamiseksi on vihdoin toteutettava rakentamalla pyöräilijöille turvalliset, sekä jalankulkijoista että autoista erotetut väylät: pyöräkaistat. Tämä tehdään merkitsemällä väylä kaistaviivan lisäksi huomiovärillä, kuvioinnilla, katumateriaalilla ja korkeusero reunakivellä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Tavoite pyöräilyn tuplaamiseksi'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-02.15:48:03')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Pyöräteitä voi edullisesti luoda liikennemerkeillä ja kaistamaalilla, niin että joka kaupunginosasta pääsisi yli 12-vuotiaat edes laillisesti liikkeelle joutumatta suoraan autojen sekaan. Tämä rohkaisee perheitä tarttumaan pyörään myös "kivikaupungin" alueella.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräteitä edullisesti liikennemerkeillä ja kaistamaalilla'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:43:32')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["apoikola"],\
#      content=u'Huoltoasemilla yleensä on saatavilla adapteri, jolla pyöränkin renkaat saa täyteen. Voisihan näitä muuallakin olla, muistan aikanaan, kun kotikadullani ollut pyöräliike tarjosi paineilmaa postiluukusta tulevalla letkulla halukkaille ohikulkijoille.'.encode('utf-8'))
#message_ids.append (str(id))
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Asemille tai kauppojen yhteyteen tai kaupungin rakennuksiin tai muihin sopiviin paikkoihin tarvitaan pummppuasemia pyörän kumin pumppaamiseksi. Onko jo saatavilla vuokrattavia peräkärryjä pyörään liitettäväksi?'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Asemille tai kauppojen yhteyteen pumppuasemia'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:45:08')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Helsingin pyöräilyverkon tulee olla kattava. Pyöräily töihin ja kouluun ei houkuta, jos välillä joutuu koukkaamaan autojen sekaan. Pyörätiet tulee valaista riittävästi. Jatkuvat tietyömaat ja pyörätielle väärin parkkeeratut autot haittaavat kulkua, tähän voisi puuttua ainakin autojen osalta sakottamalla (ja nostamalla pysäköintivirhemaksua). Työmatkapyöräilyyn voitaisiin kohdistaa markkinointikampanja, esimerkkinä Amsterdam tai Kööpenhamina.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Helsingin pyöräilyverkon tulee olla kattava'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:51:57')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Vähemmän autoja, enemmän turvallisia ja selkeästi merkittyjä pyöräteitä. Aamuisin on mahdotonta ylittää Pakilantie matkalla kouluun ja päiväkotiin. Alikulkutunnelissa saavat ajaa myös mopot, joita väistelen kahden pyöräilevän lapseni kanssa. Kolmas kiljuu kyydissä, kun mopot innostavat.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Enemmän turvallisia ja selkeästi merkittyjä pyöräteitä'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.14:56:04')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Pyöräreitit vapaaksi autoista pysäköinnin valvontaa tehostamalla. Helsingin villistä pysäköinnistä kärsivät niin pyöräilijät kuin jalankulkijatkin, eikä niin pientä esinettä ole, etteikö sen "lastaamiseksi" saisi pysäköidä jalkakäytävälle. Lisäksi poistaisin mopot pyöräteiltä ennen kuin sattuu pahasti. Asiat liittyvät toisiinsa siten, että molemmissa tapauksissa moottoriajoneuvo on sille kuulumattomalla paikalla.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräreitit vapaaksi autoista pysäköintiä valvomalla'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.15:08:10')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Haluan, että pyörien kuljettaminen joukkoliikennevälineissä olisi maksutonta. Metrossa näin jo on, mutta maksuttomuus tulisi laajentaa varsinkin juniin. Metroissa ja junissa tulisi olla pyörille merkatut paikat, jotta kuljetukselle olisi tilaa. Myös ratikka- ja bussikuljettamista olisi selvitettävä.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyörien kuljettaminen joukkoliikennevälineissä maksuttomaksi'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-01.15:11:35')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Erilliset pyöräkaistat ja oikeus ajaa myös ajoradalla. Kevyen liikenteen väylät ovat monesti heikkolaatuisia ja jopa turvattomia. Lisää ajatuksia Kesäfillari-blogini entryssä http://fillari.blogspot.com/2008/08/poliitikko-keksi-pyr.html" Poliitikko, keksi pyörä!'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Erilliset pyöräkaistat ja oikeus ajaa myös ajoradalla'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-03.13:28:39')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Pyörille omat kaistat autokaistojen reunaan, ei jalankulkijoiden sekaan.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyörille omat kaistat autokaistojen reunaan'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-03.14:36:19')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Yhtenäisiä pyöräilykaistoja tarvitaan lisää, ettei tien puolta tarvitsisi jatkuvasti vaihtaa. Esimerkiksi Kööpenhaminassa pyörällä pystyy helposti liikkumaan ihan ydinkeskustassakin. Pyöräilyyn kannattaa panostaa, koska se on ympäristöystävällistä ja hyvä tapa saada liikuntaa ja vireämpi mieli toimistotyöläisille.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Yhtenäisiä pyöräilykaistoja tarvitaan lisää'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-13.17:59:02')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'I innerstaden borde gatuparkering ersättas med cykelfiler på i medeltal varannan gata.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'I innerstaden borde gatuparkering ersättas med cykelfiler'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-13.18:03:17')
##db.issue.set(id, creator=users['fillariehdokkaat'])
#message_ids = []
#id = msg.create(author=users["fillariehdokkaat"],\
#      content=u'Pyöräteitä lisää nykyiseen tahtiin, keskustaan myös pyöräkaistoja (mm. Mansku pohjoiseen päin). Tulevaisuudessa poikittaisliikenteeseen ja lähiöihin suuntautuviin pikaratikoihin pyörienkuljetustilat.'.encode('utf-8'))
#message_ids.append (str(id))
#id=db.issue.create(title=u'Pyöräteitä lisää, keskustaan myös pyöräkaistoja'.encode('utf-8'),\
#                   status='2', priority='3', messages=message_ids, score="0" )
#
##db.issue.set(id, creation='2008-10-13.18:08:02')
##db.issue.set(id, creator=users['fillariehdokkaat'])
