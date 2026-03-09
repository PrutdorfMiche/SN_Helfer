import os
from PIL import Image, ImageEnhance
import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk

bildpfade = []

VERSION = 3.1

def convert_to_jpg(pfad):
    pfad_clean = pfad.translate(str.maketrans({
        'ä': 'ae', 'Ä': 'Ae',
        'ö': 'oe', 'Ö': 'Oe',
        'ü': 'ue', 'Ü': 'Ue',
        'ß': 'ss'
    }))

    if pfad != pfad_clean:
        os.rename(pfad, pfad_clean)
        pfad = pfad_clean

    img = Image.open(pfad)
    output = pfad.rsplit('.', 1)[0] + '.jpg'
    img.convert('RGB').save(output)
    return output

def image_quer_machen(pfad):
    img_old = Image.open(pfad)
    w, h = img_old.size

    new_w = int(16/9 * h)
    img_new = Image.new("RGB", (new_w, h), (255, 255, 255))
    img_new.paste(img_old, ((new_w - w) // 2, 0))

    resized = img_new.resize((1920, int(1920 / new_w * h)))
    resized.save(pfad.rsplit('.', 1)[0] + '_quer.jpg')

def image_aufhellen(pfad, helligkeit=1.2, saettigung=1.1):
    img = Image.open(pfad).convert("RGB")

    # Erst Farbsättigung erhöhen
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(saettigung)

    # Dann Helligkeit erhöhen
    brightness_enhancer = ImageEnhance.Brightness(img)
    result = brightness_enhancer.enhance(helligkeit)

    output = pfad.rsplit('.', 1)[0] + f'_aufgehellt.jpg'
    result.save(output)
    return output

def images_nebeneinanderstellen(pfade):
    resized_images = []
    total_width = 0
    target_height = 1600

    for pfad in pfade:
        img = Image.open(pfad)
        w, h = img.size
        new_w = int(target_height / h * w)
        resized = img.resize((new_w, target_height))
        resized_images.append(resized)
        total_width += new_w

    combined = Image.new("RGB", (total_width, target_height), (255, 255, 255))
    x_offset = 0
    for img in resized_images:
        combined.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    final = combined.resize((1920, int(1920 / combined.size[0] * combined.size[1])))
    final.save(pfade[0].rsplit('.', 1)[0] + '_nebeneinander.jpg')

def starte_konvertierung(pfade, jpg, quer, aufhellen, nebeneinander, helligkeit=1.2, saettigung=1.1):
    if not pfade:
        messagebox.showinfo('Fehler', 'Keine Bilder ausgewählt')
        return

    neue_pfade = []

    for pfad in pfade:
        try:
            if jpg:
                pfad = convert_to_jpg(pfad)
            if aufhellen:
                pfad = image_aufhellen(pfad, helligkeit, saettigung)
            if quer:
                image_quer_machen(pfad)
            neue_pfade.append(pfad)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei {pfad}:\n{e}")
            return

    if nebeneinander:
        try:
            images_nebeneinanderstellen(neue_pfade)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Zusammenfügen:\n{e}")
            return

    messagebox.showinfo('Erfolg', f'{len(pfade)} Bild(er) erfolgreich verarbeitet.')

def bilder_auswaehlen():
    global bildpfade
    pfade = fd.askopenfilenames(title='Wähle Bilder')
    bildpfade = list(pfade)

def start_quermachen():
    jpg = var1.get() == 1
    aufhellen = var3.get() == 1
    zweck = var2.get()
    quer = zweck == 1
    nebeneinander = zweck == 2
    try:
        helligkeit = float(aufhellfaktor_var.get()) if aufhellen else 1.0
        saettigung = float(saettigung_var.get()) if aufhellen else 1.0
    except ValueError:
        messagebox.showerror("Fehler", "Ungültige Werte für Helligkeit oder Sättigung")
        return
    starte_konvertierung(bildpfade, jpg, quer, aufhellen, nebeneinander, helligkeit, saettigung)

def erstelle_gui():
    global root, var1, var2, var3, aufhellfaktor_var, saettigung_var

    root = tk.Tk()
    root.title("Bilder-Konverter")
    root.geometry('600x400')

    tk.Label(root, text="Allgemeine Einstellungen:").place(relx=0.025, rely=0.025)
    var1 = tk.IntVar(value=1)
    tk.Checkbutton(root, text="In jpg konvertieren", variable=var1).place(relx=0.025, rely=0.1)

    var3 = tk.IntVar(value=0)
    tk.Checkbutton(root, text="Bilder aufhellen", variable=var3).place(relx=0.025, rely=0.175)

    tk.Label(root, text="Welcher Zweck?").place(relx=0.525, rely=0.025)
    var2 = tk.IntVar(value=0)
    tk.Radiobutton(root, text="Bilder quer machen", variable=var2, value=1).place(relx=0.525, rely=0.1)
    tk.Radiobutton(root, text="Bilder nebeneinanderstellen", variable=var2, value=2).place(relx=0.525, rely=0.175)
    tk.Radiobutton(root, text="Kein Zweck", variable=var2, value=0).place(relx=0.525, rely=0.25)

    ttk.Separator(root, orient='horizontal').place(relx=0.025, rely=0.45, relwidth=1)

    tk.Button(root, text="Wähle Bilder aus", command=bilder_auswaehlen).place(relx=0.025, rely=0.5, relwidth=0.45, relheight=0.45)
    tk.Button(root, text="Start Konvertierung", command=start_quermachen).place(relx=0.525, rely=0.5, relwidth=0.45, relheight=0.45)

    aufhellfaktor_var = tk.StringVar(value="1.5")
    tk.Label(root, text="Helligkeit (z.B. 1.2)").place(relx=0.025, rely=0.25)
    tk.Entry(root, textvariable=aufhellfaktor_var).place(relx=0.025, rely=0.3, relwidth=0.2)

    saettigung_var = tk.StringVar(value="1.3")
    tk.Label(root, text="Sättigung (z.B. 1.1)").place(relx=0.275, rely=0.25)
    tk.Entry(root, textvariable=saettigung_var).place(relx=0.275, rely=0.3, relwidth=0.2)

    root.mainloop()

if __name__ == "__main__":
    erstelle_gui()
