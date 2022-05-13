#!/usr/bin/python3
# -*- coding: utf-8 -*-
import Sword as SW 
import re 

# module internal constants
# output formatting of xml
OF_PLAIN = 1
OF_STRONGS = 2
OF_RAW = 3

# handling of comma from verse list in output
CVL_NONE = 0       # leave as it is delivered from Sword (but close with newline)
CVL_SEPARATOR = 1  # write a separator line after each input section
CVL_NEWLINE = 2    # write additional newline after each input section

# headings (book/chapter/verse) in verse output
BCV_NONE = 0       # no verse heading (use input field for reference)
BCV_INPUT = 1      # use sections from input verse list
BCV_VERSE = 2      # write heading before each verse
BCV_NUMBER = 3     # use sections from input, additionally print verse number

# search type definitions from the C++ source code
SEARCHTYPE_REGEX = 0              # (default)
SEARCHTYPE_PHRASE = -1            #
SEARCHTYPE_MULTIWORD = -2         #
SEARCHTYPE_ENTRYATTR = -3         # (eg. "Word//Lemma./G1234/")
SEARCHTYPE_EXTERNAL = -4          # (e.g. Apache Lucene)

# Removing XML tags could also be done with a markup filter 
# mf = SW.MarkupFilterMgr(SW.FMT_PLAIN) 
# my_lib = SW.SWMgr(mf) 
# However, the filter throws a memory access fault on closing, 
# so this is an easy workaround. 
def stripHTML(verseText, oformat = OF_PLAIN):
    result = verseText
    # preserve paragraph ends as line breaks
    result = re.sub('type="line"/>', 'type="line"/>\n', result)
    result = re.sub('type="x-p"/>', 'type="x-p"/>\n', result)
    if oformat == OF_STRONGS:
        # replace strongs tags
        result = re.sub(r'<[^"]+?"strong:H(\d{1,5})">',r'{H\1}', result)
        result = re.sub(r'<[^"]+?"strong:G(\d{1,4})">',r'{G\1}', result)
    if oformat != OF_RAW:    
        # remove all remaining HTML/XML tags
        result = re.sub('<[^>]+>', '', result)
    return result

# get list of verse references from ListKey
def to_list(listKey):
    tlist = []
    for i in range(listKey.getCount()):
        my_key = listKey.getElement(i) 
        tlist.append(my_key.getText())
    return tlist    
    
# build verse list from verse string 
def getKeyTextList(verse_string):
    # verse_string is either a textual bible reference list e. g. "Mat 4:12-5:5, Luk 2:3-4"
    # or is already a ListKey instance, e. g. as a result of bible.doSearch()
    # output is a Python list with all single bible verse references
    if isinstance(verse_string, SW.ListKey):
        tlist = to_list(verse_string)
    else:
        vkey = SW.VerseKey() 
        vlist = vkey.parseVerseList(verse_string, '', True)
        tlist = []
        my_key = vlist.getElement(0)
        while isinstance(my_key, SW.SWKey):
            tlist.append(my_key.getText())
            vlist.increment()
            my_key = vlist.getElement()
    return tlist 
  
# build text output list from verse list 
def getVerseText(modname, verse_string, cvl = CVL_NONE, bcv = BCV_NONE, oformat = OF_PLAIN): 
    result = '' 
    my_lib = SW.SWMgr() 
    bible = my_lib.getModule(modname)
    for item in verse_string.split(","):
        passage = item.strip()
        if passage != '':
            if bcv in [BCV_INPUT, BCV_NUMBER]:
                result += "[" + passage + "]\n"
            for my_key in getKeyTextList(passage): 
                bible.setKeyText(my_key) 
                my_text = stripHTML(bible.renderText().getRawData(), oformat)
                if bcv == BCV_VERSE:
                    my_text = ' [' + my_key + '] ' + my_text
                elif bcv == BCV_NUMBER:
                    my_text = ' [' + re.sub(r'.+\:', '', my_key) + '] ' + my_text
                result += my_text
            if result[-1] != "\n":
                result += "\n"
            if cvl == CVL_SEPARATOR:
                result += "-----------------\n"
            elif cvl == CVL_NEWLINE:
                result += "\n"
    return result 
  
# build verse list from search term 
def getSearchText(modname, search_term, scope = '', output = '', oformat = OF_PLAIN):
    # doSearch() Parameters:
    # * istr string for which to search
    # * flags / posix re options for search 
    #      1 - REG_EXTENDED (use extended regular expressions)
    #      2 - REG_ICASE (perform case insensitive search; supported by most all search types)
    #      4 - REG_NEWLINE (if set, then anchors ^$ do not match at newline, otherwise they do)
    #   flags / Sword specific options
    #   4096 - SWModule::SEARCHFLAG_MATCHWHOLEENTRY
    #   8192 - SWModule::SEARCHFLAG_STRICTBOUNDARIES
    #   By default SWORD defaults to allowing searches to cross the artificial boundaries of verse markers
    #   Searching is done in a sliding window of 2 verses right now.
    #   To turn this off, include SEARCHFLAG_STRICTBOUNDARIES in search flags
    # * scope Key List containing the scope. Example:
    #   scopeList = SW.VerseKey().parseVerseList("Psalms","", True)
    #   result = bible.doSearch("/Word//Lemma./H06862", bible.SEARCHTYPE_ENTRYATTR, 2, scopeList)
    my_lib = SW.SWMgr()
    # Apparently VerseKey and ListKey take some properties from the currently active bible.
    # Experiments showed this to be true for sort ordering and for verse list parsing.
    # Therefore we first instantiate a KJV bible, no matter what was requested through the interface.
    bible = my_lib.getModule('KJV')
    result = SW.ListKey()
    scopeList = SW.VerseKey().parseVerseList(scope,"", True) if scope else None
    # Having created our objects, we now get the bible requested via search interface
    bible = my_lib.getModule(modname)
    strongs = re.findall(r'H0\d{4}|G\d{4}', search_term)
    if strongs:
        search_term = re.sub('H0\d{4}', '', search_term)
        search_term = re.sub('G\d{4}', '', search_term)
        for term in strongs:
            for my_key in to_list(bible.doSearch("Word//Lemma./" + term + "/", SEARCHTYPE_ENTRYATTR, 0, scopeList)):
                result.add(SW.SWKey(my_key))
    if search_term.strip() != '':
        for term in search_term.split(' '):
            for my_key in to_list(bible.doSearch(term, SEARCHTYPE_REGEX, 2, scopeList)):
                result.add(SW.SWKey(my_key))
    # output the results
    result.sort()
    vList = getKeyTextList(result)
    output = output or modname
    restext = ''
    bible = my_lib.getModule(output)
    for item in vList:
        rc = bible.setKeyText(item)
        if bible.getType != 'bible':
            restext += item + ': ' + stripHTML(bible.renderText().c_str() + "\n", oformat)
        else:    
            restext += item + ': ' + stripHTML(bible.renderText().c_str(), oformat)
    return restext    


if __name__ == "__main__":
    print(getSearchText('Vines', 'delight'))
    print(getSearchText('StrongsHebrew', '8173'))
    print(getSearchText('StrongsGreek', '5463'))
    print(getVerseText('KJV', 'Psalms 94:19', bcv=BCV_NUMBER, oformat=OF_RAW))
    print(getSearchText('KJV', 'H08191 H08173', output='KJV', oformat=OF_STRONGS))
