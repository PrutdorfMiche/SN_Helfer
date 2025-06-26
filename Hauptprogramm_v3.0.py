# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 15:41:28 2021

@author: Miche
"""

import os
from PIL import Image, ImageEnhance
import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk

bildpfade = []

version = 3.1

def convert_to_jpg(Pfad_read):
    
    Pfad_read_old = Pfad_read
    
    Pfad_read = Pfad_read.replace('ä','ae')
    Pfad_read = Pfad_read.replace('Ä','Ae')
    Pfad_read = Pfad_read.replace('ö','oe')
    Pfad_read = Pfad_read.replace('Ö','Oe')
    Pfad_read = Pfad_read.replace('ü','ue')
    Pfad_read = Pfad_read.replace('Ü','Ue')
    Pfad_read = Pfad_read.replace('ß','ss')
    
    os.rename(Pfad_read_old,Pfad_read)
    
    img = Image.open(Pfad_read)
    
    if Pfad_read[len(Pfad_read)-5:len(Pfad_read)-4] != ".":
        output = Pfad_read[0:len(Pfad_read)-4]+'.jpg'
    else:
        output = Pfad_read[0:len(Pfad_read)-5]+'.jpg'
    
    
    output_img = img.convert('RGB')
    
    output_img.save(output)
    
    #cv2.imwrite(output,img,[int(cv2.IMWRITE_JPEG_QUALITY), 200])
    
    return output

def image_quer_machen(Pfad_read):
    img_old = Image.open(Pfad_read)
    old_size = img_old.size
    

    basewidth = int(16/9*old_size[1])
    baseheight = old_size[1]
    new_size = (basewidth, baseheight)
    img_new = Image.new("RGB", new_size,(255, 255, 255))
    
    
    img_new.paste(img_old, ((new_size[0]-old_size[0])//2,
                          (new_size[1]-old_size[1])//2))
    
    #resize
    (laenge,hoehe) = img_new.size
    laenge_new = 1920
    hoehe_new = int(laenge_new/laenge*hoehe)
    new_size = (laenge_new,hoehe_new)
    img_new = img_new.resize(new_size)
    
    img_new.save(Pfad_read[0:len(Pfad_read)-4]+'_quer'+'.jpg')
    
    return

def image_aufhellen(Pfad_read,faktor = 1.7):
    img_old = Image.open(Pfad_read)
    
    converter = ImageEnhance.Color(img_old)
    
    img_new = converter.enhance(faktor)
    img_new.save(Pfad_read[0:len(Pfad_read)-4]+'_aufgehellt.jpg')
    
    output = Pfad_read[0:len(Pfad_read)-4]+'_aufgehellt.jpg'
    
    return output

def images_nebeneinanderstellen(Bildpfade_neu):
    
    imgs_gesamt = []
    laenge_gesamt = 0
    
    #Größe vereinheitlichen
    for bildpfad in Bildpfade_neu:
        img = Image.open(bildpfad)
        (laenge,hoehe) = img.size
        hoehe_new = 1600
        laenge_new = int(hoehe_new/hoehe*laenge)
        new_size = (laenge_new,hoehe_new)
        img = img.resize(new_size)
        
        laenge_gesamt += laenge_new
        imgs_gesamt.append(img)
    
    #Neues Bild erstellen mit Höhe 1600 und Laenge Gesamt
    size_gesamt = (laenge_gesamt, 1600)
    img_new = Image.new("RGB", size_gesamt,(255, 255, 255))
    
    #Bilder nebeneinander stellen
    laenge_aktuell = 0
    for img in imgs_gesamt:
        img_new.paste(img,(laenge_aktuell,0))
        size = img.size
        laenge_aktuell += size[0]
    
    #resize
    (laenge,hoehe) = img_new.size
    laenge_new = 1920
    hoehe_new = int(laenge_new/laenge*hoehe)
    new_size = (laenge_new,hoehe_new)
    img_new = img_new.resize(new_size)
    
    #Abspeichern
    Pfad_read = Bildpfade_neu[0]
    img_new.save(Pfad_read[0:len(Pfad_read)-4]+'_nebeneinander'+'.jpg')
    
    return 

def starte_konvertierung(Bildpfade,jpg,quer,aufhellen,nebeneinanderstellen):
    
    if not Bildpfade:
        messagebox.showinfo('Fehler','Keiner Bilder ausgewählt')
        return
    
    Bildpfade_neu = []
    
    for bildpfad in Bildpfade:
        
        if jpg:
            try:
                bildpfad = convert_to_jpg(bildpfad)
            except:
                messagebox.showinfo('Fehler','Fehler bei Konvertierung zu jpg')
                root.destroy()
                return
        
        if aufhellen:
            try:
                bildpfad = image_aufhellen(bildpfad)
            except:
                messagebox.showinfo('Fehler','Fehler bei aufhellen')
                root.destroy()
                return
        
        if quer:
            try:
                image_quer_machen(bildpfad)
            except:
                messagebox.showinfo('Fehler','Fehler bei Konvertierung zu quer')
                root.destroy()
                return
            
        Bildpfade_neu.append(bildpfad)
        
    
    
    if nebeneinanderstellen:
            try:
                images_nebeneinanderstellen(Bildpfade_neu)
            except:
                messagebox.showinfo('Fehler','Fehler beim Nebeneinanderstellen der Bilder')
                root.destroy()
                return
            
    anz = str(len(Bildpfade))
    if anz == '1':    
        messagebox.showinfo('Ende',anz +' Bild ' + 'erfolgreich konvertiert')
    else:
        messagebox.showinfo('Ende',anz +' Bilder ' + 'erfolgreich konvertiert')
    
def bilder_auswaehlen():
    global bildpfade
    files = fd.askopenfilenames(parent=root,title='Choose a file')
    bildpfade = list(files)
    
def start_quermachen():
    global bildpfade
    
    #GUI auslesen
    if var1.get() == 1:
        jpg = True
    else:
        jpg = False
        
    if var2.get() == 1:
        quer = True
    else:
        quer = False
        
    if var2.get() == 2:
        nebeneinanderstellen = True
    else:
        nebeneinanderstellen = False
        
    if var3.get() == 1:
        aufhellen = True
    else:
        aufhellen = False
        
    
    starte_konvertierung(bildpfade,jpg,quer,aufhellen,nebeneinanderstellen)
    

#GUI
root = tk.Tk()
root.title("Bilder-Konverter")
root.geometry('600x400')

#buttons
button_auswahl = tk.Button(text="Wähle Bilder aus", command = bilder_auswaehlen)
button_start = tk.Button(text="Start Konvertierung Bilder", command = start_quermachen)

#Seperatoren
separator1 = ttk.Separator(root, orient='horizontal')

#Labels
label_einstellungen = tk.Label(root,text="Allgemeine Einstellungen:")
label_zweck = tk.Label(root,text="Welcher Zweck?")

#checkboxen
var1 = tk.IntVar(value=1)
button_check_jpg = tk.Checkbutton(root,text="In jpg konvertieren",variable = var1)
var3 = tk.IntVar(value=0)
button_check_aufhellen = tk.Checkbutton(root,text="Bilder aufhellen",variable = var3)

var2 = tk.IntVar(value=0)
button_quer = tk.Radiobutton(root,text="Bilder quer machen",variable = var2,value = 1)
button_neben = tk.Radiobutton(root,text="Bilder nebeneinanderstellen",variable = var2,value = 2)
button_ohneZweck = tk.Radiobutton(root,text="Kein Zweck",variable = var2,value = 0)


label_einstellungen.place(relx=0.025,rely=0.025,relwidth=0.25,relheight=0.05)
button_check_jpg.place(relx=0.025,rely=0.1,relwidth=0.45,relheight=0.05)
button_check_aufhellen.place(relx=0.025,rely=0.175,relwidth=0.45,relheight=0.05)

label_zweck.place(relx=0.525,rely=0.025,relwidth=0.25,relheight=0.05)
button_quer.place(relx=0.525,rely=0.1,relwidth=0.45,relheight=0.05)
button_neben.place(relx=0.525,rely=0.175,relwidth=0.45,relheight=0.05)
button_ohneZweck.place(relx=0.525,rely=0.25,relwidth=0.45,relheight=0.05)

separator1.place(relx=0.025,rely=0.45,relwidth=1,relheight=0.025)


button_auswahl.place(relx=0.025,rely=0.5,relwidth=0.45,relheight=0.45)
button_start.place(relx=0.525,rely=0.5,relwidth=0.45,relheight=0.45)


root.mainloop()