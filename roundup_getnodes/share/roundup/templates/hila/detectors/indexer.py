# -*- coding: UTF-8 -*-

from roundup import roundupdb, hyperdb
import logging
import random
import re,os
import math
import simplejson

try:
    import xapian
    xapian_avail = True
except ImportError:
    logging.warning('Failed to import xapian, search disabled')
    xapian_avail = False
    
    
xapiandb = None
    
XAPIAN_ISSUE_SCORE_VALUE = 1
XAPIAN_LATITUDE_VALUE = 4
XAPIAN_LONGITUDE_VALUE = 3

XAPIAN_X_COORD_FIELD=3
XAPIAN_Y_COORD_FIELD=4
XAPIAN_POSTAL_FIELD=5
XAPIAN_CREATED_FIELD=6
XAPIAN_MODIFIED_FIELD=7
XAPIAN_ARTIST_FIELD=8
XAPIAN_HAS_PICTURE_FIELD=9
XAPIAN_DATATYPE_FIELD=10
XAPIAN_ID_FIELD=11
XAPIAN_PARENT_ISSUE_FIELD=12
XAPIAN_PARENT_MESSAGE_FIELD=13
XAPIAN_STATUS_FIELD=14


XAPIAN_INDEXING_TYPE_PLACE=3.0
XAPIAN_INDEXING_TYPE_ISSUE=1.0
XAPIAN_INDEXING_TYPE_MESSAGE=2.0


MAX_PROB_TERM_LENGTH = 64

XAP_VOTE_FIELD_ID = 5
XAP_STOPWORDS=[u'juu', u'ei', u'myös', u'eli', u'eikä', u'myöskään',
           u'ilman', u'sekä', u'että', u'hän', u'minä', u'mä', u'se', u'sen',
           u'mun']
XAP_OFFSET_KLUDGER = 100


def p_alnum(c):
    return (c in string.ascii_letters or c in string.digits)

def p_notalnum(c):
    return not p_alnum(c)

def p_notplusminus(c):
    return c != '+' and c != '-'

def find_p(string, start, predicate):
    while start<len(string) and not predicate(string[start]):
        start += 1
    return start

def is_stopword( word):
    return word in XAP_STOPWORDS

def to_lower_case(word):
    word = re.sub('Ä', 'ä', word)
    word = re.sub('Ö', 'ö', word)
    word = re.sub('Å', 'å', word)
    word = re.sub('Ü', 'ü', word)
    word = re.sub('Á', 'á', word)
    word = re.sub('À', 'à', word)
    word = re.sub('É', 'é', word)
    word = re.sub('È', 'è', word)
    word = re.sub('[/,.-;:!?\']', ' ', word)
    return word.lower()
    

def add_terms(doc, data, stemmer):
    while i < len(data):
        i = find_p(data, i, p_alnum)
        j = find_p(data, i, p_notalnum)
        k = find_p(data, j, p_notplusminus)
        if k == len(para) or not p_alnum(para[k]):
            j = k
        if (j - i) <= MAX_PROB_TERM_LENGTH and j > i:
            if is_stopword(term):
                pos += 1
                continue 
            term = stemmer(string.lower(data[i:j]))
            doc.add_posting(term, pos)
            pos += 1
        i = j
    return doc



def get_latlng_range(value):
    floatvalue = float(value)
    binstrings=[]

    floor = math.floor(floatvalue)
    for tick in [0.05, 0.2, 0.5]:
        binborder=floor

        for i in range(0,21):
            if floatvalue < binborder:
                binstrings.append(str(binborder-tick)+"_"+str(binborder))
                break
            binborder += tick

    binstrings.append(str(floor)+"_"+ str(math.floor(floatvalue) + 1 ))
    
    coarsefloor = math.floor(floatvalue/10)*10
    if floatvalue < coarsefloor + 5:
        binstrings.append(str(coarsefloor)+"_"+ str(coarsefloor + 5 ))
    else:
        binstrings.append(str(coarsefloor+5)+"_"+ str(coarsefloor + 10 ))
    binstrings.append(str(coarsefloor)+"_"+ str(coarsefloor +10 ))


    #print binstrings
    return binstrings
    


def get_place_terms(place=None):
    terms = []
    terms.append("_gp_" + place.postalcode)
    terms.append("_gc_" + place.city )

    for term in get_latlng_range(place.lat):
        terms.append("_glatrange_"+term)
    for term in get_latlng_range(place.lng):
        terms.append("_glngrange_"+term)

    return terms


def get_msg_terms(db=None,msg=None):

