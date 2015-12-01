#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# mm2dm - Mind Manager to Markdown file converter

import lxml.etree as etree
import sys
import zipfile

NS = "{http://schemas.mindjet.com/MindManager/Application/2003}"

def initlog():
    import logging
    logger = logging.getLogger()
    hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)

def main():
    mm2md(sys.argv[1])
    

def mm2md(filename):
    if not filename.endswith(".mmap"):
        LOG.error("file extension error")
        return

    f = open(filename, 'r')
    z = zipfile.ZipFile(f)
    content = z.read("Document.xml")
    dom = etree.fromstring(content)
    oneTopic = dom.find(NS+'OneTopic')

    fout = open(filename.replace(".mmap",".md"),'w')
    processTopic(oneTopic.find(NS+'Topic'),fout,0)
    fout.flush()
    fout.close()

def mdLevel(str,level):
    return '#'*(level+1)+' '+str.encode("utf8")+'\n'

def processTopic(topic,fout,level):
    text = topic.find(NS+'Text')
    if text!=None:
        fout.write(mdLevel(text.get('PlainText'),level))
    notesGroup = topic.find(NS+'NotesGroup')
    if notesGroup!=None:
        fout.write(notesGroup.find(NS+'NotesXhtmlData').get('PreviewPlainText').encode('utf8')+'\n')
    subtopics = topic.find(NS+'SubTopics')
    if subtopics!=None:
        for subtopic in subtopics:
            processTopic(subtopic,fout,level+1)

if __name__ == "__main__":
    main()