#! /usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Built upon example in 
# http://www.rkblog.rk.edu.pl/w/p/xapian-python/
#
#   9.2.2009 rk


import sys
import xapian
import pygame
import re
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'

global screenwidth
global screenheight


class Variables:
	
	screen_width = 827
	screen_height = 695

	use_bg_bitmap = True
	bg_bitmap = "./ksv_bg.bmp"

	search_area_bg_color = [255,255,255]

	search_text_color = [0,0,0]
	result_text_color = [0,0,0]

	search_area_left = 82
	search_area_top = 529
	search_area_width = 295
	search_area_height = 148

	result_area_bg_color = [238,238,238]

	result_area_left = 471
	result_area_top = 238
	result_area_width = 293
	result_area_height = 449

# 	bg_bitmap = "./test_bg.bmp"

#	search_area_left = 110
#	search_area_top = 115
#	search_area_width = 290
#	search_area_height = 250

#	result_area_bg_color = [255,255,255]

#	result_area_left = 457
#	result_area_top = 89
#	result_area_width = 285
#	result_area_height = 475

	result_count = 8

	stoplist = { "on": 1, "se": 1 , "han": 1 , "mika" :1, "joka":1, "ei":1, "vain":1, "vaan":1}
	stopchars = { '!':1, '?':1, '.':1, ';':1 }

	def __init__(self):
		print '(Initializing variables)'


### These are from pygame.org:
### From wiki, text wrapping functions:

