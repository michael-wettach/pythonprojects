#!/usr/bin/python3
# -*- coding: utf-8 -*-
import wx
import SwordFuncs as SF
from bs4 import BeautifulSoup
import re
import requests
import datetime
  

class My_Dialog(wx.Frame):
    
    def __init__(self, *args, **kwargs): 
        super(My_Dialog, self).__init__(*args, **kwargs)
        self.bibleChoice = 'NASB'
        self.InitUI() 
  
    def InitUI(self): 
        ###################################### 
        # Define Menu Bar 
        ###################################### 
  
        menubar = wx.MenuBar() 
  
        ###########################
        # Dropdown menu "File"
        fileMenu = wx.Menu() 
  
        # Add an entry to the dropdown menu 
        fileExit = fileMenu.Append(wx.ID_EXIT, 'Exit', 'Exit application') 
        self.Bind(wx.EVT_MENU, self.OnExit, fileExit) 
  
        # Add the dropdown menu to the menu bar 
        menubar.Append(fileMenu, '&File') 
  
        ###########################
        # Dropdown menu "Bible"
        bibleMenu = wx.Menu()
        
        bibNeue = bibleMenu.Append(wx.ID_ANY, 'NeUe', 'Neue Evangelistische Übersetzung') 
        self.Bind(wx.EVT_MENU, self.OnNeue, bibNeue) 
        
        bibMenge = bibleMenu.Append(wx.ID_ANY, 'Menge', 'Hermann Menge') 
        self.Bind(wx.EVT_MENU, self.OnMenge, bibMenge)
        
        bibNasb = bibleMenu.Append(wx.ID_ANY, 'NASB', 'New American Standard Bible') 
        self.Bind(wx.EVT_MENU, self.OnNasb, bibNasb) 

        menubar.Append(bibleMenu, '&Bibles') 
  
        ###########################
        # Dropdown menu "Settings"
        settingsMenu = wx.Menu()
        
        fmtLarger = settingsMenu.Append(wx.ID_ANY, 'Larger', 'Increase font size') 
        self.Bind(wx.EVT_MENU, self.OnLarger, fmtLarger)
        largeAcc = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('+'), fmtLarger.GetId())
        fmtLarger.SetAccel(largeAcc)
        
        fmtSmaller = settingsMenu.Append(wx.ID_ANY, 'Smaller', 'Decrease font size') 
        self.Bind(wx.EVT_MENU, self.OnSmaller, fmtSmaller)
        smallAcc = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('-'), fmtSmaller.GetId())
        fmtSmaller.SetAccel(smallAcc)
        
        menubar.Append(settingsMenu, '&Settings')
        
        ###########################
        # Dropdown menu Daily Read
        dailyMenu = wx.Menu()
        
        readLos = dailyMenu.Append(wx.ID_ANY, 'Losungen', 'Herrenhuter Tageslesungen') 
        self.Bind(wx.EVT_MENU, self.OnLos, readLos)

        readERF_AT = dailyMenu.Append(wx.ID_ANY, 'ERF Anstoß', 'Gedanken zur Losung') 
        self.Bind(wx.EVT_MENU, self.OnERF_AT, readERF_AT)

        readERF_NT = dailyMenu.Append(wx.ID_ANY, 'ERF Wort zum Tag', 'Gedanken zur Losung') 
        self.Bind(wx.EVT_MENU, self.OnERF_NT, readERF_NT)
        
        readLeben = dailyMenu.Append(wx.ID_ANY, 'Leben ist mehr', 'Tägliche Andachten') 
        self.Bind(wx.EVT_MENU, self.OnLeben, readLeben)
        
        menubar.Append(dailyMenu, '&Daily Read')
  
        ###########################
        self.SetMenuBar(menubar) 
  
        ###################################### 
        # Define Window Panel 
        ###################################### 
  
        panel = wx.Panel(self) 
  
        # The panel is structured by way of "sizers". Each sizer is basically a box. 
        # This is the main sizer containing all other elements and sizers. 
        main_sizer = wx.BoxSizer(wx.VERTICAL) 
  
        # First we add a text display widget at the top of the main box. 
        self.text = wx.TextCtrl(panel, 1000, size=(400, 300), style=wx.TE_MULTILINE | wx.TE_READONLY) 
        main_sizer.Add(self.text, 1, wx.ALL | wx.EXPAND, 5) 
  
        # Beneath the first widget we add an inner box with 2 horizontal elements. 
        sub_sizer = wx.BoxSizer(wx.HORIZONTAL) 
        main_sizer.Add(sub_sizer, 0, wx.TOP | wx.EXPAND,  1) 
  
        # One element is a text entry widget (field) 
        self.text_ctrl = wx.TextCtrl(panel) 
        sub_sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5) 
  
        # The other is a button to trigger some action. 
        my_btn = wx.Button(panel, label='Get Text') 
        my_btn.Bind(wx.EVT_BUTTON, self.OnPress)
        my_btn.SetDefault()
        sub_sizer.Add(my_btn, 0, wx.ALL, 5) 
  
        panel.SetSizer(main_sizer) 
  
        ###################################### 
        # Show Window 
        ###################################### 
  
        self.SetTitle('Basic Sword Bible Test') 
        self.CreateStatusBar() 
        self.Centre() 
        self.Show(True) 

    def formatSoup(self, mytext):
        ftext = mytext.replace("  ", "") 
        ftext = ftext.replace('\r', '') 
        ftext = re.sub(r"([^\d][.!?\)])(\s*[A-Z])",r"\1\n\2",ftext) 
        ftext = re.sub(r"([a-z])([A-Z])",r"\1\n\2",ftext) 
        ftext = ftext.replace("\n\n", "\n") 
        return ftext 

    def OnNeue(self, e): 
        self.bibleChoice = 'GerNeUe'
        self.OnPress(e)
  
    def OnMenge(self, e): 
        self.bibleChoice = 'GerMenge'
        self.OnPress(e)
  
    def OnNasb(self, e): 
        self.bibleChoice = 'NASB'
        self.OnPress(e)
  
    def OnLarger(self, e): 
        curFont = self.text.GetFont()
        curSize = curFont.GetPointSize()
        if curSize < 36:
            curFont.SetPointSize(curSize + 2)
            self.text.SetFont(curFont)
  
    def OnSmaller(self, e): 
        curFont = self.text.GetFont()
        curSize = curFont.GetPointSize()
        if curSize > 8:
            curFont.SetPointSize(curSize - 2)
            self.text.SetFont(curFont)
  
    def OnLos(self, e): 
        url = r"https://www.moravian.org/the-daily-texts/" 
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) 
        html = response.content
        soup = BeautifulSoup(html, features="html.parser")
        widget = soup.find('div', {"class": "widget widget_text", "id": "text-2"})
        div = widget.findAll('div')[1]
        today = div.find('strong')
        title = SF.stripHTML(today.text)
        lesungen = div.find('p')
        passages = ''
        for line in lesungen.text.split("\n"):
            line = line.replace('–', '-')
            citation = re.findall(r"\d?[\. ]?[A-Za-z]+ ?\d{1,3}\:\d{1,3}\-?\d{0,3}\:?\d{0,3}", line)
            for verse in citation:
                passages += verse + ','
        lostext = div.find_all('a')
        value = ''
        for p in lostext:
            value = value + self.formatSoup(p.text) + ','
        self.text_ctrl.SetValue(value + passages)     
        self.OnPress(e)    

    def OnERF_AT(self, e): 
        my_date = datetime.date.today().strftime("%d.%m.%Y")
        url = r"https://erf.de/erf-plus/audiothek/anstoss/72-0"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = response.content
        soup = BeautifulSoup(html, features="html.parser")
        for day in soup.find_all('h3'):
            curday = day.text[0:10]
            if (curday == my_date):
                my_link = day.findNext('a').get('href')
                break
        url = "https://erf.de" + my_link
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = response.content
        soup = BeautifulSoup(html, features="html.parser")
        gedanken = self.formatSoup(soup.find('div', { "class": "col-12"}).text)
        gedanken = re.sub(r".*Bibelvers\n", "", gedanken, flags=re.DOTALL)
        gedanken = re.sub(r"Sie möchten.*", "", gedanken, flags=re.DOTALL)
        gedanken = re.sub(r'([\r\n])[\r\n]+', r'\1', gedanken, flags=re.MULTILINE)
        self.text.SetValue(gedanken)
  
    def OnERF_NT(self, e): 
        my_date = datetime.date.today().strftime("%d.%m.%Y")
        url = r"https://erf.de/erf-plus/audiothek/wort-zum-tag/73?reset=1" 
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) 
        html = response.content 
        soup = BeautifulSoup(html, features="html.parser") 
        for day in soup.find_all('h3'): 
            curday = day.text[0:10] 
            if (curday == my_date): 
                my_link = day.findNext('a').get('href') 
                break 
        url = "https://erf.de" + my_link 
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) 
        html = response.content 
        soup = BeautifulSoup(html, features="html.parser") 
        gedanken = self.formatSoup(soup.find('div', { "class": "col-12"}).text) 
        gedanken = re.sub(r".*Bibelvers\n", "", gedanken, flags=re.DOTALL) 
        gedanken = re.sub(r"Sie möchten.*", "", gedanken, flags=re.DOTALL) 
        gedanken = re.sub(r'([\r\n])[\r\n]+', r'\1', gedanken, flags=re.MULTILINE)
        self.text.SetValue(gedanken)
  
    def OnLeben(self, e): 
        my_date = datetime.date.today().strftime("%d.%m.%Y")
        url = r"https://www.lebenistmehr.de/leben-ist-mehr.html?datum=" + my_date
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) 
        html = response.content 
        soup = BeautifulSoup(html, features="html.parser") 
        box = soup.find('div', { "id": "lim"})
        heading = self.formatSoup(box.find('h1').text)
        passage = self.formatSoup(box.find('a').text)
        self.text_ctrl.SetValue(passage)
        content = box.find('div', { "class", "uk-column-large-1-3 uk-column-medium-1-2 uk-margin-bottom"})
        gedanken = ''
        for paragraph in content.find_all('p'):
            gedanken += SF.stripHTML(paragraph.text)
        gedanken = re.sub(r'Mit dem Autor Kontakt.+', '', gedanken, flags=re.DOTALL)    
        gedanken = re.sub(r'Diesen Artikel.+', '', gedanken, flags=re.DOTALL)    
        self.text.SetValue(gedanken)

    def OnExit(self, e): 
        self.Close() 
  
    def OnPress(self, event):
        value = self.text_ctrl.GetValue()
        if value:
            my_text = SF.getVerseText(self.bibleChoice, value, cvl = SF.CVL_NEWLINE, bcv = SF.BCV_NUMBER)
            self.text.SetValue(my_text) 
  
  
if __name__ == "__main__": 
    ex = wx.App() 
    My_Dialog(None) 
    ex.MainLoop() 
