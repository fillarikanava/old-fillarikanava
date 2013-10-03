# -*- coding: UTF-8 -*-

from roundup import roundupdb, hyperdb
import logging
import random
import re,os
import math

try:
    import xapian
    xapian_avail = True
except ImportError:
    logging.warning('Failed to import xapian, search disabled')
    xapian_avail = False
    
    
XAPIAN_ISSUE_SCORE_VALUE = 1
XAPIAN_LATITUDE_VALUE = 3
XAPIAN_LONGITUDE_VALUE = 4



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


def geographical_indexer(db, cl, nodeid, oldvalues):

    if cl == db.getclass('place'):
        logging.info("================= Running geographical indexer =================")
        print "Place added or set"
        data_object = cl.getnode(nodeid)
        place = data_object
         

        if xapian_avail and len(place.lng) > 0:
            
            itemid=nodeid
               
            xap_db = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'text-index'), xapian.DB_CREATE_OR_OPEN)
            print "place: " + place.lng
        
            print "place: " + place.lat
            print "place: " + place.address
            print "place: " + place.country
        
            # We use the identifier twice: once in the actual "text" being
            # indexed so we can search on it, and again as the "data" being
            # indexed so we know what we're matching when we get results
            
            ''' "identifier" is  (classname, itemid, property) '''

            issue_ids = db.issue.find( places={itemid:1 } )
            if issue_ids:
                identifier = "place:issues:" + itemid +":" + issue_ids[0]
            else:
                message_ids = db.msg.find( places={itemid:1 } )
                if message_ids:
                    identifier = "place:messages:" + itemid + message_ids[0]
                else:
                    identifier = "place::" + itemid
                    
            print "identifier: " + identifier
                
            # see if the id is in the database
            enquire = xapian.Enquire(xap_db)
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

            for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{2,25}\b', to_lower_case(data_object.address)):
                word = match.group(0)
                if is_stopword(word):
                    continue
                term = stemmer(word)
                doc.add_posting(term, match.start(0))
 
            print "indexing: "+ place.lat + " "+str(xapian.sortable_serialise(float(place.lat)))+ ", " + place.lng + " "+ str(xapian.sortable_serialise(float(place.lng)))
 
            doc.add_value(XAPIAN_LATITUDE_VALUE, xapian.sortable_serialise(float(place.lat)))
            doc.add_value(XAPIAN_LONGITUDE_VALUE, xapian.sortable_serialise(float(place.lng)))
    
            if docid:
                print "replacing "+docid
                xap_db.replace_document(docid, doc)
            else:
                print "Adding new thing "
                xap_db.add_document(doc)
                
        else:
            logging.info("XAPIAN NOT AVAILABLE!")



def init(db):
#    logging.info("================= Firing geographical indexer =================")

    
    db.place.react('set', geographical_indexer)
    db.place.react('create', geographical_indexer)