#   This is pretty important: what data to be shown from the thing?
#   Maybe should be parsed into json already? Ot serialise a hash somehow?
    doc_data = msg.content
    doc_values = []

    doc_terms = []
    
    stemmer = xapian.Stem("finnish")

    for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{3,35}\b', to_lower_case(msg.content)):
        word = match.group(0)
        if is_stopword(word):
            continue
        term = stemmer(word)
        doc_terms.append(term)

    for term in ["_commented-by_"+msg.author]:
        doc_terms.append(term)

    if msg.date:
        doc_terms.append("_c_"+str(msg.date)[:7])
                   
    official_terms = ["_o_"+msg.id]

    if msg.places:
        place = db.place.getnode(msg.places[0])
        for term in get_place_terms(place = place):
            doc_terms.append (term)


        for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{3,35}\b', to_lower_case(place.address)):
            word = match.group(0)
            if is_stopword(word):
                continue
            term = stemmer(word)
            #print "adding term "+term
            doc_terms.append(term)


        doc_data += "  " + place.address

        for term in get_latlng_range(place.lat):
            doc_terms.append("_glatrange_"+term)
        for term in get_latlng_range(place.lng):
            doc_terms.append("_glngrange_"+term)

        
        doc_values.append({"field": XAPIAN_X_COORD_FIELD, "value":xapian.sortable_serialise(float(place.lat))})
        doc_values.append({"field": XAPIAN_Y_COORD_FIELD, "value":xapian.sortable_serialise(float(place.lng))})	
    if msg.date:
    	doc_values.append({"field": XAPIAN_CREATED_FIELD, "value": xapian.sortable_serialise( float( msg.date.serialise() ) ) })


    return {"doc_data":doc_data,
            "doc_terms":doc_terms,
            "doc_values":doc_values }
    
def index_msg_react(db, cl, nodeid, oldvalues):
    index_msg(db=db, id=nodeid)

def index_msg(db=None, id=None, msg=None):

    global xapiandb

    
    if msg == None:
        msg=db.msg.getnode(id)

