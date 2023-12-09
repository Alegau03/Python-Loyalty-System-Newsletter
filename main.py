import tkinter as tk
import yagmail
import time
import pandas
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import PhotoImage
from pymongo import MongoClient
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import csv
######################
client = MongoClient('mongodb://localhost:27017/')
database = client['CarteFedelta']
collection = database['cartefedelta']

password = "yourpassword"
sender = 'youremail@exmaple.com'

######################

def crea_card():
    # Funzione chiamata quando il pulsante "Crea Card" viene premuto
    # Apre una nuova finestra per l'inserimento dei dati
    nuova_finestra = NuovaFinestra(root, database)

class NuovaFinestra(tk.Toplevel):
    # Finestra per l'inserimento dei dati
    def __init__(self, master, database):
        super().__init__(master)
        self.title("Inserisci Dati")
        self.configure(bg='#42a7f5')

        self.database = database

        # Variabili per i dati inseriti
        self.nome_var = tk.StringVar()
        self.cognome_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.indirizzo_var = tk.StringVar()
        self.comune_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # Etichette e campi di input
        tk.Label(self, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.nome_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Cognome:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.cognome_var).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Numero di telefono:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.telefono_var).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Indirizzo:").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.indirizzo_var).grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self, text="Comune di residenza:").grid(row=4, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.comune_var).grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self, text="Email:").grid(row=5, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.email_var).grid(row=5, column=1, padx=10, pady=10)

        # Pulsante di conferma
        ttk.Button(self, text="Conferma", command=self.conferma_inserimento).grid(row=6, column=0, columnspan=2, pady=20)

    def conferma_inserimento(self):
        # Funzione chiamata quando il pulsante di conferma viene premuto
        # Salva i dati nel database e l'email nel file CSV, poi chiude la finestra
        nome = self.nome_var.get()
        cognome = self.cognome_var.get()
        telefono = self.telefono_var.get()
        indirizzo = self.indirizzo_var.get()
        comune = self.comune_var.get()
        email = self.email_var.get()

        # Verifica che tutti i campi siano stati riempiti
        if not nome or not cognome or not telefono or not indirizzo or not comune or not email:
            messagebox.showerror("Errore", "Riempi tutti i campi!")
            return
        img = Image.open('CartaBasic.png')
        I1 = ImageDraw.Draw(img)
        mf = ImageFont.truetype('FreeMono.otf', 70)
        text = nome+" "+cognome
        textsave= nome+cognome
        I1.text((10, 10), text , fill =(255, 255, 0),font=mf)
        img.save("cards/"+textsave+".png")
        
        send_first_email(nome,cognome,email)
        # Salva i dati nel database
        nuovo_record = {
            "Nome": nome,
            "Cognome": cognome,
            "NumeroTelefono": telefono,
            "Indirizzo": indirizzo,
            "ComuneResidenza": comune,
            "Email": email,
            "Punti": 0  # Inizializza Punti a 0
        }

        self.database.collection.insert_one(nuovo_record)

        # Salva l'email nel file CSV
        with open('Emails.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Scrive l'email
            writer.writerow([email])

        # Chiudi la finestra
        self.destroy()

def cerca_card():
    # Funzione chiamata quando il pulsante "Cerca Card" viene premuto
    # Apre una nuova finestra per la ricerca di una carta
    ricerca_finestra = RicercaFinestra(root, database, DettagliFinestra)

class RicercaFinestra(tk.Toplevel):
    # Finestra per la ricerca di una carta
    def __init__(self, master, database, dettagli_finestra_cls):
        super().__init__(master)
        self.title("Cerca Card")
        self.configure(bg='#42a7f5')

        self.database = database
        self.dettagli_finestra_cls = dettagli_finestra_cls

        # Variabili per i dati inseriti
        self.nome_var = tk.StringVar()
        self.cognome_var = tk.StringVar()
        self.telefono_var = tk.StringVar()

        # Etichette e campi di input
        tk.Label(self, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.nome_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Cognome:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.cognome_var).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Numero di telefono:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self, textvariable=self.telefono_var).grid(row=2, column=1, padx=10, pady=10)

        # Pulsante di ricerca
        ttk.Button(self, text="Cerca", command=self.esegui_ricerca).grid(row=3, column=0, columnspan=2, pady=20)

    def esegui_ricerca(self):
        # Funzione chiamata quando il pulsante "Cerca" viene premuto
        # Esegue una ricerca nel database e mostra i risultati in una nuova finestra
        nome = self.nome_var.get()
        cognome = self.cognome_var.get()
        telefono = self.telefono_var.get()

        # Verifica che tutti i campi siano stati riempiti
        if not nome or not cognome or not telefono:
            messagebox.showerror("Errore", "Riempi tutti i campi!")
            return

        # Esegui la query nel database
        query = {
            "Nome": nome,
            "Cognome": cognome,
            "NumeroTelefono": telefono
        }

        risultato = self.database.collection.find_one(query)

        if risultato:
            # Se trovato, mostra i dettagli in una nuova finestra
            DettagliFinestra(self, self.database, risultato)
        else:
            messagebox.showinfo("Nessuna carta trovata", "Nessuna carta trovata con i dati forniti")

