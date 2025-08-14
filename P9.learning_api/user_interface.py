import tkinter as tk
from tkinter import ttk
from spotify import search_loop, get_songs
from PIL import ImageTk, Image
import urllib.request
import io
import base64
   
##unfinished program##

def main():
    app = Application()
    app.mainloop()

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.geometry('700x500')

        frame = InputForm(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        

class InputForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=3)
        self.rowconfigure(2, weight=1)

        self.label = ttk.Label(self, text="Search for an artist")
        self.label.grid(column=0, row=0)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.entry.bind("<Return>", self.show_artist)


        self.entry_btn = ttk.Button(self, text="Enter", command=self.show_artist)
        self.entry_btn.grid(row=1, column=3)

        self.clear_btn = ttk.Button(self, text="Clear", command=self.clear_list)
        self.clear_btn.grid(row=1, column=4)


    def show_artist(self, _event=None):
        text = self.entry.get()
        if text:
            result = search_loop(text)
            #print(result)
            self.entry.delete(0, tk.END)
            #name, followers, genres
            label_text = f"\nName: {result['name']:20}        Followers: {result['followers']['total']}\n "
            self.info_lbl = ttk.Label(self, text=label_text, font=40)
            self.info_lbl.grid(row=2, column=0)
            self.artist_id = result["id"]
            self.create_buttons()

    def create_buttons(self):
        self.top_songs = ttk.Button(self, text="Top Songs", command=self.show_top_songs)
        self.top_songs.grid(row=3, column=0)
        self.albums = ttk.Button(self, text="Albums")
        self.albums.grid(row=3, column=1)

    def show_top_songs(self):
        songs = get_songs(self.artist_id)
        self.show_songs = ttk.Label(self, text=songs, font=16)
        self.show_songs.grid(row=4, column=0)

    # def get_image(self, data):
    #     image = WebImage(data['images'][0]['url']).get()
    #     img_label = ttk.Label(self, image=image, text="Test")
    #     img_label.grid(row=0, column=0)

    def clear_list(self):
        pass


 
if __name__ == "__main__": 
    main()