# _u_(author.id)
# _c_(yyyyrmm) (c niinkuin created)(esim. _c_200902 eli näin hakusanalla "AND _c_200902" saadaan rajattua haku helmikuussa 2009 luotuihin issueihin. Jos halutaan issuet ajalta 5.4.2009-12.7.2009, haetaan AND _c_200904 OR _c_200905 OR _c_200906 OR _c_200907 ja käsitellään nämä ValueRangeProcessorilla. Jos aikajakso yli vuoden, niin käytetään allaiolevaa _c_2009)
# _c_(yyyy)
# _m_(yyyymm) (m niinkuin modified)
# _m_(yyyy)
# _o_ (Jos virallinen vastaus)
# _s_(issue.status) (Tämä on varmaan tulevaisuudessa se pullonkaulan leventäjä - Kaikki obsoletet ja solvatut ja arkistoidut ja mitälie asiat voidaan jättää rauhassa arkiston kätköihin eikä niitä tarvi tuoda valuerangeprocessoria kuormittamaan.)
# _pp_(place.postal)
# _pc_(place.city)
# _c_(class) 

    identifier = "_msg_"+msg.id 
    

    doc = xapian.Document()

    db_opened = False
    
    if db.msg.is_retired(msg.id):
       if not xapiandb:
          xapiandb = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'xapian-msg-index/'), xapian.DB_CREATE_OR_OPEN)
          db_opened = True
       enquire = xapian.Enquire(xapiandb)
       query = xapian.Query(xapian.Query.OP_AND, [identifier])
       enquire.set_query(query)
       search_limit = 10
       matches = enquire.get_mset(0, search_limit)

       docid = None
       if matches.size():      # would it killya to implement __len__()??
           b = matches.begin()
           docid = b.get_docid()

       if docid:
	   doc.add_term("_retired", 0)
	   #print "removing "+str(docid) + "(identifier: " + identifier +") "
	   xapiandb.replace_document(docid, doc)
       if db_opened:
	   xapiandb =None
       return	


    index_stuff=get_msg_terms(db=db,msg=msg)
    #doc.set_data(index_stuff["doc_data"])
    msg_dict=message_to_dict(msg, db=db)
    doc.set_data( simplejson.dumps(msg_dict))

    
    doc.add_term(identifier,0)
    positioncounter=1

    index_stuff["doc_terms"].append("_msg")
    
    for term in index_stuff["doc_terms"]:
        doc.add_posting(term, positioncounter)
        positioncounter+=1



    author = db.user.getnode(msg.author)

    doc.add_posting("_author_"+author.username, positioncounter)
    positioncounter+=1
    	
    official=False
    if not author.organisation == "None":
	    for keyid in author.organisation:
		doc.add_posting("_group_"+db.organisation.getnode(keyid).name, positioncounter)
		positioncounter+=1
		doc.add_posting("_group_"+keyid, positioncounter)
		positioncounter+=1
		if keyid == "4" or keyid == "6":
			doc.add_posting("_official", positioncounter)
			#print "==#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#This is official message!=#=##=#=#=#=#=#=#=#=#=#=#=#"
			official=True
			positioncounter+=1


    for value in index_stuff["doc_values"]:        
        doc.add_value(value["field"], value["value"])
 
    doc.add_value(XAPIAN_DATATYPE_FIELD, "msg")
    doc.add_value(XAPIAN_ID_FIELD, msg.id)


    issue_id = db.issue.find(messages={id:1})
    if not issue_id:
            print "issue "+str(issue_id) +"not found: Returning!"
            return
    issue_id = issue_id[0]
    #print "parent issue_id"+ issue_id

    doc.add_value(XAPIAN_PARENT_ISSUE_FIELD, issue_id)


    msg_dict=message_to_dict(msg, db=db)
    msg_dict['parent_id']=issue_id
    msg_dict['parent_title']=db.issue.getnode(issue_id).title
    doc.set_data( simplejson.dumps(msg_dict))


    keywords=False
    if issue_id > 0:
        for keyid in db.issue.getnode(issue_id).keyword:
            doc.add_posting("_key_"+db.keyword.getnode(keyid).name, positioncounter)
            positioncounter+=1
            keywords=True

    if not keywords:
        doc.add_posting("_no_key", positioncounter)
        positioncounter+=1

                                            

    if not xapiandb:
        xapiandb = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'xapian-msg-index/'), xapian.DB_CREATE_OR_OPEN)
        db_opened = True

    enquire = xapian.Enquire(xapiandb)
    query = xapian.Query(xapian.Query.OP_AND, [identifier])
    enquire.set_query(query)
    search_limit = 10
    matches = enquire.get_mset(0, search_limit)

    docid = None
    if matches.size():      # would it killya to implement __len__()??
        b = matches.begin()
        docid = b.get_docid()

    if docid:
        #print "replacing "+str(docid) + "(identifier: "+identifier +") "
        xapiandb.replace_document(docid, doc)
    else:
        #print "Adding new thing (identifier: "+identifier +") "
        xapiandb.add_document(doc)

    if db_opened:
        xapiandb =None


def index_issue_react(db, cl, nodeid, oldvalues):
    index_issue(db=db, id=nodeid)

def index_issue(db=None, id=None, issue=None):
    global xapiandb


    print "indexing "+id

    if issue == None:
        issue=db.issue.getnode(id)

    identifier = "_issue_"+issue.id 


    doc = xapian.Document()

    if db.issue.is_retired(issue.id):
	    db_opened = False
	    if not xapiandb:
		try:
		   xapiandb = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'xapian-msg-index/'), xapian.DB_CREATE_OR_OPEN)
		   db_opened = True
		except:
		   print "could not open database! (index_issue, id="+str(id)+")"
		   return


	 
	    enquire = xapian.Enquire(xapiandb)
	    query = xapian.Query(xapian.Query.OP_AND, [identifier])
	    enquire.set_query(query)
	    search_limit = 10
	    matches = enquire.get_mset(0, search_limit)

	    docid = None
	    if matches.size():      # would it killya to implement __len__()??
		b = matches.begin()
		docid = b.get_docid()


	    if docid:
	      doc.add_term("_retired", 0)
	      #print "removing "+str(docid) + "(identifier: " + identifier +") "
	      xapiandb.replace_document(docid, doc)
	    if db_opened:
	      xapiandb =None
	    return	
