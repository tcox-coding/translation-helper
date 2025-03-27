import tkinter as tk
from tkinter import filedialog, messagebox
from deep_translator import GoogleTranslator
import json
import os
from utils import deref_multi

class TranslationHelper():
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Translation Helper")
    self.root.geometry("800x600")
    self.root.resizable(False, False)
    
    self.selected_folder = None
    self.create_widgets()
    self.root.mainloop()
  
  def create_widgets(self):
    self.create_menubar()
    self.create_translation_location()
    self.create_translation_text()
    
    self.translate_button = tk.Button(self.root, text="Translate", font=("Arial", 12), command=self.translate)
    self.translate_button.pack()
    
  def create_translation_location(self):
    message = tk.Label(self.root, text="Translation JSON Location", font=("Arial", 14))
    message.pack()
    
    self.translation_location = tk.Entry(self.root, width=50, font=("Arial", 12))
    self.translation_location.insert(0, "example.json.location")
    self.translation_location.pack()
    
  def create_translation_text(self):
    message = tk.Label(self.root, text="Translation Text", font=("Arial", 14))
    message.pack()
    
    self.translation_text = tk.Text(self.root, width=50, height=10, font=("Arial", 12))
    self.translation_text.insert(tk.END, "Example English text to translate")
    self.translation_text.pack()
  
  def create_menubar(self):
    MenuBar = tk.Menu(self.root, tearoff=False) # Create the main menu
    self.root.config(menu=MenuBar)
    
    FileOption = tk.Menu(MenuBar, tearoff=False)
    MenuBar.add_cascade(label="File", menu=FileOption, underline=0)
    
    FileOption.add_command(label="Select .json location", command=self.select_json, accelerator="Ctrl+j")
    FileOption.add_command(label="Quit", command=exit, accelerator="Ctrl+q")
  
  def translate(self):
    print("Translating...")
    # Get the translation text
    translation_text = self.translation_text.get("1.0", "end").strip()
    
    if not self.selected_folder:
      messagebox.showerror("Error", "Please select a .json file location under the File menu")
      return
    
    for root, dir, files in os.walk(self.selected_folder):
      for file in files:
        if file.endswith(".json"):
          lang = file.split(".")[0]
          self.do_translation(translation_text, lang, os.path.join(root, file))
  
  def do_translation(self, text, lang, json_file_location):
    json_location = self.translation_location.get().strip()
    data = None
    
    # Open the already existing json file as a dictionary
    with open(json_file_location, "r", encoding='utf-8') as json_file:
      data = json.load(json_file)
      json_file.close()
    
    # Get to the last location of the json file
    last_loc = json_location.split(".")[-1]
    new_data = data
    
    # Dereference the json location
    for loc in json_location.split("."):
      if loc == last_loc:
        break
      print(json.dumps(new_data), loc)
      if not new_data.get(loc):
        new_data[loc] = {}
      new_data = new_data[loc]
    
    # Do translation
    if lang == 'en':
      new_data[last_loc] = text
    elif lang == 'ukr':
      new_data[last_loc] = GoogleTranslator(source="en", target="uk").translate(text)
    else:
      new_data[last_loc] = GoogleTranslator(source="en", target=lang).translate(text)
      
    # Write the new data to the json file
    with open(json_file_location, "w", encoding='utf-8') as json_file:
      json.dump(data, json_file, indent=2)
      json_file.close()
  
  def select_json(self):
    print("Selecting .json file locations...")
    # Choose the directory
    self.selected_folder = filedialog.askdirectory()
  
if __name__ == "__main__":
  app = TranslationHelper()