old-fillarikanava
=================

Vanhan Fillarikanavan viimeisimmät backupit löytyvät DropBoxista. Huom. muitakin kantoja (esim. mediawiki) ja repoja (doc) on tallessa.

https://dl.dropbox.com/u/33161960/hila/hila-tietokannat-ja-svn.tar.gz

Dataa, eli käyttäjien aloittamia viestiketjuja näyttäisi olevan 1477 kpl, eka tullut 2009-11-11 10:14:06 ja
viimeinen 2011-11-23 15:33:42.

Alla ohjeistus, miten datan saa käyttöön.





##README 7.9.2012


###1. SVN

SVN-repon ja checkoutit saa pelaamaan alla olevilla esimerkkikomennoilla, kunhan vain Subversion on asennettu.


```
$ mkdir -p /home/janne/svn/repos/hila
$ svnadmin create /home/janne/svn/repos/hila
$ svnadmin load /home/janne/svn/repos/hila < backup.svn

```

Sitten esim.:

```
$ mkdir -p /home/janne/projects/hila
$ cd /home/janne/projects/hila
$ svn co file:///home/janne/svn/repos/hila/hila_webapp/trunk hila_webapp

```
Tuon hila_webapp:in lisäksi löytyy näitä:
dev/
graphics/
hila_media/
roundup-getnodes/
xapian-components

Repoa voi selailla komennolla:


```
$ svn list file:///home/janne/svn/repos/hila

```

###2. TIETOKANNAT

Asenna MySQL. Sitten rootina sisään mysql-terminaaliin ja:

mysql> create database hila_roundup default character set utf8;
mysql> grant all privileges on hila_roundup.* to 'hila_roundup'@'localhost' identified by 'hila_roundup';
mysql> flush privileges;

Sitten komentoriviltä (ei mysql-terminaalista!) vaikka normikäyttäjänä:


```
$ mysql -u hila_roundup -p < hila_roundup_2011-12-25_04h25m.Sunday.sql  	<-- ANNA SALASANA 'hila_roundup'

```

Sitten voikin mennä tsekkaamaan kantaa:

```
$ mysql -u hila_roundup -p hila_roundup         <-- ANNA SALASANA 'hila_roundup'

```

```
mysql> show tables;
+------------------------+
| Tables_in_hila_roundup |
+------------------------+
| __textids              |
| __words                |
| _file                  |
| _issue                 |
| _keyword               |
| _language              |
| _msg                   |
| _organisation          |
| _place                 |
| _priority              |
| _query                 |
| _status                |
| _user                  |
| _vote                  |
| file__journal          |
| ids                    |
| issue__journal         |
| issue_files            |
| issue_keyword          |
| issue_messages         |
| issue_nosy             |
| issue_places           |
| issue_superseder       |
| issue_votes            |
| keyword__journal       |
| language__journal      |
| msg__journal           |
| msg_files              |
| msg_places             |
| msg_recipients         |
| msg_votes              |
| organisation__journal  |
| otks                   |
| place__journal         |
| priority__journal      |
| query__journal         |
| schema                 |
| sessions               |
| status__journal        |
| user__journal          |
| user_organisation      |
| user_queries           |
| vote__journal          |
+------------------------+
43 rows in set (0.00 sec)

```


```
mysql> select id, _title, _creation from _issue limit 10;
+----+-----------------------------------------------------------------------+---------------------+
| id | _title                                                                | _creation           |
+----+-----------------------------------------------------------------------+---------------------+
|  1 | PyÃ¶rÃ¤ilykaista HÃ¤meentielle Kurvista Hakaniemeen                   | 2009-06-12 00:46:29 |
|  2 | Reunakorokkeet pois suojateiden kohdalta                              | 2009-06-12 00:46:30 |
|  3 | Keskustan pyÃ¶rÃ¤tieverkko yhtenÃ¤isiksi                              | 2009-06-12 00:46:30 |
|  4 | PyÃ¶rÃ¤teiden viitoitus                                               | 2009-06-12 00:46:30 |
|  5 | Napit liikennevaloista kokonaan pois                                  | 2009-06-12 00:46:30 |
|  6 | BussipysÃ¤kkien mainokset sivuseinistÃ¤ takaseiniin                   | 2009-06-12 00:46:30 |
|  7 | PyÃ¶rÃ¤tie Tukholmankadulle                                           | 2009-06-12 00:46:30 |
|  8 | Pumppu/pyÃ¶rÃ¤telineyhdistelmiÃ¤ julkisille paikoille                 | 2009-06-12 00:46:30 |
|  9 | Koulutusta lastinkuljettajille pyÃ¶rÃ¤ilijÃ¶iden huomioimiseksi       | 2009-06-12 00:46:30 |
| 10 | Mechelininkadulle pyÃ¶rÃ¤kaista                                       | 2009-06-12 00:46:30 |
+----+-----------------------------------------------------------------------+---------------------+
10 rows in set (0.00 sec)

```

Ja niin edelleen...

Ja merkistöä voi koittaa säätä komennoilla:


```
mysql> set names latin1;

```

tai


```
mysql> set names utf8;

```

Voi olla, että meillä on merkistöongelmia ollut kannan tai 
tallentamisen kanssa, en oo ihan varma. Mutta noita nyt voi korjata 
konvertoimalla ym.

@jnur