#   This is pretty important: what data to be shown from the thing?
#   Maybe should be parsed into json already? Ot serialise a hash somehow?
    doc_data = issue.title

    stemmer = xapian.Stem("finnish")

    extra_terms=["_issue", str(identifier)]

    if issue.author:
        extra_terms.append("_created-by_"+str(issue.author)) 

    doc.add_term(identifier,0)
    position_counter=1

    for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{3,35}\b', to_lower_case(issue.title)):
        word = match.group(0)
        if is_stopword(word):
            continue
        term = stemmer(word)
        doc.add_posting(term, position_counter)
        position_counter+=1

    date_modified = None
    if issue.date:
        extra_terms.append("_created_"+str(issue.date)[:7])
        date_modified = issue.date.serialise()
    

    if issue.places:
        place = db.place.getnode(issue.places[0])
        index_place(id=place.id, db=db)
        for term in get_place_terms(place = place):
            doc.add_term(term,  position_counter)
            position_counter += 1

        for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{3,35}\b', to_lower_case(place.address)):
            word = match.group(0)
            if is_stopword(word):
                continue
            term = stemmer(word)
            doc.add_term(term,  position_counter)
            position_counter += 1


        doc_data += "  " + place.address
        doc.add_value(XAPIAN_X_COORD_FIELD, xapian.sortable_serialise(float(place.lat)))
        doc.add_value(XAPIAN_Y_COORD_FIELD, xapian.sortable_serialise(float(place.lng)))
    else:
        print "no places for this issue"

    keywords=False
    for keyid in issue.keyword:
        doc.add_posting("_key_"+db.keyword.getnode(keyid).name, position_counter)
        position_counter+=1
	keywords=True

    if not keywords:
        doc.add_posting("_no_key", position_counter)
        position_counter+=1

    if issue.author is not None:   
       	    author = db.user.getnode(issue.author)
	    doc.add_posting("_author_"+author.username, position_counter)
	    position_counter+=1
	    	
	    official=False
	    if not author.organisation == "None":
		    for keyid in author.organisation:
			doc.add_posting("_group_"+db.organisation.getnode(keyid).name, position_counter)
			position_counter+=1
			doc.add_posting("_group_"+keyid, position_counter)
			position_counter+=1
			if keyid == "4" or keyid == "6":
				#print "=================================This is official issue!==========================="
				doc.add_posting("_official", position_counter)
				official=True
				position_counter+=1

    if not keywords:
        doc.add_posting("_no_official", position_counter)
        position_counter+=1


    for term in extra_terms:
        if term[0:1] == '_':
            doc.add_posting(term, position_counter)
        else:
            doc.add_posting(stemmer(term), position_counter)
        position_counter+=1




    for msg_id in issue.messages:
        if not db.msg.is_retired(msg_id):
		msg=db.msg.getnode(msg_id)

		index_stuff=get_msg_terms(db=db,msg=msg)

		index_stuff["doc_terms"].append("_contains_msg_"+msg_id)

		for term in index_stuff["doc_terms"]:
		    doc.add_posting(term, position_counter)
		    position_counter+=1

		doc_data += index_stuff["doc_data"]
		
		if date_modified:
		    if msg.date > date_modified:
		        date_modified = msg.date.serialise()
		else:
		    date_modified = msg.date.serialise()


    doc.set_data( simplejson.dumps(issue_to_dict(issue, db=db)))

#    doc.add_value(XAPIAN_LATITUDE_VALUE, xapian.sortable_serialise(float(place.lat)))
#    doc.add_value(XAPIAN_LONGITUDE_VALUE, xapian.sortable_serialise(float(place.lng)))
#    doc.add_value(XAPIAN_POSTAL_FIELD, place.postalcode)
#    #print issue.date.serialise()    

    doc.add_value(XAPIAN_CREATED_FIELD, xapian.sortable_serialise( float( issue.date.serialise() ) ) )
    doc.add_value(XAPIAN_MODIFIED_FIELD, xapian.sortable_serialise( float( date_modified ) ) )
    if issue.author:
        doc.add_value(XAPIAN_ARTIST_FIELD, issue.author)
    doc.add_value(XAPIAN_HAS_PICTURE_FIELD, "-1")
    doc.add_value(XAPIAN_DATATYPE_FIELD,"issue")
    doc.add_value(XAPIAN_ID_FIELD, issue.id)
    doc.add_value(XAPIAN_PARENT_ISSUE_FIELD, "-1")
    doc.add_value(XAPIAN_PARENT_MESSAGE_FIELD, "-1")
    doc.add_value(XAPIAN_STATUS_FIELD, issue.status)


    db_opened = False
    if not xapiandb:
	try:
           xapiandb = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'xapian-msg-index/'), xapian.DB_CREATE_OR_OPEN)
           db_opened = True
        except:
	   print "could not open database! (index_issue, id="+str(id)+")"
	   return


 
    enquire = xapian.Enquire(xapiandb)
    query = xapian.Query(xapian.Query.OP_AND, [identifier])
    enquire.set_query(query)
    search_limit = 10
    matches = enquire.get_mset(0, search_limit)

    docid = None
    if matches.size():      # would it killya to implement __len__()??
        b = matches.begin()
        docid = b.get_docid()


    if docid:
        #print "replacing "+str(docid) + "(identifier: " + identifier +") "
        xapiandb.replace_document(docid, doc)
    else:
        #print "Adding new thing (identifier: "+ identifier +") "
        xapiandb.add_document(doc)


    if db_opened:
        xapiandb =None

    

