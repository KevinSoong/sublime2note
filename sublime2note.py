#! /usr/bin/env python
import sys, os
import subprocess
import pickle
#
# Force Python to notice local-embedded Evernote API libs
#
sys.path.append('./lib')
CURRENT_PATH = os.path.abspath('./').replace(' ', '\\ ')
ACCESS_TOKEN_PATH = '.sublime2note-token'

from thrift.transport.THttpClient import THttpClient
from evernote.edam.type.ttypes import Note as EvernoteTypeNote
from evernote.edam.error.ttypes import EDAMUserException
from evernote.api.client import EvernoteClient
from html import XHTML

if __name__ != '__main__':
    try:
        import sublime, sublime_plugin
    except Exception, e:
        print e

settings = sublime.load_settings('Sublime2Note.sublime-settings')

class ResetEvernoteAuthenticationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            os.remove(ACCESS_TOKEN_PATH)
        except Exception, e:
            pass
        sublime.error_message("Sucess: Evernote authentication data is cleared.")

class SaveToEvernoteCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view    
        self.window = sublime.active_window()
        self.note = {}
    def process_note(self):
        region = sublime.Region(0L, self.view.size())
        self.note['content'] = self.view.substr(region)
        self.note['title'] = os.path.basename(self.view.file_name())
        self.note['tags'] = ''
        if settings.get('always_use_filename_as_title'):
            self.send()
        else:
            self.window.show_input_panel('title:','',self.on_title,None,None)
    def on_title(self, title):
        self.note['title'] = title
        if settings.get('always_prompt_for_tags'):
            self.window.show_input_panel('tags:','',self.on_tags,None,None)
        else:
            self.send()
    def on_tags(self, tags):
        self.note['tags'] = tags
        self.send()
    def send(self):
        note = self.note
        xhtml = XHTML()
        n = EvernoteTypeNote()
        n.title = note['title']
        n.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        n.content += '<en-note><pre>%s</pre></en-note>' % xhtml.p(note['content'].encode('utf-8'))
        n.tagNames = [x.strip() for x in note['tags'].split(',') if x.strip()]
        try:
            n = self.noteStore.createNote(n)
        except Exception, e:
            sublime.error_message('Sublime2Note: Failed to create note. Error detail: %s' % e)
        else:
            sublime.status_message('Sucess: Evernote \"%s\" is created.' % note['title'])
    def connect(self, client):
        try:
            noteStore = client.get_note_store()
        except EDAMUserException, e:
            sublime.status_message('Authentication failed: Reconnect to Evernote... %s' % e)
            proc = subprocess.Popen('python %s start' % os.path.join(CURRENT_PATH, 'sublime2note-tool.py'), shell=True)
            return False
        else:
            return noteStore
    def load_token(self):
        if os.path.isfile(ACCESS_TOKEN_PATH):
            with open(ACCESS_TOKEN_PATH) as f:
                return pickle.load(f)
        return ''
    def run(self, edit):
        client = EvernoteClient(token=self.load_token())
        self.noteStore = self.connect(client)
        if self.noteStore:
            self.process_note()