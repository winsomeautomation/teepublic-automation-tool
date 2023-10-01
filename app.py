import tkinter
from tkinter import *
from tkinter import Menu
import tkinter.filedialog
import customtkinter
import os
import json
from PIL import Image
import subprocess
import configparser
from datetime import datetime
import pyperclip
import threading

customtkinter.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Message Window
class MessageWindow(customtkinter.CTkToplevel):
    
    def ok_button_pressed(self):
        self.button_pressed = "OK"
        self.destroy()

    def close_button_pressed(self):
        self.button_pressed = "Close"
        self.destroy()

    def __init__(self, title, message):
        super().__init__()

        self.title(title)
        self.geometry("300x150")
        self.maxsize(300, 150)
        self.after(201, lambda : self.iconbitmap('icon.ico'))
        self.focus()
        self.grab_set()

        # Variable to store the button pressed
        self.button_pressed = None
        
        #Message
        self.mw_messagebox = customtkinter.CTkFrame(self, fg_color="transparent")
        self.mw_messagebox.pack(anchor="n", fill=customtkinter.BOTH, expand=True, padx=10, pady=(10, 5))

        self.mw_message = customtkinter.CTkLabel(self.mw_messagebox, text=message, font=customtkinter.CTkFont(size=14), justify="left", wraplength=250)
        self.mw_message.pack(padx=10, pady=10, anchor="w")

        #Footer
        self.mw_footer = customtkinter.CTkFrame(self, fg_color="transparent")
        self.mw_footer.pack(anchor="n", fill=customtkinter.BOTH, padx=10, pady=(5, 10))
        self.mw_footer.grid_columnconfigure((1), weight=1)

        self.mw_ok_button = customtkinter.CTkButton(self.mw_footer, text="OK", font=customtkinter.CTkFont(size=14), width=50, command=self.ok_button_pressed)
        self.mw_ok_button.grid(row=0, column=2, padx=5, pady=5)

        self.mw_close_button = customtkinter.CTkButton(self.mw_footer, text="Close", font=customtkinter.CTkFont(size=14), width=70, fg_color="crimson", command=self.close_button_pressed)
        self.mw_close_button.grid(row=0, column=3, padx=5, pady=5)
        