def index_place_react(db, cl, nodeid, oldvalues):
    index_place(db=db, id=nodeid)


def index_place(db=None, id=None, issue=None):



    msg = None
    issue = None
    
    msg_id = db.msg.find(places={id:1})
    if msg_id:
        issue_id = db.issue.find(messages={msg_id[0]:1})
        if not issue_id:
            print "issue "+str(issue_id) +" of msg_id " + str(msg_id)+ " not found: (Maybe it is deleted?)"
            msg_id = None
        else:
            issue_id = issue_id[0]
            msg_id = msg_id[0]
            print "issue_id"+ issue_id+"\tmsg_id"+msg_id
    if not msg_id:
        issue_id = db.issue.find(places={id:1})
        if not issue_id:
            print "issue "+str(issue_id) +"not found: Returning!"
            return
        issue_id = issue_id[0]
        msg_id = "-1"

        print "issue_id"+ issue_id+"\tmsg_id"+msg_id

    
    place = db.place.getnode(id)

    identifier = "_place_"+str(place.id)


    doc = xapian.Document()


    issue = db.issue.getnode(issue_id) 

    if int(msg_id) > 0:   
	msg=db.msg.getnode(msg_id)
	content =  msg.content
    else:
	content = issue.title


    doc.set_data(content)
    #print content


#   This is pretty important: what data to be shown from the thing?
#   Maybe should be parsed into json already? Ot serialise a hash somehow?


    stemmer = xapian.Stem("finnish")

    position_counter = 0
    for term in [identifier,
                 "_place",
                 "_gpostal_" + str(place.postalcode),
                 "_gcity_" + str(place.city) ,
                 "_gcountry_" + str(place.country)]:
        #print term
        doc.add_term(term, position_counter)
        position_counter += 1
        
    for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{3,35}\b', to_lower_case(place.address)):
        word = match.group(0)
        if is_stopword(word):
            continue
        term = stemmer(word)
        #print term
        doc.add_term(term,  position_counter)
        position_counter += 1

    for term in get_latlng_range(place.lat):
        doc.add_term("_glatrange_"+term, position_counter)
        position_counter += 1
    for term in get_latlng_range(place.lng):
        doc.add_term("_glngrange_"+term, position_counter)
        position_counter += 1



    doc.add_value(XAPIAN_LATITUDE_VALUE, xapian.sortable_serialise(float(place.lat)))
    doc.add_value(XAPIAN_LONGITUDE_VALUE, xapian.sortable_serialise(float(place.lng)))
    doc.add_value(XAPIAN_POSTAL_FIELD, place.postalcode)
#    doc.add_value(XAPIAN_CREATED_FIELD=6, None)
#    doc.add_value(XAPIAN_MODIFIED_FIELD=7
#    doc.add_value(XAPIAN_ARTIST_FIELD=8
#    doc.add_value(XAPIAN_HAS_PICTURE_FIELD=9
    doc.add_value(XAPIAN_DATATYPE_FIELD,"place")
    doc.add_value(XAPIAN_ID_FIELD, place.id)
    doc.add_value(XAPIAN_PARENT_ISSUE_FIELD, issue_id)
    doc.add_value(XAPIAN_PARENT_MESSAGE_FIELD, msg_id)
    doc.add_value(XAPIAN_STATUS_FIELD, issue.status)


    db_opened = False
    global xapiandb
    if not xapiandb:
	try:
           xapiandb = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'xapian-msg-index/'), xapian.DB_CREATE_OR_OPEN)
	   db_opened = True
        except:
	   print "could not open database! (index_place, id="+str(id)+")"
	   return


    enquire = xapian.Enquire(xapiandb)
    query = xapian.Query(xapian.Query.OP_AND, [identifier])
    enquire.set_query(query)
    search_limit = 10
    matches = enquire.get_mset(0, search_limit)

    docid = None
    if matches.size():      # would it killya to implement __len__()??
        b = matches.begin()
        docid = b.get_docid()

    if docid:
        #print "replacing "+str(docid) + "(identifier: " + identifier +") parent message id: " + msg_id +"\tparent issue id: " + issue_id + "\tplace id"+ place.id
        xapiandb.replace_document(docid, doc)
    else:
        #print "Adding new thing (identifier: "+ identifier +") parent message id: " + msg_id +"\tparent issue id: " + issue_id + "\tplace id"+ place.id
        xapiandb.add_document(doc)    

    if db_opened:
        xapiandb =None


    print "place indexed: id "+id


