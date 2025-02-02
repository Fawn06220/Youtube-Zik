# coding: utf8
import wx
import time
from time import gmtime, strftime
import os, sys
from os import listdir
from os.path import *
import wx.lib.agw.hyperlink as hl
import threading
from pytubefix import YouTube, Search
from collections import deque
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
from pytubefix.cli import on_progress

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, title, size=wx.Size(515, 790),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX|wx.STAY_ON_TOP)

        #Panel pour affichage
        self.panel = wx.Panel(self,-1)
        self.panel.Fit()
        self.panel.Show()
        
        #On capture l'event de fermeture de l'app
        self.Bind(wx.EVT_CLOSE,self.on_close,self)

        #Crée la barre d'état (en bas).
        self.CreerBarreEtat()

        #Loader
        self.loader = Loader(self,-1,"Download live status !")
        self.loader.Centre()

        #RadioButtons
        self.mp3_b = wx.RadioButton(self.panel,-1, label="Format: m4a (audio only)", style=wx.RB_GROUP)
        self.Bind(wx.EVT_RADIOBUTTON,self.def_mp3,self.mp3_b)
        self.mp4_b = wx.RadioButton(self.panel,-1, label="Format: mp4 (video)")
        self.Bind(wx.EVT_RADIOBUTTON,self.def_mp4,self.mp4_b)

        #ComboBox
        self.choix_qualite = wx.ComboBox(self.panel,-1,choices=["Low Quality","High Quality"],style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.mp4_quality, self.choix_qualite)
        self.choix_qualite.SetSelection(1)
        self.choix_qualite.Disable()

        #CheckBox
        self.sound_off = wx.CheckBox(self.panel,-1,label="Without sound ?")
        self.Bind(wx.EVT_CHECKBOX, self.no_sound, self.sound_off)
        self.sound_off.Disable()
        
        #Boutons
        #Help 
        self.help = wx.Button(self.panel,-1,"Need help ?")
        self.Bind(wx.EVT_BUTTON, self.show_help, self.help)
        self.help.SetForegroundColour("forest Green")
        self.help.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        self.help.SetToolTip(wx.ToolTip('Click if you need help'))

        #More Results
        self.more = wx.Button(self.panel,-1,"Need more ?")
        self.Bind(wx.EVT_BUTTON, self.show_more, self.more)
        self.more.SetForegroundColour("Blue")
        self.more.SetFont(wx.Font(12, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        self.more.SetToolTip(wx.ToolTip('Click to fetch more results'))

        #widgets vides
        self.txtVideMemo = wx.StaticText(self.panel,-1,"")
        self.txtVideMemo.SetFont(wx.Font(14, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False, "Impact" ))
        self.txtVideMemo.SetForegroundColour(wx.RED)
        
        #widgets
        #Music
        self.txtMus = wx.StaticText(self.panel,-1,"Search on YouTube :")
        self.txtMus.SetFont(wx.Font(11, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False ))

        #Music field
        self.txtBox = wx.TextCtrl(self.panel,-1,size=(300,25),style=wx.TE_PROCESS_ENTER)
        self.txtBox.SetFont(wx.Font(11, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False ))
        self.txtBox.SetHint("Type music/album/artist name here...")
        self.Bind(wx.EVT_TEXT_ENTER,self.get_music,self.txtBox)
        
        #Output
        self.AffichTxt = wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.BORDER_SUNKEN,size=(440,350))
        self.AffichTxt.InsertColumn(0, "MUSIC TITLES",width=440)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.no_resize, self.AffichTxt)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.download, self.AffichTxt)
        
        #Donate
        self.txt_don = wx.StaticText(self.panel,-1,"Link to Dev's Paypal.me :")

        self.Lien_don = hl.HyperLinkCtrl(self.panel, wx.ID_ANY, 'Thanks if you donate <3',URL="http://paypal.me/noobpythondev")
        self.Lien_don.SetLinkCursor(wx.CURSOR_HAND)
        self.Lien_don.SetUnderlines(False, False, True)
        self.Lien_don.EnableRollover(True)
        self.Lien_don.SetColours("BLUE", "ORANGE", "BLUE")
        self.Lien_don.SetBold(True)
        self.Lien_don.SetToolTip(wx.ToolTip('Donation link to the no0b Dev ;)'))
        self.Lien_don.UpdateLink()
        
        #Sizer install
        gbox0 = wx.GridBagSizer(10,10)
        gbox0.SetEmptyCellSize((10,10))
        gbox0.Add(self.txt_don,(0,0))
        gbox0.Add(self.Lien_don,(0,1))
        
        #Sizer gestion
        gbox1 = wx.GridBagSizer(10,10)
        gbox1.SetEmptyCellSize((2,2))
        gbox1.Add(self.txtMus,(0,0))
        gbox1.Add(self.txtBox,(0,1))
        gbox1.Add(self.txtVideMemo,(1,1))
        gbox1.Add(self.help,(2,0))
        gbox1.Add(self.more,(2,1))

        #over grid grid
        gtest = wx.GridBagSizer(10,10)
        gtest.SetEmptyCellSize((10,10))
        gtest.Add(self.choix_qualite,(0,0))
        gtest.Add(self.sound_off,(0,1))
        
        #Sizer affichage
        gbox2 = wx.GridBagSizer(10,10)
        gbox2.SetEmptyCellSize((10,10))
        gbox2.Add(self.mp3_b,(0,0))
        gbox2.Add(self.mp4_b,(1,0))
        gbox2.Add(gtest,(2,0))
        gbox2.Add(self.AffichTxt,(3,0))
        
        
        #DONATE
        bsizer0 = self.create_static_box(self.panel, "Donation :", gbox0)
        
        #Zik-DDL
        bsizer1 = self.create_static_box(self.panel, "Youtube-Zik Downloader :", gbox1)

        # Affichage
        bsizer2 = self.create_static_box(self.panel, "Results of YT music search :", gbox2)

        #--------Ajustement du sizer----------
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(bsizer1, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer2, 0,wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(bsizer0, 0,wx.ALL|wx.EXPAND, 10)
        self.panel.SetSizerAndFit(mainSizer)

        #Create dir for mp3 DL if not exixts
        if not os.path.exists('Audio Collection'):
            os.makedirs('Audio Collection')

        #Create dir for mp4 DL if not exixts
        if not os.path.exists('Video Collection'):
            os.makedirs('Video Collection')

        #Initialize vars
        self.test_mp3 = self.mp3_b.GetValue()
        self.choix=1
        self.vid_only = False
        sys.stdout=self.loader.AffichTxt

    def create_static_box(self, panel, title, gbox):
        """Crée une boîte statique avec un titre et un élément interne (gbox)."""
        box = wx.StaticBox(panel, -1, title)
        bsizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gbox, 0, wx.ALL | wx.CENTER, 10)
        bsizer.Add(sizer, 1, wx.EXPAND, 0)
        return bsizer

    #Threads wrapper usage : mark @threaded over differents threads
    def threaded(fn):
        def wrapper(*args, **kwargs):
            threading.Thread(target=fn, args=args, kwargs=kwargs).start()
        return wrapper
        
    def def_mp3(self,evt):
        self.test_mp3 = self.mp3_b.GetValue()
        self.choix_qualite.Disable()
        self.sound_off.Disable()
        evt.Skip()

    def no_sound(self,evt):
        self.vid_only = self.sound_off.IsChecked()
        evt.Skip()
        
    def def_mp4(self,evt):
        self.mp3_b.SetValue(False)
        self.test_mp3 = self.mp3_b.GetValue()
        self.choix_qualite.Enable()
        if self.choix==1:
            self.sound_off.Enable()
        evt.Skip()

    @threaded
    def show_more(self,evt):
        if (self.AffichTxt.IsEmpty()==False):
            self.s.get_next_results()
            self.fetch_q()
        else:
            self.txtVideMemo.SetLabel("Search for music first !")
        evt.Skip()
    
    #Prevents user from resizing columns width
    def no_resize(self,evt):
        evt.Veto()

    @threaded
    def get_music(self,evt):
        if (self.AffichTxt.IsEmpty()==False):
            self.AffichTxt.DeleteAllItems()
        zik = self.txtBox.GetValue()
        if (zik!=""):
            self.txtVideMemo.SetLabel("")
            self.s = Search(zik)
            self.fetch_q()
        else:
            self.txtVideMemo.SetLabel("Search something first !")
        evt.Skip()  

    @threaded
    def fetch_q(self):
        self.liste_urls=deque()
        self.liste_titres=deque()
        liste_all = self.s.videos
        for i in liste_all:
            self.title = i.title
            self.title = self.replace_char(self.title)
            self.liste_titres.appendleft(self.title)
            url = i.watch_url
            self.liste_urls.appendleft(url)
            self.AffichTxt.InsertItem(0,self.title)
            self.color_txt()
        self.check_files()

    def color_txt(self):
        self.AffichTxt.SetTextColour(wx.BLUE)
        
    def check_files(self):
        liste_ziks=[f for f in listdir("Audio Collection") if isfile(join("Audio Collection", f))]
        liste_vids=[f for f in listdir("Video Collection") if isfile(join("Video Collection", f))]
        lst_ziks = [os.path.splitext(x)[0] for x in liste_ziks]
        lst_vids = [os.path.splitext(x)[0] for x in liste_vids]
        for self.title in self.liste_titres:
            self.index=self.AffichTxt.FindItem(-1,self.title)
            if self.title in lst_ziks:
                self.AffichTxt.SetItemTextColour(self.index,"PURPLE")
            if self.title in lst_vids:
                self.AffichTxt.SetItemTextColour(self.index,"FOREST GREEN")
            if self.title in lst_ziks and self.title in lst_vids:
                self.AffichTxt.SetItemTextColour(self.index,wx.RED)
    
    def download(self,evt):
        self.loader.AffichTxt.Clear()
        i_text = evt.GetText()
        self.index=self.AffichTxt.FindItem(-1,i_text)
        url=self.liste_urls[self.index]
        self.yt = YouTube(url,'WEB',on_progress_callback = on_progress)
        test_color = self.AffichTxt.GetItemTextColour(self.index)
        if test_color=="PURPLE":
            Connexion = wx.MessageDialog(self, "You already own this Music !\nDo you want to download the video file(mp4) ?\nDo you want to overwrite the existing MP3 file ?","Warning window",\
            style=wx.ICON_QUESTION|wx.CENTRE|wx.YES_NO|wx.CANCEL,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
            Connexion.SetYesNoLabels('Download MP4 HQ/LQ','Overwrite MP3')
            rep = Connexion.ShowModal() #Affiche le message a l'ecran.
            if rep == wx.ID_YES:
                if (self.test_mp3==False):
                    self.def_mp4(evt)
                    self.dl_vid()
                else:
                    Connexion = wx.MessageDialog(self, "Please configure MP4 Quality and sound !","Alert window",\
                    style=wx.ICON_QUESTION|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
                    rep = Connexion.ShowModal() #Affiche le message a l'ecran.
            if rep == wx.ID_NO:
                self.dl_zik()
            else:
                pass
        elif test_color=="FOREST GREEN":
            Connexion = wx.MessageDialog(self, "You already own this Video !\nDo you want to download the audio file(mp3) ?\nDo you want to overwrite the existing MP4 file ?","Warning window",\
            style=wx.ICON_QUESTION|wx.CENTRE|wx.YES_NO|wx.CANCEL,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
            Connexion.SetYesNoLabels('Download MP3', 'Overwrite MP4 HQ/LQ')
            rep = Connexion.ShowModal() #Affiche le message a l'ecran.
            if rep == wx.ID_YES:
                self.dl_zik()
            if rep == wx.ID_NO:
                if (self.test_mp3==False):
                    self.def_mp4(evt)
                    self.dl_vid()
                else:
                    Connexion = wx.MessageDialog(self, "Please configure MP4 Quality and sound !","Alert window",\
                    style=wx.ICON_QUESTION|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
                    rep = Connexion.ShowModal() #Affiche le message a l'ecran.
            else:
                pass
        elif test_color==wx.RED:
            Connexion = wx.MessageDialog(self, "You already own this Audio and Video !\nDo you want to overwrite MP3 or MP4 ?","Warning window",\
            style=wx.ICON_QUESTION|wx.CENTRE|wx.YES_NO|wx.CANCEL,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
            Connexion.SetYesNoLabels('Overwrite MP3', 'Overwrite MP4 HQ/LQ')
            rep = Connexion.ShowModal() #Affiche le message a l'ecran.
            if rep == wx.ID_YES:
                self.dl_zik()
            if rep == wx.ID_NO:
                if (self.test_mp3==False):
                    self.def_mp4(evt)
                    self.dl_vid()
                else:
                    Connexion = wx.MessageDialog(self, "Please configure MP4 Quality and sound !","Alert window",\
                    style=wx.ICON_QUESTION|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
                    rep = Connexion.ShowModal() #Affiche le message a l'ecran.
            else:
                pass
        else:
            if (self.test_mp3==True):
                self.dl_zik()
            else:
                self.dl_vid()
        evt.Skip()


    def find_most_recent_file(self,directory, extension):
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]
        if not files:
            return None
        most_recent_file = max(files, key=os.path.getctime)
        return most_recent_file

    def mp4_quality(self,evt):
        self.choix = self.choix_qualite.GetSelection()
        if self.choix == 0:
            self.sound_off.Disable()
        else:
            self.sound_off.Enable()
        evt.Skip()

    def replace_char(self,chaine):
        for i in chaine:
            if not i.isalnum() and not i.isspace():
                chaine=chaine.replace(i,'')
        return chaine

    @threaded
    def dl_vid(self):
        self.loader.Show()
        self.yt.title=self.replace_char(self.yt.title)
        if self.choix==1:
            if self.vid_only==True:
                try:
                    video_stream = self.yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
                    video_stream.download("Video Collection")
                except:
                    Connexion = wx.MessageDialog(self, "This video can't be downloaded, try another one please !","Video unavaible",\
                    style=wx.ICON_WARNING|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
                    rep = Connexion.ShowModal() #Affiche le message a l'ecran.
            else:
            #DL video and audio separately for best quality
                try:
                    video_stream = self.yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
                    audio_stream = self.yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
                    video_stream.download()
                    audio_stream.download()
                    audio_file = self.find_most_recent_file(os.getcwd(), '.m4a')
                    video_file = self.find_most_recent_file(os.getcwd(), '.mp4')
                    output_path = os.getcwd()+'\\Video Collection\\'+self.yt.title+'.mp4'
                    ffmpeg_merge_video_audio(video_file,
                             audio_file,
                             output_path,
                             logger=None)
                    os.remove(audio_file)
                    os.remove(video_file)
                except:
                    Connexion = wx.MessageDialog(self, "This video can't be downloaded, try another one please !","Video unavaible",\
                    style=wx.ICON_WARNING|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
                    rep = Connexion.ShowModal() #Affiche le message a l'ecran.
        if self.choix==0:
            try:
                stream = self.yt.streams.get_highest_resolution()
                stream.download("Video Collection")
            except:
                Connexion = wx.MessageDialog(self, "This video can't be downloaded, try another one please !","Video unavaible",\
                style=wx.ICON_WARNING|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
                rep = Connexion.ShowModal() #Affiche le message a l'ecran.
        self.check_files()
        time.sleep(5)
        self.loader.Hide()
        
    @threaded
    def dl_zik(self):
        self.loader.Show()
        try:
            stream = self.yt.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first() #Generates m4a files
            self.yt.title=self.replace_char(self.yt.title)
            stream.download("Audio Collection",filename=self.yt.title+'.m4a')
        except:
            Connexion = wx.MessageDialog(self, "This music can't be downloaded, try another one please !","Music unavaible",\
            style=wx.ICON_WARNING|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
            rep = Connexion.ShowModal() #Affiche le message a l'ecran
        self.check_files()
        time.sleep(5)
        self.loader.Hide()
        
    def show_help(self,evt):
        Connexion = wx.MessageDialog(self, "YouTube Downloader Python V2.1 Notice :"+"\n\n"+"Right click on a BLUE coloured music to download it."+"\n"+"To know when download finished just wait until music title color change !"+"\n"+"If the music is coloured in RED you already have it in the 'Collection''s folder !"+"\n\n"+"Press the 'NEED MORE ?' button to fetch more results !"+"\n\n"+"That's all folks !","Help window",\
        style=wx.ICON_WARNING|wx.CENTRE|wx.OK,pos=wx.DefaultPosition) #Definit les attributs de la fenetre de message.
        rep = Connexion.ShowModal() #Affiche le message a l'ecran.
        evt.Skip()
    
    def Chrono(self):#Chronometre (date )
        stemps = time.strftime("%A %d/%m/%Y") #Definit le format voulu
        self.SetStatusText(stemps,1) #Affiche a droite.
        self.SetStatusText("Developed by François Garbez",0)
    
    def CreerBarreEtat(self):#Creation de la barre d'etat du bas avec l'affichage de la date
        self.CreateStatusBar(2) #Cree une barre de statut (en bas) de deux parties.
        self.SetStatusWidths([-1,150]) #Definit la taille.
        self.Chrono()#Affiche.

    def on_close(self,evt):#On detruit tout :)
        try:
            self.loader.Destroy()
        except:
            pass
        finally:
            self.Destroy()

class Loader(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id, title, wx.DefaultPosition, wx.Size(700, 400),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION|wx.STAY_ON_TOP)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self,-1)
        self.panel.Fit()
        self.panel.Show()
        
        self.txt = wx.StaticText(self.panel,-1,"Downloading or preparing files...Please Wait...")
        #create wx.Font object
        font = wx.Font(14, family = wx.FONTFAMILY_MODERN, style = 0, weight = 90, 
                      underline = False, faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self.txt.SetFont(font)
        
        self.AffichTxt=wx.TextCtrl(self.panel,-1,size=(620,300),style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_AUTO_URL|wx.TE_RICH)
        self.AffichTxt.SetBackgroundColour('BLACK')
        self.AffichTxt.SetFont(wx.Font(10, wx.DEFAULT , wx.NORMAL, wx.NORMAL,False ))
        self.AffichTxt.SetForegroundColour("FOREST GREEN")

        sizer.AddStretchSpacer(1)
        sizer.Add(self.txt, 0, wx.ALIGN_CENTER)
        sizer.Add(self.AffichTxt, 1, wx.ALIGN_CENTER)
        sizer.AddStretchSpacer(1)

        self.panel.SetSizerAndFit(sizer)
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "YoutubeZik DDL V2.2")
        frame.Show(True)
        frame.Centre()
        return True
 
if __name__=='__main__':    
 
    app = MyApp()
    app.MainLoop()



### YoutubeZik DDL V2.2 by François GARBEZ 04/12/2024 Tested on python 3.12 Win11 ###