# Edit Window
class EditWindow(customtkinter.CTkToplevel):

    def __init__(self, container, file_name, folder_path, file_index, list_items):
        super().__init__()

        self.title(file_name)
        self.geometry("600x480")
        self.maxsize(600, 480)
        self.after(201, lambda : self.iconbitmap('icon.ico'))

        self.container = container
        self.file_name = file_name
        self.folder_path = folder_path
        self.file_index = file_index
        self.list_items = list_items

        #Top Level Window Header
        self.tlw_header = customtkinter.CTkFrame(self, height=50)
        self.tlw_header.pack(anchor="n", fill=customtkinter.X, padx=10, pady=(10, 5))

        self.tlw_header_title = customtkinter.CTkLabel(self.tlw_header, text="Details", font=customtkinter.CTkFont(size=20))
        self.tlw_header_title.grid(row=0, column=0, padx=10, pady=10)

        #Top Level Window Container
        self.tlw_container = customtkinter.CTkScrollableFrame(self, height=50)
        self.tlw_container.pack(anchor="n", fill=customtkinter.BOTH, expand=True, padx=10, pady=(5, 5))

        #Title
        self.tlw_container_title_label = customtkinter.CTkLabel(self.tlw_container, text="Title", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_container_title_label.pack(padx=10, pady=0, anchor="w")
        self.tlw_container_title = customtkinter.CTkEntry(self.tlw_container, height=30, border_width=1)
        self.tlw_container_title.pack(padx=10, pady=5, fill=customtkinter.X, expand=True)

        #Description
        self.tlw_container_description_label = customtkinter.CTkLabel(self.tlw_container, text="Description", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_container_description_label.pack(padx=10, pady=0, anchor="w")
        self.tlw_container_description = customtkinter.CTkTextbox(self.tlw_container, height=100, border_width=1, fg_color=["#f9f9fa", "#343638"])
        self.tlw_container_description.pack(padx=10, pady=5, fill=customtkinter.X, expand=True)

        #Primary Tag
        self.tlw_container_ptag_label = customtkinter.CTkLabel(self.tlw_container, text="Primary Tag", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_container_ptag_label.pack(padx=10, pady=0, anchor="w")
        self.tlw_container_ptag = customtkinter.CTkEntry(self.tlw_container, height=30, border_width=1)
        self.tlw_container_ptag.pack(padx=10, pady=5, fill=customtkinter.X, expand=True)

        #Secondary Tag
        self.tlw_container_stag_label = customtkinter.CTkLabel(self.tlw_container, text="Secondary Tags", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_container_stag_label.pack(padx=10, pady=0, anchor="w")
        self.tlw_container_stag = customtkinter.CTkTextbox(self.tlw_container, height=50, border_width=1, fg_color=["#f9f9fa", "#343638"])
        self.tlw_container_stag.pack(padx=10, pady=5, fill=customtkinter.X, expand=True)

        #Settings
        self.tlw_setting_label = customtkinter.CTkLabel(self.tlw_container, text="Settings", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.tlw_setting_label.pack(padx=10, pady=10, anchor="w")

        #Tshirt Settings
        self.tlw_setting_tshirt_label = customtkinter.CTkLabel(self.tlw_container, text="Tshirt", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_setting_tshirt_label.pack(padx=10, pady=0, anchor="w")

        self.tlw_setting_tshirt_frame = customtkinter.CTkFrame(self.tlw_container)
        self.tlw_setting_tshirt_frame.pack(padx=10, pady=0, fill=customtkinter.X)
        self.tlw_setting_tshirt_frame.grid_columnconfigure(6, weight=1)
        
        #Tshirt Color
        self.tlw_tshirt_color_label = customtkinter.CTkLabel(self.tlw_setting_tshirt_frame, text="Color", font=customtkinter.CTkFont(size=14))
        self.tlw_tshirt_color_label.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.tlw_tshirt_color_combobox = customtkinter.CTkComboBox(self.tlw_setting_tshirt_frame, values=["White", "Black"])
        self.tlw_tshirt_color_combobox.grid(row=0, column=1, padx=5, pady=5)

        #Tshirt Side
        self.tlw_tshirt_side_label = customtkinter.CTkLabel(self.tlw_setting_tshirt_frame, text="Side", font=customtkinter.CTkFont(size=14))
        self.tlw_tshirt_side_label.grid(row=0, column=3, padx=5, pady=5)

        self.tlw_tshirt_side_combobox = customtkinter.CTkComboBox(self.tlw_setting_tshirt_frame, values=["Front", "Back", "Both"])
        self.tlw_tshirt_side_combobox.grid(row=0, column=4, padx=5, pady=5)

        #Tshirt Scale
        self.tlw_tshirt_scale_label = customtkinter.CTkLabel(self.tlw_setting_tshirt_frame, text="Scale", font=customtkinter.CTkFont(size=14))
        self.tlw_tshirt_scale_label.grid(row=0, column=5, padx=5, pady=5)

        self.tlw_tshirt_scale = customtkinter.CTkEntry(self.tlw_setting_tshirt_frame, border_width=1)
        self.tlw_tshirt_scale.grid(row=0, column=6, padx=5, pady=5)

        #Hoodie Settings
        self.tlw_setting_hoodie_label = customtkinter.CTkLabel(self.tlw_container, text="Hoodie", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_setting_hoodie_label.pack(padx=10, pady=0, anchor="w")

        self.tlw_setting_hoodie_frame = customtkinter.CTkFrame(self.tlw_container)
        self.tlw_setting_hoodie_frame.pack(padx=10, pady=0, fill=customtkinter.X)
        
        #Hoodie Color
        self.tlw_hoodie_color_label = customtkinter.CTkLabel(self.tlw_setting_hoodie_frame, text="Color", font=customtkinter.CTkFont(size=14))
        self.tlw_hoodie_color_label.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.tlw_hoodie_color_combobox = customtkinter.CTkComboBox(self.tlw_setting_hoodie_frame, values=["Black", "Red"])
        self.tlw_hoodie_color_combobox.grid(row=0, column=1, padx=5, pady=5)

        #Sticker Settings
        self.tlw_setting_sticker_label = customtkinter.CTkLabel(self.tlw_container, text="Sticker", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_setting_sticker_label.pack(padx=10, pady=0, anchor="w")

        self.tlw_setting_sticker_frame = customtkinter.CTkFrame(self.tlw_container)
        self.tlw_setting_sticker_frame.pack(padx=10, pady=0, fill=customtkinter.X)
        
        #Sticker Cut
        self.tlw_sticker_cut_label = customtkinter.CTkLabel(self.tlw_setting_sticker_frame, text="Cut Style", font=customtkinter.CTkFont(size=14))
        self.tlw_sticker_cut_label.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.tlw_sticker_cut_combobox = customtkinter.CTkComboBox(self.tlw_setting_sticker_frame, values=["Auto", "Auto with Background", "Print"])
        self.tlw_sticker_cut_combobox.grid(row=0, column=1, padx=5, pady=5)

        #Magnet Settings
        self.tlw_setting_magnet_label = customtkinter.CTkLabel(self.tlw_container, text="Magnet", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.tlw_setting_magnet_label.pack(padx=10, pady=0, anchor="w")

        self.tlw_setting_magnetframe = customtkinter.CTkFrame(self.tlw_container)
        self.tlw_setting_magnetframe.pack(padx=10, pady=0, fill=customtkinter.X)
        
        #magnet Cut
        self.tlw_magnet_cut_label = customtkinter.CTkLabel(self.tlw_setting_magnetframe, text="Cut Style", font=customtkinter.CTkFont(size=14))
        self.tlw_magnet_cut_label.grid(row=0, column=0, padx=(0, 5), pady=5)

        self.tlw_magnet_cut_combobox = customtkinter.CTkComboBox(self.tlw_setting_magnetframe, values=["Auto", "Auto with Background", "Rectangle", "Circle"])
        self.tlw_magnet_cut_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Create a list of items (you can add more items here)
        # Assuming you have a list of product data, each containing a "name" and a "scale" field
        self.other_product_list = [
            {"name": "Case", "scale": ""},
            {"name": "CoffeeMug", "scale": ""},
            {"name": "TravelMug", "scale": ""},
            {"name": "Print", "scale": ""},
            {"name": "Pillow", "scale": ""},
            {"name": "Tote", "scale": ""},
            {"name": "Pin", "scale": ""},
        ]

        # Create an empty list to store product widgets
        self.product_widgets = []

        # Create repeating list items
        for index, product_data in enumerate(self.other_product_list):
            product_name = product_data["name"]
            product_scale = product_data["scale"]

            #Product
            self.tlw_setting_product_label = customtkinter.CTkLabel(self.tlw_container, text=product_name, font=customtkinter.CTkFont(size=14, weight="bold"))
            self.tlw_setting_product_label.pack(padx=10, pady=0, anchor="w")

            self.tlw_setting_product_frame = customtkinter.CTkFrame(self.tlw_container)
            self.tlw_setting_product_frame.pack(padx=10, pady=0, fill=customtkinter.X)
            
            #Product Scale
            self.tlw_product_scale_label = customtkinter.CTkLabel(self.tlw_setting_product_frame, text="Scale", font=customtkinter.CTkFont(size=14))
            self.tlw_product_scale_label.grid(row=0, column=0, padx=(0, 5), pady=5)

            self.tlw_product_scale = customtkinter.CTkEntry(self.tlw_setting_product_frame, width=100, border_width=1)
            self.tlw_product_scale.grid(row=0, column=1, padx=5, pady=5)
            self.tlw_product_scale.insert(0, product_scale)  # Set the initial value for the scale entry

            # Store the product widgets in the list
            self.product_widgets.append({
                "product_label": self.tlw_setting_product_label,
                "product_scale_entry": self.tlw_product_scale,
            })

        #Top Level Footer
        self.tlw_footer = customtkinter.CTkFrame(self, height=50)
        self.tlw_footer.pack(anchor="n", fill=customtkinter.BOTH, padx=10, pady=(5, 10))
        self.tlw_footer.grid_columnconfigure((1, 2, 3), weight=1)

        self.tlw_footer_savebutton = customtkinter.CTkButton(self.tlw_footer, text="Save", font=customtkinter.CTkFont(size=14), width=70, command=self.save_data)
        self.tlw_footer_savebutton.grid(row=0, column=4, padx=5, pady=10)

        self.tlw_footer_applyallbutton = customtkinter.CTkButton(self.tlw_footer, text="Apply to All", font=customtkinter.CTkFont(size=14), width=70, command=self.apply_all)
        self.tlw_footer_applyallbutton.grid(row=0, column=5, padx=5, pady=10)

        self.tlw_footer_closebutton = customtkinter.CTkButton(self.tlw_footer, text="Close", font=customtkinter.CTkFont(size=14), fg_color="crimson", width=70, command=self.destroy)
        self.tlw_footer_closebutton.grid(row=0, column=6, padx=(5, 10), pady=10)

        #Load the data from Json file if the index matches
        self.load_data()

    def load_data(self):
        # Load existing data from JSON file
        json_file_path = "data.json"  # Change this to the desired file path
        if os.path.exists(json_file_path) and os.stat(json_file_path).st_size > 0:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

        else:
            data = [] 

        # Check if data for the file index is present and update or add accordingly
        for idx, item in enumerate(data):
            if item["index"] == self.file_index:
                
                self.tlw_container_title.insert(0, item["title"])
                self.tlw_container_description.insert(1.0, item["description"])
                self.tlw_container_ptag.insert(0, item["primary_tag"])
                self.tlw_container_stag.insert(1.0, item["secondary_tags"])

                self.tlw_tshirt_color_combobox.set(item["tshirt_color"])
                self.tlw_tshirt_side_combobox.set(item["tshirt_side"])
                self.tlw_tshirt_scale.insert(0, item["tshirt_scale"])
                self.tlw_hoodie_color_combobox.set(item["hoodie_color"])
                self.tlw_sticker_cut_combobox.set(item["sticker_cut"])
                self.tlw_magnet_cut_combobox.set(item["magnet_cut"])

                for index, product_widget in enumerate(self.product_widgets):
                    product_label = product_widget["product_label"].cget("text")
                    product_widget = product_widget["product_scale_entry"]

                    for idx, product in enumerate(item["product_scales"]):
                        if product == product_label:
                            product_widget.insert(0, item["product_scales"][product])
                            break
                    else:
                        print("Not Matched")

                    # scale_entry.insert(0, item["product_scales"][product_widget["product_label"]])

                break
        else:
            print(f"Data with {self.file_index} Not Found...")

    def save_data(self):
        title = self.tlw_container_title.get()
        description = self.tlw_container_description.get("1.0", "end-1c")
        primary_tag = self.tlw_container_ptag.get()
        secondary_tags = self.tlw_container_stag.get("1.0", "end-1c")
        tshirt_color = self.tlw_tshirt_color_combobox.get()
        tshirt_side = self.tlw_tshirt_side_combobox.get()
        tshirt_scale = self.tlw_tshirt_scale.get()
        hoodie_color = self.tlw_hoodie_color_combobox.get()
        sticker_cut = self.tlw_sticker_cut_combobox.get()
        magnet_cut = self.tlw_magnet_cut_combobox.get()

        # Retrieve product scales for all products
        product_scales = {}
        for index, product_widget in enumerate(self.product_widgets):
            scale_entry = product_widget["product_scale_entry"]
            scale_value = scale_entry.get()
            product_name = self.other_product_list[index]["name"]
            product_scales[product_name] = scale_value

        # Create a dictionary with the filled data
        file_path = os.path.join(self.folder_path, self.file_name).replace("\\", "/")

        data = {
            "index": self.file_index,
            "path": file_path,
            "title": title,
            "description": description,
            "primary_tag": primary_tag,
            "secondary_tags": secondary_tags,
            "tshirt_color": tshirt_color,
            "tshirt_side": tshirt_side,
            "tshirt_scale": tshirt_scale,
            "hoodie_color": hoodie_color,
            "sticker_cut": sticker_cut,
            "magnet_cut": magnet_cut,
            "product_scales": product_scales
        }

        # Load existing data from JSON file
        json_file_path = "data.json"  # Change this to the desired file path
        if os.path.exists(json_file_path) and os.stat(json_file_path).st_size > 0:
            with open(json_file_path, "r") as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = []

        # Check if data for the file index is present and update or add accordingly
        index_found = False
        for idx, item in enumerate(existing_data):
            if item["index"] == self.file_index:
                existing_data[idx] = data
                index_found = True
                break

        if not index_found:
            existing_data.append(data)

        # Save the updated data to JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)

        message_box = MessageWindow("Save", "Save Successfully!")
        message_box.wait_window()  # Wait for the window to close

        # Check which button was pressed
        if message_box.button_pressed == "OK":
            self.destroy()

    def apply_all(self):
        title = self.tlw_container_title.get()
        description = self.tlw_container_description.get("1.0", "end-1c")
        primary_tag = self.tlw_container_ptag.get()
        secondary_tags = self.tlw_container_stag.get("1.0", "end-1c")
        tshirt_color = self.tlw_tshirt_color_combobox.get()
        tshirt_side = self.tlw_tshirt_side_combobox.get()
        tshirt_scale = self.tlw_tshirt_scale.get()
        hoodie_color = self.tlw_hoodie_color_combobox.get()
        sticker_cut = self.tlw_sticker_cut_combobox.get()
        magnet_cut = self.tlw_magnet_cut_combobox.get()

        # Retrieve product scales for all products
        product_scales = {}
        for index, product_widget in enumerate(self.product_widgets):
            scale_entry = product_widget["product_scale_entry"]
            scale_value = scale_entry.get()
            product_name = self.other_product_list[index]["name"]
            product_scales[product_name] = scale_value

        json_file_path = "data.json"  # Change this to the desired file path
        with open(json_file_path, "w") as json_file:
            json_file.write('[]')
        
        updated_data = []
        # Process item_bar and create new_data dictionary
        for i, item_bar in enumerate(self.container.grid_slaves()):
            
            file_name = self.list_items[i]
            file_path = os.path.join(self.folder_path, file_name).replace("\\", "/")

            # Create a dictionary with the filled data
            data = {
                "index": i,
                "path": file_path,
                "title": title,
                "description": description,
                "primary_tag": primary_tag,
                "secondary_tags": secondary_tags,
                "tshirt_color": tshirt_color,
                "tshirt_side": tshirt_side,
                "tshirt_scale": tshirt_scale,
                "hoodie_color": hoodie_color,
                "sticker_cut": sticker_cut,
                "magnet_cut": magnet_cut,
                "product_scales": product_scales
            }
            updated_data.append(data)
        
        # Write combined data back to JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(updated_data, json_file, indent=4)  # You can use 'indent' for pretty formatting

        message_box = MessageWindow("Info", "Apply to all Successfully!")
        message_box.wait_window()  # Wait for the window to close

# Setting Window
class SettingWindow(customtkinter.CTkToplevel):

    def onloadWindow(self):
        self.teepublic_email = self.sw_container_email
        self.teepublic_password = self.sw_container_password

        # Create a ConfigParser object
        self.config = configparser.ConfigParser()

        self.config.read("config.ini")
        if self.config.has_section("teepublic"):
            if self.config.has_option("teepublic", "email"):
                email = self.config.get("teepublic", "email")
                self.teepublic_email.insert(0, email)
            
            if self.config.has_option("teepublic", "password"):
                password = self.config.get("teepublic", "password")
                self.teepublic_password.insert(0, password)


    def save_setting(self):
        # If 'teepublic' section already exists, update the values
        if self.config.has_section('teepublic'):
            self.config.set('teepublic', 'email', self.teepublic_email.get())
            self.config.set('teepublic', 'password', self.teepublic_password.get())
        else:
            # Add 'teepublic' section if it doesn't exist
            self.config.add_section('teepublic')
            self.config.set('teepublic', 'email', self.teepublic_email.get())
            self.config.set('teepublic', 'password', self.teepublic_password.get())

        # Write the configuration to a file
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        message_box = MessageWindow("Info", "Saved Successfully!")
        message_box.wait_window()  # Wait for the window to close

        # Check which button was pressed
        if message_box.button_pressed == "OK":
            self.destroy()
    
    def __init__(self):
        super().__init__()

        self.title("Settings")
        self.geometry("600x480")
        self.maxsize(600, 480)
        self.after(201, lambda : self.iconbitmap('icon.ico'))

        #Window Header
        self.sw_header = customtkinter.CTkFrame(self, height=50)
        self.sw_header.pack(anchor="n", fill=customtkinter.X, padx=10, pady=(10, 5))

        self.sw_header_title = customtkinter.CTkLabel(self.sw_header, text="Settings", font=customtkinter.CTkFont(size=20))
        self.sw_header_title.grid(row=0, column=0, padx=10, pady=10)

        #Top Level Window Container

        self.sw_container = customtkinter.CTkFrame(self, height=50)
        self.sw_container.pack(anchor="n", fill=customtkinter.X, expand=True, padx=10, pady=(5, 5))

        #Title
        self.sw_container_title = customtkinter.CTkLabel(self.sw_container, text="Teepublic Account Details", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.sw_container_title.pack(padx=20, pady=(20, 5), anchor="w")

        self.sw_container_description = customtkinter.CTkLabel(self.sw_container, text="Your account details are kept secure and never stored in our databases or the cloud. They are exclusively held in local storage within the software.", font=customtkinter.CTkFont(size=12), justify="left", wraplength=520)
        self.sw_container_description.pack(padx=20, pady=(5, 10), anchor="w")

        self.sw_container_email = customtkinter.CTkEntry(self.sw_container, height=30, border_width=1, placeholder_text="Enter Your Teepublic Account Email")
        self.sw_container_email.pack(padx=20, pady=5, fill=customtkinter.X, expand=True)

        self.sw_container_password = customtkinter.CTkEntry(self.sw_container, height=30, border_width=1, placeholder_text="Enter Your Teepublic Account Password")
        self.sw_container_password.pack(padx=20, pady=5, fill=customtkinter.X, expand=True)

        self.sw_footer_savebutton = customtkinter.CTkButton(self.sw_container, text="Save", font=customtkinter.CTkFont(size=14), width=70, command=self.save_setting)
        self.sw_footer_savebutton.pack(padx=20, pady=(10, 20), fill=customtkinter.X, expand=True)

        self.onloadWindow()

# Top Level Window
class TopLevelWindow(customtkinter.CTkToplevel):

    def copy_to_clipboard(self, address):
        pyperclip.copy(address)
        print(f"Link copied to clipboard: {address}")
     
        message_box = MessageWindow("Info", f"Link Copied to Clipboard!\n{address}")
        message_box.wait_window()  # Wait for the window to close

    def __init__(self, windowTitle):
        super().__init__()

        if windowTitle == "about":

            self.title("About")
            self.geometry("480x360")
            self.maxsize(480, 360)
            self.after(201, lambda : self.iconbitmap('icon.ico'))

            #Window Header
            self.tlw_header = customtkinter.CTkFrame(self, height=50)
            self.tlw_header.pack(anchor="n", fill=customtkinter.X, padx=10, pady=(10, 5))

            self.tlw_header_title = customtkinter.CTkLabel(self.tlw_header, text="About", font=customtkinter.CTkFont(size=20))
            self.tlw_header_title.grid(row=0, column=0, padx=10, pady=10)
            
            #Top Level Window Container
            self.tlw_container = customtkinter.CTkFrame(self, height=50)
            self.tlw_container.pack(anchor="n", fill=customtkinter.BOTH, expand=True, padx=10, pady=(5, 10))
            
            self.tlw_container_description = customtkinter.CTkLabel(self.tlw_container, text="Welcome to the Teepublic Automation Tool! We're dedicated to simplifying and streamlining the process of uploading your designs and configuring various projects on Teepublic. With our user-friendly Python tool, you can now achieve these tasks in a matter of minutes, saving you time and effort. Whether you're a seasoned Teepublic seller or just getting started, our tool is designed to make your experience more efficient and enjoyable.", justify="left", wraplength=420)
            self.tlw_container_description.pack(padx=20, pady=20, anchor="n")
            
        elif windowTitle == "support":
            
            self.title("Support")
            self.geometry("480x360")
            self.maxsize(480, 360)
            self.after(201, lambda : self.iconbitmap('icon.ico'))

            #Window Header
            self.tlw_header = customtkinter.CTkFrame(self, height=50)
            self.tlw_header.pack(anchor="n", fill=customtkinter.X, padx=10, pady=(10, 5))

            self.tlw_header_title = customtkinter.CTkLabel(self.tlw_header, text="Support", font=customtkinter.CTkFont(size=20))
            self.tlw_header_title.grid(row=0, column=0, padx=10, pady=10)
            
            #Top Level Window Container
            self.tlw_container = customtkinter.CTkFrame(self, height=50)
            self.tlw_container.pack(anchor="n", fill=customtkinter.BOTH, expand=True, padx=10, pady=(5, 10))
            
            self.tlw_container_description = customtkinter.CTkLabel(self.tlw_container, text="Your support and feedback are essential in helping us improve the Teepublic Automation Tool and provide you with the best experience possible. Feel free to reach out to us through the following crypto links to show your support or request assistance:", justify="left", wraplength=420)
            self.tlw_container_description.pack(padx=20, pady=(20, 10), anchor="n")

            crypto_addresses = {
                "Bitcoin": "1QDJQWyqGPXewHb5jFqfVRz14Sp6QEkeSf",
                "Ethereum": "0xfe02109ecd649d2f152ecd5c31b8fd79138e4f6d",
                "Litecoin": "LefYbZwex6Fu7jJF9UouNTtAf3PaRB2B1z",
                "USDT": "TPzP6GzBjGhCnSwooRX96SnnZcwMjsN5rJ",
                "BNB": "0xfe02109ecd649d2f152ecd5c31b8fd79138e4f6d"
            }

            for crypto, address in crypto_addresses.items():
                label_text = f"{crypto}: {address}"
                label = customtkinter.CTkLabel(self.tlw_container, text=label_text, font=customtkinter.CTkFont(size=13, weight="bold"), justify="left", cursor="hand2")
                label.pack(padx=30, pady=0, anchor="w")
                label.bind("<Button-1>", lambda e, address=address: self.copy_to_clipboard(address))
     

# Main App Window
class App(customtkinter.CTk):

    def intermediate(self, i):
        for row, item_bar in enumerate(self.container.grid_slaves()):
            current_row = item_bar.grid_info()["row"]
            
            for j, file_name in enumerate(item_bar.grid_slaves()):   
                if isinstance(file_name, customtkinter.CTkLabel):
                    if current_row == i:
                        file_name = file_name.cget('text')
                        self.edit_window(self.container, file_name, i)
                        break

    def edit_window(self, container, file_name, file_index):

        folder_path = self.folder_path
        list_items = self.list_items
        
        if self.editwindow is None or not self.editwindow.winfo_exists():
            self.editwindow = EditWindow(container, file_name, folder_path, file_index, list_items)  # create window if its None or destroyed
            self.editwindow.grab_set()
        else:
            self.editwindow.focus()  # if window exists focus it
            self.editwindow.grab_set()

    def setting_window(self):
        
        if self.settingwindow is None or not self.settingwindow.winfo_exists():
            self.settingwindow = SettingWindow()  # create window if its None or destroyed
            self.settingwindow.grab_set()
        else:
            self.settingwindow.focus()  # if window exists focus it
            self.settingwindow.grab_set()

    def toplevel_window(self, windowTitle):
        
        if self.toplevelwindow is None or not self.toplevelwindow.winfo_exists():
            self.toplevelwindow = TopLevelWindow(windowTitle)  # create window if its None or destroyed
            self.toplevelwindow.grab_set()
        else:
            self.toplevelwindow.focus()  # if window exists focus it
            self.toplevelwindow.grab_set()

    def browse_folder(self):
        self.folder_path = tkinter.filedialog.askdirectory()
        if self.folder_path:
            self.list_items = [
                file for file in os.listdir(self.folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.update_list_items()

            # Clear Json File
            json_file_path = "data.json"
            with open(json_file_path, "w") as json_file:
                json_file.write('[]')
    
    def update_list_items(self):
        # Function to update list items in the GUI
        for widget in self.container.winfo_children():
            widget.destroy()
        
        for index, item_name in enumerate(self.list_items):
            list_item_bar = customtkinter.CTkFrame(self.container,  fg_color=["#c8c8c8", "#2e2e2e"])
            list_item_bar.grid(row=index, column=0, padx=10, pady=(10, 0), sticky="ew")
            list_item_bar.grid_columnconfigure(1, weight=1)

            list_item_thumbnail = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.folder_path, item_name).replace("\\", "/")), size=(30, 30))
            list_item_image = customtkinter.CTkLabel(list_item_bar, image=list_item_thumbnail, text="", width=10)
            list_item_image.grid(row=0, column=0, padx=(10, 5), pady=10)

            list_item_title = customtkinter.CTkLabel(list_item_bar, text=item_name, font=customtkinter.CTkFont(size=14), anchor="w")
            list_item_title.grid(row=0, column=1, padx=5, pady=10)

            row_number = list_item_bar.grid_info()["row"]

            list_item_edit_button = customtkinter.CTkButton(list_item_bar, text="Edit", font=customtkinter.CTkFont(size=14), width=50, command=lambda i=row_number: self.intermediate(i))
            list_item_edit_button.grid(row=0, column=2, padx=5, pady=10, sticky="e")

            self.editwindow = None

            self.list_item_delete_button = customtkinter.CTkButton(list_item_bar, text="Delete", font=customtkinter.CTkFont(size=14), fg_color="crimson", width=50, command=lambda i=row_number: self.remove_item(i))
            self.list_item_delete_button.grid(row=0, column=3, padx=(5, 10), pady=10, sticky="e")

    def remove_item(self, index):

        if 0 <= index < len(self.list_items):
            # Get the list_item_bar associated with the item at the specified index
            list_item_bar = self.container.grid_slaves(row=index)[0]
            list_item_bar.grid_remove()

            # Remove the item from the JSON File
            
            # Load existing data from JSON file
            json_file_path = "data.json"  # Change this to the desired file path
            if os.path.exists(json_file_path) and os.stat(json_file_path).st_size > 0:
                with open(json_file_path, "r") as json_file:
                    existing_data = json.load(json_file)
            else:
                existing_data = []

            # Check if data for the file index is present and update or add accordingly
            for idx, item in enumerate(existing_data):
                if item["index"] == index:
                    existing_data.pop(idx)
                    break
            
            # Update the indices in existing_data for remaining items
            for idx, item in enumerate(existing_data):
                if item["index"] > index:
                    existing_data[idx]["index"] -= 1

            # Save the updated data to JSON file
            with open(json_file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)
                

            # Update grid row values of the remaining widgets
            for row, item_bar in enumerate(self.container.grid_slaves()):
                current_row = item_bar.grid_info()["row"]

                if current_row > index:
                    item_bar.grid_configure(row=current_row - 1)

                for j, edit_button in enumerate(item_bar.grid_slaves()):       
                    if isinstance(edit_button, customtkinter.CTkButton) and edit_button.cget('text') == 'Edit':
                        correction = len(self.container.grid_slaves()) - (row + 1)
                        edit_button.configure(command=lambda i=correction: self.intermediate(i))

                for k, delete_button in enumerate(item_bar.grid_slaves()):       
                    if isinstance(delete_button, customtkinter.CTkButton) and delete_button.cget('text') == 'Delete':
                        correction = len(self.container.grid_slaves()) - (row + 1)
                        delete_button.configure(command=lambda i=correction: self.remove_item(i))

            # Remove the item from the list
            self.list_items.pop(index)
    
    def start_upload(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        email = config.get("teepublic", "email")
        password = config.get("teepublic", "password")

        if email == "" or password == "":
            message_box = MessageWindow("Warning", "Please Set Your Teepublic Email and Password in Setting Menu")
            message_box.wait_window()

        # Check Json data file is empty or not
        elif os.stat("data.json").st_size == 0:
            message_box = MessageWindow("Warning", "There is no files to Upload!")
            message_box.wait_window()
        
        else:
            self.statusbar_status.configure(text="Uploading...")
            # Run the automation script in a separate thread
            automation_thread = threading.Thread(target=self.run_automation)
            automation_thread.start()

    def run_automation(self):
        try:
            # Run the automation script and capture its output
            process = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            for line in process.stdout:
                # Process and display the progress information in your UI
                progress_text = line.strip()
                self.update_progress(progress_text)

            process.wait()

            if process.returncode == 0:
                self.update_progress("ok")
            else:
                self.update_progress("err")
        except Exception as e:
            self.update_progress("exception")

    def update_progress(self, progress_text):
        if progress_text == "ok":
            self.statusbar_status.configure(text="Uploading completed successfully.")
            
            message_box = MessageWindow("Uploading Complete", "Uploading Completed successfully!")
            message_box.wait_window()  # Wait for the window to close
            
        elif progress_text == "err":
            self.statusbar_status.configure(text="Uploading Failed!")

            message_box = MessageWindow("Uploading Failed", "Uploading Failed!")
            message_box.wait_window()  # Wait for the window to close
        
        elif progress_text == "exception":
            self.statusbar_status.configure(text="Something Went Wrong!")
        
        else:
            filename, progress = progress_text.split(",")
            
            self.statusbar_status.configure(text=f"{filename} is Uploaded!")
            self.statusbar_progress.configure(text=progress)
    
    def open_file(self):
        open_file_path = tkinter.filedialog.askopenfilename(
            initialdir='/',
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
            )            

        data = []
        if open_file_path:
            with open(open_file_path, "r") as json_file:
                data = json.load(json_file)
                
                self.list_items = []

                for item in data:
                    if "path" in item:
                        file_path = item["path"]
                        filename = os.path.basename(file_path)
                        self.list_items.append(filename)
        
            self.folder_path = os.path.dirname(file_path)

            # Clear Json File
            json_file_path = "data.json"
            with open(json_file_path, "w") as json_file:
                json_file.write('[]')

            # Save the updated data to JSON file
            with open(json_file_path, "w") as json_file:
                json.dump(data[1:], json_file, indent=4)

            self.update_list_items()

    def save_file(self):
        save_file_path = tkinter.filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
            )

        if save_file_path:
            existing_data = []

            # Load existing data from data.json if it exists
            if os.path.exists("data.json"):
                with open("data.json", "r") as json_file:
                    existing_data = json.load(json_file)

                if not existing_data:
                    print("There is nothing to save...")
                    return

            # Append additional information to existing data
            meta_data = {
                "file_name": os.path.basename(save_file_path),
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "author": os.getlogin(),
                # Add your additional data here
            }

            # Combine new data with existing data
            combined_data = [meta_data] + existing_data

            # Save the combined data to the chosen location
            with open(save_file_path, "w") as json_file:
                json.dump(combined_data, json_file, indent=4)

            print("Data saved successfully!")

    def handle_menu(self, menu_item):
        #File Menu
        if menu_item == "open_file":
            self.open_file()

        elif menu_item == "save":
            self.save_file()
        
        elif menu_item == "add_folder":
            self.browse_folder()
        
        elif menu_item == "setting":
            self.setting_window()
            
        elif menu_item == "exit":
            message_box = MessageWindow("Exit", "Do you really want to exit?")
            message_box.wait_window()  # Wait for the window to close

            # Check which button was pressed
            if message_box.button_pressed == "OK":
                self.destroy()
        
        #Help Menu
        elif menu_item == "about":
            self.toplevel_window(menu_item)
        
        elif menu_item == "support":
            self.toplevel_window(menu_item)

    def __init__(self):
        super().__init__()

        # Configure Window
        self.title("Teepublic Automation | Winsome Designs Automation")
        self.geometry(f"{850}x{480}")
        self.iconbitmap("icon.ico")

        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(label='Add Folder', accelerator="Ctrl+N", command=lambda: self.handle_menu("add_folder"))
        file_menu.add_command(label='Open File...', accelerator="Ctrl+O", command=lambda: self.handle_menu("open_file"))
        file_menu.add_separator()
        file_menu.add_command(label='Save', accelerator="Ctrl+S", command=lambda: self.handle_menu("save"))
        file_menu.add_separator()
        file_menu.add_command(label='Settings', command=lambda: self.handle_menu("setting"))
        file_menu.add_separator()
        file_menu.add_command(label='Exit', accelerator="Alt+F4", command=lambda: self.handle_menu("exit"))

        help_menu = Menu(menubar,  tearoff=0)
        help_menu.add_command(label='About...', command=lambda: self.handle_menu("about"))
        help_menu.add_command(label='Support Us...', command=lambda: self.handle_menu("support"))

        # Add menus to the menubar
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Binding accelerators to root window
        self.bind('<Control-o>', lambda event: self.handle_menu("open_file"))
        self.bind('<Control-s>', lambda event: self.handle_menu("save"))
        self.bind('<Control-n>', lambda event: self.handle_menu("add_folder"))

        #Create Main Menu
        self.main_menu = customtkinter.CTkFrame(self)
        self.main_menu.pack(anchor="n", fill=customtkinter.X, padx=10, pady=(10, 5))

        # Add Buttons into Menu Bar
        self.add_button = customtkinter.CTkButton(self.main_menu, text="+", font=customtkinter.CTkFont(size=20), width=30, height=30, command=self.browse_folder)
        self.add_button.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.upload_button = customtkinter.CTkButton(self.main_menu, text="Start Upload", font=customtkinter.CTkFont(size=14), width=100, height=30, command=self.start_upload)
        self.upload_button.grid(row=0, column=1, padx=5, pady=10)

        #Create Container
        self.list_items = []

        self.container = customtkinter.CTkScrollableFrame(self)
        self.container.pack(anchor="n", fill=customtkinter.BOTH, padx=10, pady=(5, 5), expand=True)
        self.container.grid_columnconfigure((0), weight="1")

        # Create Footer Status Bar
        self.statusbar = customtkinter.CTkFrame(self)
        self.statusbar.pack(anchor="s", fill=customtkinter.X, padx=10, pady=(5, 10))
        self.statusbar.grid_columnconfigure(1, weight=1)

        #Add Elements into Footer Status Bar
        self.statusbar_status_label = customtkinter.CTkLabel(self.statusbar, text="Status:", font=customtkinter.CTkFont(size=14, weight='bold'))
        self.statusbar_status_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.statusbar_status = customtkinter.CTkLabel(self.statusbar, text="Click Start to Upload!", font=customtkinter.CTkFont(size=14))
        self.statusbar_status.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.statusbar_progress_label = customtkinter.CTkLabel(self.statusbar, text="Completed:", font=customtkinter.CTkFont(size=14, weight='bold'))
        self.statusbar_progress_label.grid(row=0, column=2, padx=5, pady=10)

        self.statusbar_progress = customtkinter.CTkLabel(self.statusbar, text="0%", font=customtkinter.CTkFont(size=14))
        self.statusbar_progress.grid(row=0, column=3, padx=(5, 10), pady=10)

        self.settingwindow = None
        self.toplevelwindow = None

        # Clear Json File
        json_file_path = "data.json"
        with open(json_file_path, "w") as json_file:
            json_file.write("")

if __name__ == "__main__":
    app = App()
    app.mainloop()