def indexer(db, cl, nodeid, oldvalues):
           
    data_to_be_indexed={}
    message_words_to_be_indexed={}
    
    if cl == db.getclass('place'):
        logging.info("================= Running geographical indexer =================")
        #print "Place added or set"
        data_object = cl.getnode(nodeid)
        place = data_object
        
        place_identifier = "place:"+str(nodeid)
         
        if len(place.lng) > 0:
                                    
            #print "place: " + place.lng
            #print "place: " + place.lat
            #print "place: " + place.address
            #print "place: " + place.country
            #print "place: " + place.postal

            data_to_be_indexed.update({ XAPIAN_DATATYPE_FIELD: float(XAPIAN_INDEXING_TYPE_PLACE), 
                                        XAPIAN_X_COORD_FIELD: float(place.lng),
                                        XAPIAN_Y_COORD_FIELD: float(place.lat), 
                                        XAPIAN_POSTAL_FIELD: float(place.postal)})
        
            # We use the identifier twice: once in the actual "text" being
            # indexed so we can search on it, and again as the "data" being
            # indexed so we know what we're matching when we get results
            
            ''' "identifier" is  (classname, itemid, property) '''

            issue_ids = db.issue.find( places={nodeid:1 } )
            if issue_ids:
                data_to_be_indexed.update({XAPIAN_PARENT_ISSUE_FIELD:identifier})
            else:
                message_ids = db.msg.find( places={nodeid:1 } )
                if message_ids:
                    data_to_be_indexed.update({XAPIAN_PARENT_MESSAGE_FIELD:identifier})
                    
            #print "identifier: " + identifier


 
    if cl == db.getclass('issue'):
        issue_identifier = "issue:"+nodeid

    if xapian_avail:
        issue_index_db = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'xapian-complete-index'), xapian.DB_CREATE_OR_OPEN)
        # see if the id is in the database
        enquire = xapian.Enquire(issue_index_db)
        query = xapian.Query(xapian.Query.OP_AND, [identifier])
        enquire.set_query(query)
        matches = enquire.get_mset(0, 10)
        if matches.size():      # would it killya to implement __len__()??
            b = matches.begin()
            docid = b.get_docid()
        else:
            docid = None

        doc = xapian.Document()
        doc.set_data(identifier)

        stemmer = xapian.Stem("finnish")

        for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{3,25}\b', to_lower_case(data_object.title)):
            word = match.group(0)
            if is_stopword(word):
                continue
            term = stemmer(word)
            doc.add_posting(term, match.start(0))

        offset = len(data_object.title) + XAP_OFFSET_KLUDGER 

        for msg in data_object.messages:
            msg_object=db.msg.getnode(msg)
            text = msg_object.content #.encode('utf-8')
            logging.info("Adding message: "+ text)

            for match in re.finditer(r'\b[A-ZÅÖÄÜÉÈÁÀ]{2,35}\b', to_lower_case(text)):
                word = match.group(0)
                if is_stopword(word):
                    continue
                term = stemmer(word)
                logging.info("Adding term: " +word + " > \t" + term)
                doc.add_posting(term, match.start(0) + offset)
    
            offset += len(text  ) + XAP_OFFSET_KLUDGER 

            if msg.places:
                for term in get_place_keywords(place = db.place.getnode(msg.places[0])):
                    doc.add_posting(term)


        for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{2,35}\b', to_lower_case(data_object.address)):
            word = match.group(0)
            if is_stopword(word):
                continue
            term = stemmer(word)
            doc.add_posting(term, match.start(0))

        if issue.places:
            for term in get_place_keywords(place = db.place.getnode(issue.places[0])):
                doc.add_posting(term)


        for key,value in data_to_be_indexed:
            doc.add_value(key, xapian.sortable_serialise(value))

        if docid:
            #print "replacing "+docid
            issue_index_db.replace_document(docid, doc)
        else:
            #print "Adding new thing "
            issue_index_db.add_document(doc)
            
    else:
        logging.info("XAPIAN NOT AVAILABLE!")


def get_issue_json_and_terms(db=None, ):
    dummy = 1



def get_msg_json_and_terms(db=None, ):
    dummy = 1






def issue_to_dict(issue, issue_id=None, db=None):
    db_opened=False
    if db is None:
        db = tracker().open('admin')
        db_opened = True;

    if issue is None:
        issue = db.issue.getnode(issue_id)


