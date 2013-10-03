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

SCOREISSUE_USER_PLUS_MULT = 2
SCOREISSUE_USER_PLUS_EXP  = 2
SCOREISSUE_USER_MINUS_MULT= 1
SCOREISSUE_USER_MINUS_EXP = 1
SCOREISSUE_ANON_PLUS_MULT = 1
SCOREISSUE_ANON_PLUS_EXP  = 1
SCOREISSUE_ANON_MINUS_MULT= 1
SCOREISSUE_ANON_MINUS_EXP = 1

SCORECOMM_USER_PLUS_MULT  = 1 
SCORECOMM_USER_PLUS_EXP   = 1
SCORECOMM_ANON_PLUS_MULT  = 1
SCORECOMM_ANON_PLUS_EXP   = 1


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


def popularity_indexer(db, cl, nodeid, oldvalues):

    logging.info("checking if anything should be done..." + nodeid)

    '''  watch for additions to the
        "votes" property and changes the issue scoring accordingly.
    '''
    # send a copy of all new messages to the nosy list

    
    logging.info( "nodeid: " + str(nodeid) )
    logging.info( "oldvalues: " + str(oldvalues) )
            #            votes[msg] = msg.votes

    if cl == db.getclass('vote'):
        print "Vote added or set"

        vote = db.vote.getnode(nodeid)
    
        if vote.issue != []:
            issue_id = vote.issue
        else :    
            message_id = vote.message
            logging.info( "messageid: " + str(message_id) )
            issue_ids = db.issue.find( messages={message_id:1 } )
            issue_id = issue_ids[0]
        