def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account."""
 
    # separate the text into new lines.
    if "\r\n" in text:
        new_line_char = "\r\n"
    elif "\n" in text:
        new_line_char = "\n"
    elif "\r" in text:
        new_line_char = "\r"
    else:
        new_line_char = ""
 
    if new_line_char:
        lines = text.split(new_line_char)
    else:
        lines = [text]
 
    return_lines = []
    for text in lines:
        return_lines.extend( wrapline(text, font, maxwidth) )
 
    return return_lines


### These were from pygame.org



def main():

    variables = Variables()


    pygame.init()
    window = pygame.display.set_mode((variables.screen_width, variables.screen_height))
    pygame.display.set_caption('Test')

    background = pygame.Surface(window.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 18)
    text = font.render("Kirjoita palautetta:", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2)

    searchstring = ""
    oldsearchstring = ""

    text2 = font.render(searchstring, 1, (variables.search_text_color[0],variables.search_text_color[1],variables.search_text_color[2]))
    textpos2 = text2.get_rect(left=variables.search_area_left, top=variables.search_area_top)

    text3 = font.render("Samankaltaisia palautteita:", 1, (10,10, 10))
    textpos3 = text3.get_rect(centerx=background.get_width()/2, centery=font.get_height()*3)

    resultstring = ""
    oldresultstring = ""
    counter = 3

    text4 = font.render(resultstring, 1, (10,10, 10))
    textpos4 = text.get_rect(left=variables.result_area_left, top=variables.result_area_top)

    if variables.use_bg_bitmap == True:
	    try:
		    image = pygame.image.load(variables.bg_bitmap)
	    except pygame.error, message:
		    print 'Cannot load image:', name
		    raise SystemExit, message
	    image = image.convert()
	    imagepos = image.get_rect(left=0, top=0)

	    background.blit(image, imagepos)



    window.blit(background, (0, 0))
    pygame.display.flip()

    while True:
      clock.tick(30000)

      for event in pygame.event.get():
        if event.type == QUIT:
            return

        elif event.type is pygame.KEYDOWN:
            
            _ = pygame.key.name(event.key)
            print _

            if _ == 'backspace' and len(searchstring) > 0:
                
                searchstring = searchstring[:-1]

            elif len(_) == 1 and ord(_[0]) <= ord("z") and ord(_[0]) >= ord("a"):
                searchstring += str(_)

            elif _ == "space":
                searchstring += " "
	    elif _ == "'":
		    searchstring += "a"
	    elif _ == ";": 
		    searchstring += "o"
	    else:
		    print "invalid key: "+_

#	    if len(searchstring) == 0 or searchstring[-1] == ' ':
      
      if oldsearchstring != searchstring:
		try:
                    database = xapian.Database('test/')

                    enquire = xapian.Enquire(database)
                    stemmer = xapian.Stem("finnish")
                    tmp_terms = searchstring.split(' ')
                    terms= []
                    for term in tmp_terms:
                        if len(term)>0:
				stemmed = stemmer(term)
				if not variables.stoplist.has_key(stemmed):
					terms.append(stemmer(term))
				else: 
					print "not including " + term
                    print terms
                    query = xapian.Query(xapian.Query.OP_OR, terms)
                    print "Performing query `%s'" % query.get_description()
#                    resultstring = "Performing query `%s'" % query.get_description() + "\n"

                    enquire.set_query(query)
                    matches = enquire.get_mset(0, variables.result_count)

                    print "%i results found" % matches.get_matches_estimated()
                    resultstring = "%i results found" % matches.get_matches_estimated() + "\n"
                    for match in matches:
#                        resultstring += "ID %i %s" % (match[xapian.MSET_DID], match[xapian.MSET_DOCUMENT].get_data()) + "\n"

			    
#                        resultstring += "ID %i" % (match[xapian.MSET_DID])

			    
			full_result = re.sub(r'\s+', ' ', match[xapian.MSET_DOCUMENT].get_data()).split(' ')
			print full_result
			counterhash = {}
			counter = -1
			headline = 1
			headlineend = -1
			for word in full_result:
				counter += 1

				if headline == 1:
					counterhash[counter] = 1
					if word == "*":
						headline = -1
						headlineend = counter
						print "headline end" + str(headlineend)
						continue

					
				else:
					word = re.sub (r'\W','',word)				
					for stem in terms:
						if stemmer(word).lower() == stem:
							for c in range (1, 4):
								print str(c) + ": "+ str(counter - c)
								if counter - c <= 0:
									print "breaking : 1>" + full_result[counter-c][-1] + "<1"
									break

								if counter - c > 0 and counter -c < len(full_result) and variables.stopchars.has_key(full_result[counter-c][-1]):
									print "breaking : 1>" + full_result[counter-c][-1] + "<1"
									break
								counterhash[counter - c] = 1
								print full_result[counter-c]

							for c in range (0, 6):
								print str(c) + ": "+ str(counter + c)
								if counter + c >= len(full_result) :
									print "breaking : 2>" + full_result[counter+c][-1] + "<2"
									break
								elif variables.stopchars.has_key(full_result[counter+c][-1]):
									print "breaking : 2>" + full_result[counter+c][-1] + "<2"
									counterhash[counter + c] = 1
									break
								counterhash[counter + c] = 1
								print full_result[counter+c]
								


			oldindex = 0
			for k in counterhash.keys():
				if k == headlineend:
					resultstring += "\n\n"
				elif k >= 0 and k < len(full_result):
					resultstring += full_result[k] + " "
#					if k-oldindex > 1:
#						resultstring += "..."
					oldindex = k
				else:
					print "missing word "+k
			
			resultstring += "...\n     __________________________________   \n\n"
#                        resultstring += "ID %i %i%% [%s]" % (match[xapian.MSET_DID], match[xapian.MSET_PERCENT], match[xapian.MSET_DOCUMENT].get_data()) + "\n"
#                        print "ID %i %i%% [%s]" % (match[xapian.MSET_DID], match[xapian.MSET_PERCENT], match[xapian.MSET_DOCUMENT].get_data())


                except Exception, e:
                    print >> sys.stderr, "Exception: %s" % str(e)
                    sys.exit(1)



#      background.fill((250, 250, 250))
#      background.blit(text, textpos)

      blitting = False

      if oldsearchstring != searchstring:

          pygame.draw.rect(background, (variables.search_area_bg_color[0],variables.search_area_bg_color[1],variables.search_area_bg_color[2]), (variables.search_area_left, variables.search_area_top, variables.search_area_width, variables.search_area_height))

	  oldsearchstring = searchstring
          counter = 0

      
	  clean_searchstring = re.sub(r'ä', 'a', searchstring)
	  clean_searchstring = re.sub(r'ö', 'o', clean_searchstring)

          for line in wrap_multi_line(clean_searchstring, font, variables.search_area_width):

              textheight = font.get_height()*counter

	      if textheight + font.get_height() > variables.search_area_height:
		      break

              linetext = font.render(line, 1, (variables.search_text_color[0],variables.search_text_color[1],variables.search_text_color[2]))
	      linetextpos = linetext.get_rect(left=variables.search_area_left, top=variables.search_area_top+textheight)

              background.blit(linetext, linetextpos)
              counter += 1
	      blitting = True



#      background.blit(text3, textpos3)


      if oldresultstring != resultstring:
          pygame.draw.rect(background, (variables.result_area_bg_color[0],variables.result_area_bg_color[1],variables.result_area_bg_color[2]), (variables.result_area_left, variables.result_area_top, variables.result_area_width, variables.result_area_height))

          oldresultstring = resultstring
          counter = 0

	  clean_resultstring = re.sub(r'ä', 'a', resultstring)
	  clean_resultstring = re.sub(r'ö', 'o', clean_resultstring)

          for line in wrap_multi_line(clean_resultstring, font, variables.result_area_width):

              textheight = font.get_height()*counter

	      if textheight + font.get_height() > variables.result_area_height:
		      break

              linetext = font.render(line, 1, (variables.result_text_color[0],variables.result_text_color[1],variables.result_text_color[2]))
	      linetextpos = linetext.get_rect(left=variables.result_area_left, top=variables.result_area_top+textheight)

              background.blit(linetext, linetextpos)
              counter += 1

	      blitting = True
	      
      if blitting:
	      window.blit(background, (0, 0))
	      pygame.display.flip()

if __name__ == "__main__":
    main()