#    if issue.date is not None:
#        smart_date = smart_date_diff(datetime.datetime(issue.date.year, issue.date.month, issue.date.day, issue.date.hour,
#            issue.date.minute, int(issue.date.second)))
#    else:
    smart_date = ''     

    
    if db.issue.is_retired(issue.id):
        rval = {'title':_('This message by has been removed by %(actor)s.') % {'actor' : 'administrators'},
                          'date' : str(issue.date),
                          'smartdate' : smart_date,}
        if db_opened:
            db.close()
        return rval

    
    places = []
    for place_id in issue.places:
        if db.place.hasnode(place_id):
            places.append(db.place.getnode(place_id))
      
    points = []

    for place in places:
        if place.lat and place.lng:
#            #print "Appending "+'lat '+  place.lat + ', lng: '+ place.lng
            points.append( {'lat': place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id } )


    
    if issue.author is not None:
        author = db.user.getnode(issue.author)    
        if author.screenname:
            authorname=author.screenname
        else:
            authorname=author.username
        authorlink=author.username

        if author.title:
            authortitle = author.title
        else:
            authortitle = ''
        author_id = author.id
        if author.organisation != []:
            org = db.organisation.getnode(author.organisation[0])
            organisation = {'name':org.name,
                            'logo': org.logo,
                            'css': org.css,
                            'screenname':org.screenname,
                            'signature': org.signature,
                            'linkurl': org.homeurl,
                            'id': org.id  }
        else:
            organisation = {'name': None,
                    'logo': None,
                    'css': None,
                    'screenname': None,
                    'signature': None,
                    'linkurl': None,
                    'id': 0   }

            
    else:
        author = db.user.getnode(db.user.lookup('anonymous'))
        authortitle = ''
        authorname=author.screenname
        authorlink="anonymous"
        author_id = author.id
        organisation = {'name': None,
                            'logo': None,
                            'css': None,
                            'screenname': None,
                            'signature': None,
                            'linkurl': None,
                            'id': 0   }
    rval = {
        'title': issue.title,
        'options': {
            'author_id': int(author_id),
            'author' : authorname,
            'authorlink':authorlink,
            'authortitle': authortitle,
            'organisation' : organisation,
            'date' : str(issue.date),
            'smartdate' : smart_date,
            'points' : points,        
            'score': issue.score,
            'id': issue.id,
            'status': issue.status,
            'icon': {'name':'/images/merkki_sin.png',
                     'activeiconname':'/images/merkki_pun.png',
                     'partlyactiveiconname':'/images/merkki_pun.png',
                     'w': 23,
                     'h': 41,
                     'ax': 5,
                     'ay': 41,
                     },
            'type':'issue',

        },
    }
    if len(issue.keyword) ==0:
        #rval['options'].update({ 'link': reverse('report_view', args=[issue.id]) })
	rval['options'].update({ 'link': "/r/"+issue.id })
    else:
        #rval["options"].update({ 'link': reverse('tagged_report_view', args=[db.keyword.getnode(issue.keyword[0]).name, issue.id]) })
	rval['options'].update({ 'link': "/r/"+db.keyword.getnode(issue.keyword[0]).name+"/"+issue.id })
	rval['options'].update({ 'tag': db.keyword.getnode(issue.keyword[0]).name })


#    if issue.files != []:
#        dummy = 1
#        rval['options'].update({'thumburl':get_image_thumbnail(issue.files[0], 80, 80 ),
#                                'imageurl':get_image_thumbnail(issue.files[0], 380, 380) })

    
    if len(places)>0:
        if places[0].lat and places[0].lng:
            rval['options'].update ({'onMap': True })
            rval.update ({'point': {'lat': places[0].lat, 
                                               'lon':places[0].lng,
                                               'address':places[0].address,
                                               'id':places[0].id }})
#            #print "Appending "+'lat '+  place.lat + ', lng: '+ place.lng

    else:
         rval['options'].update ({'onMap': True })       


    
    if not issue.messages:
        return rval

    comments = []
    last_comment_date = ''
    last_comment_smart_date = ''
    for msg in issue.messages:
        if db.msg.is_retired(msg):
            continue
        comment_dict = message_to_dict(None,id=msg,db=db)
        if comment_dict.has_key("point"):