#        messageid = cl.getnode(nodeid).message
        
 
        # Like this but get issues according to messages they point to:
        #vote_ids = db.vote.find( msg={messageid:1 } )

        if issue_id is not None:
            itemid = issue_id
            issue_id = itemid
    
            logging.info( "issueid: " + str(itemid) )
            # who is no one?
            anon_ids = db.user.lookup('anonymous')
    
            # calculate score:
            score = 0
            
            votesFor = 0
            votesAgainst = 0
            
            votecast =""

            userVotesFor = 0
            userVotesAgainst = 0
            
            anonVotesFor = 0
            anonVotesAgainst = 0
            
            vote_ids = db.vote.find( issue={issue_id:1 } )
            
            for v in vote_ids:
                vote = db.vote.getnode(v)
                if vote.value == "1":
                    if vote.author == anon_ids[0]:
                        anonVotesFor += 1
                    else:
                        userVotesFor += 1
                elif vote.value == "-1":
                    if vote.author == anon_ids[0]:
                        anonVotesAgainst += 1
                    else:
                        userVotesAgainst += 1
        
            logging.info( "Issue nr. " + issue_id)    

            logging.info( "userVotesFor:    \t"   + str (userVotesFor    ) + " " +str(SCOREISSUE_USER_PLUS_MULT * math.pow(userVotesFor,     SCOREISSUE_USER_PLUS_EXP )))
            logging.info( "userVotesAgainst:\t" + str (userVotesAgainst) + " " + str (SCOREISSUE_USER_MINUS_MULT* math.pow(userVotesAgainst, SCOREISSUE_USER_MINUS_EXP )))
 
            logging.info( "anonVotesFor:    \t"   + str (anonVotesFor    ) + " " +str(SCOREISSUE_ANON_PLUS_MULT * math.pow(anonVotesFor,     SCOREISSUE_ANON_PLUS_EXP )))
            logging.info( "anonVotesAgainst:\t" + str (anonVotesAgainst) + " " + str (SCOREISSUE_ANON_MINUS_MULT* math.pow(anonVotesAgainst, SCOREISSUE_ANON_MINUS_EXP)))
                           
            score =  SCOREISSUE_USER_PLUS_MULT * math.pow(userVotesFor, SCOREISSUE_USER_PLUS_EXP ) - SCOREISSUE_USER_MINUS_MULT* math.pow(userVotesAgainst, SCOREISSUE_USER_MINUS_EXP)
            score += SCOREISSUE_ANON_PLUS_MULT * math.pow(anonVotesFor, SCOREISSUE_ANON_PLUS_EXP)  - SCOREISSUE_ANON_MINUS_MULT* math.pow(anonVotesAgainst, SCOREISSUE_ANON_MINUS_EXP)

            score += anonVotesFor - anonVotesAgainst
            firstMessage = False
        
            for msg_id in db.issue.getnode(itemid).messages:
                
                vote_ids = db.vote.find( message={msg_id:1 } )
                votesFor = 0
                votesAgainst = 0
                
                votecast =""
    
                userVotesFor = 0
                userVotesAgainst = 0
                
                anonVotesFor = 0
                anonVotesAgainst = 0
                
                for v in vote_ids:
                    vote = db.vote.getnode(v)
                    if vote.value == "1":
                        if vote.author == anon_ids[0]:
                            anonVotesFor += 1
                        else:
                            userVotesFor += 1
                    elif vote.value == "-1":
                        if vote.author == anon_ids[0]:
                            anonVotesAgainst += 1
                        else:
                            userVotesAgainst += 1
            
                logging.info( "Message nr. " + msg_id)    
                logging.info( "userCommentVotesFor:\t" + str (userVotesFor) + " " + str (SCORECOMM_USER_PLUS_MULT * math.pow(userVotesFor, SCORECOMM_USER_PLUS_EXP) ))
                logging.info( "anonCommentVotesFor:\t" + str (anonVotesFor) + " " + str (SCORECOMM_ANON_PLUS_MULT * math.pow(anonVotesFor, SCORECOMM_ANON_PLUS_EXP) ))
                
                score += SCORECOMM_USER_PLUS_MULT * math.pow(userVotesFor, SCORECOMM_USER_PLUS_EXP) + SCORECOMM_ANON_PLUS_MULT * math.pow(anonVotesFor, SCORECOMM_ANON_PLUS_EXP)

                
    
            logging.info( "New score for issue: " + str(score) )
    
            db.issue.set(itemid, score=str(score))
            db.commit()
    
    
    
            if xapian_avail:
                   
                       
        #        xap_db = xapian.WritableDatabase(settings.XAPIAN_DATABASE_HOME, xapian.DB_CREATE_OR_OPEN)
                xap_db = xapian.WritableDatabase( os.path.join(db.config.DATABASE, 'text-index'), xapian.DB_CREATE_OR_OPEN)
            
                stemmer = xapian.Stem("finnish")
            
                data_object = db.issue.getnode(itemid)
            
        
                # We use the identifier twice: once in the actual "text" being
                # indexed so we can search on it, and again as the "data" being
                # indexed so we know what we're matching when we get results
                
                ''' "identifier" is  (classname, itemid, property) '''
        
                identifier = "issue:" + itemid +":title:destruktomania"
                
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
        
                votes = {}
                    
        
                doc = xapian.Document()
                    
                doc.set_data(identifier)
        
                logging.info("Indexing " + itemid + ": "+ data_object.title)
        
        
                for match in re.finditer(r'\b[a-zA-ZäöåüÄÖÅÜÉÈÁÀéèáà]{2,25}\b', to_lower_case(data_object.title)):
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
        
                    for match in re.finditer(r'\b[A-ZÅÖÄÜÉÈÁÀ]{2,25}\b', to_lower_case(text)):
                        word = match.group(0)
                        if is_stopword(word):
                            continue
                        term = stemmer(word)
                        logging.info("Adding term: " +word + " > \t" + term)
                        doc.add_posting(term, match.start(0) + offset)
            
                    offset += len(text  ) + XAP_OFFSET_KLUDGER 
                    
                doc.add_value(XAPIAN_ISSUE_SCORE_VALUE, xapian.sortable_serialise(score) )
    
                
                if docid:
                    xap_db.replace_document(docid, doc)
                else:
                    xap_db.add_document(doc)
                    
                    
            else:
                logging.info("XAPIAN NOT AVAILABLE!")
    

        
    print "popularity indexer finished"
        
def init(db):
    
    logging.info("================= Firing popularity indexer =================")

    db.vote.react('set', popularity_indexer)
    db.vote.react('create', popularity_indexer)


      