class DettagliFinestra(tk.Toplevel):
    # Finestra per mostrare i dettagli di una carta
    def __init__(self, master, database, dettagli):
        super().__init__(master)
        self.title("Dettagli Carta")
        self.geometry("500x500")
        self.configure(bg='#42a7f5')

        # Mostra i dettagli
        for indice, (chiave, valore) in enumerate(dettagli.items()):
            tk.Label(self, text=f"{chiave}:").grid(row=indice, column=0, padx=10, pady=5)
            tk.Label(self, text=valore).grid(row=indice, column=1, padx=10, pady=5)

        # Variabile per i punti
        self.punti_var = tk.StringVar(value=str(dettagli.get("Punti", 0)))

        # Etichetta per mostrare i punti
        tk.Label(self, text="Punti:").grid(row=indice+1, column=0, padx=10, pady=5)
        tk.Label(self, textvariable=self.punti_var).grid(row=indice+1, column=1, padx=10, pady=5)

        # Pulsanti per gestire i punti
        ttk.Button(self, text="Aggiungi Punto", command=self.aggiungi_punto).grid(row=indice+2, column=0, padx=10, pady=20, sticky="w")
        ttk.Button(self, text="Togli Punto", command=self.togli_punto).grid(row=indice+2, column=1, padx=10, pady=20, sticky="w")
        ttk.Button(self, text="Azzera Punti", command=self.azzera_punti).grid(row=indice+2, column=2, padx=10, pady=20, sticky="e")

        # Aggiungi una variabile 'dettagli' all'istanza della finestra
        self.dettagli = dettagli
        self.database = database

    def aggiorna_punti(self, nuovi_punti):
        # Funzione chiamata per aggiornare i punti visualizzati
        self.punti_var.set(str(nuovi_punti))

    def aggiungi_punto(self):
        # Funzione chiamata quando il pulsante "Aggiungi Punto" viene premuto
        punti_attuali = int(self.punti_var.get())
        nuovi_punti = punti_attuali + 1
        self.aggiorna_punti(nuovi_punti)
        # Aggiorna i punti nel database
        self.database.collection.update_one(
            {"_id": self.dettagli['_id']},
            {"$set": {"Punti": nuovi_punti}}
        )

    def togli_punto(self):
        # Funzione chiamata quando il pulsante "Togli Punto" viene premuto
        punti_attuali = int(self.punti_var.get())
        if punti_attuali > 0:
            nuovi_punti = punti_attuali - 1
            self.aggiorna_punti(nuovi_punti)
            # Aggiorna i punti nel database
            self.database.collection.update_one(
                {"_id": self.dettagli['_id']},
                {"$set": {"Punti": nuovi_punti}}
            )
        else:
            messagebox.showinfo("Attenzione", "I punti sono già a zero.")

    def azzera_punti(self):
        # Funzione chiamata quando il pulsante "Azzera Punti" viene premuto
        self.aggiorna_punti(0)
        # Aggiorna i punti nel database
        self.database.collection.update_one(
            {"_id": self.dettagli['_id']},
            {"$set": {"Punti": 0}}
        )

def send_first_email(nome,cognome,email):
    yag = yagmail.SMTP(user=sender,password=password)
    card = "cards/"+nome+cognome+".png"
    oggetto = "your object" 
    contenuto=f"""
                        your email body
                    """
    yag.send(to=email,subject=oggetto,contents=contenuto,attachments=card)
def newsletter():
    def invia_newsletter():
        contenuto = testo_newsletter.get("1.0", tk.END)  # Ottieni il contenuto dal textfield
        send_newsletter(contenuto)
        finestra_newsletter.destroy()  # Chiudi la finestra dopo l'invio

    # Creazione della finestra per la newsletter
    finestra_newsletter = tk.Toplevel()
    finestra_newsletter.title("Newsletter")
    finestra_newsletter.configure(bg='#42a7f5')

    # Textfield per il contenuto della newsletter
    testo_newsletter = scrolledtext.ScrolledText(finestra_newsletter, wrap=tk.WORD, width=40, height=10)
    testo_newsletter.grid(row=0, column=0, padx=10, pady=10)

    # Bottone per inviare la newsletter
    invia_button = ttk.Button(finestra_newsletter, text="Invia", command=invia_newsletter)
    invia_button.grid(row=1, column=0, pady=10)



def send_newsletter(body):
    
    
    yag = yagmail.SMTP(user=sender,password=password)
    oggetto = "Object!"
    df= pandas.read_csv('Emails.csv')
    contenuto= body
    for index,row in df.iterrows():
       
        yag.send(to=row['email'],subject=oggetto,contents=contenuto)
    

# Creazione della finestra principale
root = tk.Tk()
root.title("Carte Fedeltà")

# Impostazione delle dimensioni della finestra
root.geometry("600x600")

# Impostazione del colore di sfondo
root.configure(bg='#42a7f5')  # 66, 167, 245 in formato esadecimale

# Titolo
titolo_label = tk.Label(root, text="Caffe Italia", font=("Helvetica", 30), bg='#42a7f5')
titolo_label.grid(row=0, column=1, pady=10)

# Foto a sinistra in alto

image = PhotoImage(file='logo.png')
image = image.subsample(15, 15)
foto_label = tk.Label(root, image=image, bg='#42a7f5')
foto_label.grid(row=0, column=0, padx=10, pady=10)

# Pulsanti al centro
crea_card_button = ttk.Button(root, text="Crea Card", command=crea_card, width=20)
crea_card_button.grid(row=1, column=1, pady=20, padx=10)

cerca_card_button = ttk.Button(root, text="Cerca Card", command=cerca_card, width=20)
cerca_card_button.grid(row=2, column=1, pady=20, padx=10)

newsletter_button = ttk.Button(root, text="NewsLetter", command=newsletter, width=20)
newsletter_button.grid(row=3, column=1, pady=20, padx=10)

# Esecuzione dell'app
root.mainloop()