#            print "Appending "+'lat '+  place.lat + ', lng: '+ place.lng
            comment_dict["point"]["lon"]=comment_dict["point"]["lng"]
            if rval["options"].has_key("points"):
                rval["options"]["points"].append( comment_dict["point"] )
            else:
                rval["options"]['points']=  [comment_dict["point"]]

            if not rval.has_key("point"):

                rval['point']=  comment_dict["point"]

        comments.append(comment_dict)
        if comment_dict.has_key('point'):
            rval['options'].update({'onMap':True})
    
    
#        if comment_dict.has_key('point'):
#            rval['options']['points'].append(comment_dict['point'])
    
        if last_comment_date is None or comment_dict['date'] > last_comment_date:
            last_comment_date=  comment_dict['date']
            last_comment_smart_date=  comment_dict['smartdate']
    

    if len(comments)>0:
        commentcount = len(comments)
    else:
        commentcount = "00"
        
    rval['options'].update({
        'last_comment_date' : last_comment_date,
        'last_comment_smartdate' : last_comment_smart_date,                    
        'comments': comments,
        'commentcount': commentcount,
    })
    
    if db_opened:   
        db.close()

    return rval



def message_to_dict(msg=None, id=None, db=None):        
    db_opened=False
    if db is None:
        db = tracker().open('admin')
        db_opened = True;

    if msg is None:
        if id is not None: 
            msg = db.msg.getnode(id)
        else:
            return

    if msg.date:
        date = str(msg.date)
#        smart_date = (smart_date_diff(datetime.datetime(msg.date.year, msg.date.month, 
#                                                       msg.date.day, msg.date.hour,
#                                                       msg.date.minute, 
#                                                       int(msg.date.second))))
    else:
        date = ''
    smart_date = ''

    if msg.author is not None:
        author = db.user.getnode(msg.author)    
        if author.screenname:
            authorname=author.screenname
        else:
            authorname=author.username
        authorlink=author.username
        if author.title:
            authortitle = author.title
        else:
            authortitle = ''
        if author.organisation != []:
            org = db.organisation.getnode(author.organisation[0])
            organisation = {'name':org.name,
                            'logo': org.logo,
                            'css': org.css,
                            'screenname':org.screenname,
                            'signature': org.signature,
                            'linkurl': org.homeurl,
                            'id': org.id  }
            
        else:
            organisation = {'name': None,
                            'logo': None,
                            'css': None,
                            'screenname': None,
                            'signature': None,
                            'linkurl': None,
                            'id': 0   }
    else:
        author = db.user.getnode(db.user.lookup('anonymous'))
        authortitle = ''
        authorname=author.screenname
        organisation = {'name': None,
                            'logo': None,
                            'css': None,
                            'screenname': None,
                            'signature': None,
                            'linkurl': None,
                            'id': 0   }
        
        authorname=author.screenname
        authortitle = author.title
        if author.organisation != []:
            organisation = organisation_to_dict(id=author.organisation[0], db=db)
             

    comment={
             'id': msg.id,
             'author': authorname, 
             'authortitle':authortitle,
             'authorlink':authorlink,
             'organisation': organisation,
             'date': date,
             'smartdate' : smart_date,
             'class': author.organisation is not None and 'org' or '',
             }

    if db.msg.is_retired(msg.id):
        #        comment.update({'text':_('This message by has been removed by %(actor)s.') % {'actor' : 'administrators'},
        #                        'class': 'removed' })
        comment.update({'text': 'This message by has been removed by administrators'})
        if db_opened:
            db.close()
        return comment
        

    comment.update({'text':  msg.content})


    if msg.places != []:
        place = db.place.getnode(msg.places[0])
        comment['point'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address, 'id':place.id}

#    if msg.files != []:
#        comment.update({'thumburl':get_image_thumbnail(msg.files[0], 80, 80 ),
#                                'imageurl':get_image_thumbnail(msg.files[0], 380, 380) })

#    if len(msg.places)>0:
#        place = db.place.getnode(msg.places[0])
#        comment['point'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address}
#        comment['place'] = {'lat':place.lat, 'lng':place.lng, 'address':place.address}

    if db_opened:   
        db.close()
    return comment





def init(db):
#    logging.info("================= Firing geographical indexer =================")

    
#    db.place.react('set', indexer)
#    db.place.react('create', indexer)

    db.place.react('set', index_place_react)
    db.place.react('create', index_place_react)
    db.place.react('retire', index_place_react)

    db.msg.react('set', index_msg_react)
    db.msg.react('create', index_msg_react)
    db.msg.react('retire', index_msg_react)

    db.issue.react('set', index_issue_react)
    db.issue.react('create', index_issue_react)
    db.issue.react('retire', index_issue_react)

