import tkinter
import tkinter.messagebox
from tkinter import filedialog, ttk
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from threading import Thread
import time
import string
from tkinter import messagebox
from translation import translate, load_language_setting, CONFIG_FILE

HEIGHT = 720
WIDTH = 1440
HORIZONTAL_PADDING = 70
GAME_BOX_WIDTH_HEIGHT_RATIO = 3
FONT_SIZE = 20  # Increased font size

class TournamentBracketGeneratorFrame:
    def __init__(self, master):
        self.master = master
        # Set the background color once
        #self.background_color = 'lightblue'
        #self.frame = tkinter.Frame(master, bg=self.background_color)
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        self.label = tkinter.Label(self.frame, text=translate("Tournament Bracket Generator"))
        self.label.pack(pady=10)

        self.label_teams = tkinter.Label(self.frame, text=translate("Enter team names below (one per line):"))
        self.label_teams.pack(pady=10)

        self.team_text = tkinter.Text(self.frame, width=50, height=10)
        self.team_text.pack(padx=5, pady=5)

        # Frame for buttons
        self.button_frame = tkinter.Frame(self.frame)
        self.button_frame.pack(pady=10)

        self.generate_bracket_button = tkinter.Button(self.button_frame, text=translate("Generate Bracket"), command=self.generate_and_display_bracket)
        self.generate_bracket_button.pack(side=tkinter.LEFT, padx=10)

        self.save_button = tkinter.Button(self.button_frame, text=translate("Save Bracket"), command=self.save_bracket)
        self.save_button.pack(side=tkinter.LEFT, padx=10)
        self.save_button.pack_forget()  # Initially hide the save button

        self.canvas_frame = tkinter.Frame(self.frame)
        self.canvas_frame.pack(fill=tkinter.BOTH, expand=True)

        self.canvas = tkinter.Canvas(self.canvas_frame, width=WIDTH, height=HEIGHT, scrollregion=(0, 0, WIDTH, HEIGHT))
        self.scrollbar = tkinter.Scrollbar(self.canvas_frame, orient=tkinter.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.bracket_image = None  # Placeholder for generated bracket image

        # Check for initial teams
        self.team_text.bind("<KeyRelease>", self.check_teams_input)

    def check_teams_input(self, event):
        # Enable/disable Generate Bracket button based on text input
        team_input = self.team_text.get("1.0", tkinter.END).strip()
        if team_input:
            self.generate_bracket_button.config(state=tkinter.NORMAL)
        else:
            self.generate_bracket_button.config(state=tkinter.DISABLED)

    def generate_and_display_bracket(self):
        team_input = self.team_text.get("1.0", tkinter.END).strip()
        entered_teams = [team.strip() for team in team_input.split("\n") if team.strip()]
        if len(entered_teams) < 2:
            error_message = translate("error_minimum_teams")
            tkinter.messagebox.showerror("Error", error_message)
            return

        random.shuffle(entered_teams)  # Shuffle the teams

        num_teams = len(entered_teams)
        rounds = int(math.ceil(math.log2(num_teams)))
        bracket_teams = 2 ** rounds

        self.teams = entered_teams + ['BYE'] * (bracket_teams - num_teams)

        bracket_width = WIDTH
        bracket_height = max(HEIGHT, int((2 ** rounds) * 120))

        # Create a new PIL Image object
        bracket_img = Image.new('RGB', (bracket_width, bracket_height), 'white')
        draw = ImageDraw.Draw(bracket_img)

        _size = bracket_teams // 2
        _columns = rounds + 1  # Only need columns for the left side and the center
        _column_width = bracket_width / _columns
        _game_box_width = _column_width - HORIZONTAL_PADDING
        _game_box_height = _game_box_width / GAME_BOX_WIDTH_HEIGHT_RATIO  # Adjusted width-height ratio

        for i in range(_columns):
            side = "LEFT" if i < rounds else "CENTER"

            games = 2 ** (rounds - i)
            x_center = _column_width * (i + 0.5)
            y_size = bracket_height / games  # Adjusted vertical spacing

            for j in range(games):
                y_center = y_size * (j + 0.5)
                draw.rectangle([
                    (x_center - _game_box_width / 2, y_center - _game_box_height / 2),
                    (x_center + _game_box_width / 2, y_center + _game_box_height / 2)
                ], outline="black")

                if i == 0:
                    team_index = j
                    if team_index < len(self.teams):
                        draw.text(
                            (x_center, y_center),
                            self.teams[team_index],
                            fill="black",
                            anchor="mm",
                            font=ImageFont.truetype("arial.ttf", FONT_SIZE)  # Increased font size
                        )

                if i != _columns - 1:
                    draw.line(
                        [(x_center + _game_box_width / 2, y_center),
                         (x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center)],
                        fill="black",
                        width=2
                    )

                if i != 0:
                    draw.line(
                        [(x_center - _game_box_width / 2, y_center),
                         (x_center - _game_box_width / 2 - HORIZONTAL_PADDING / 2, y_center)],
                        fill="black",
                        width=2
                    )

                if j % 2 == 1 and i < rounds:
                    draw.line(
                        [(x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center),
                         (x_center + _game_box_width / 2 + HORIZONTAL_PADDING / 2, y_center - y_size)],
                        fill="black",
                        width=2
                    )

        self.bracket_image = bracket_img  # Store generated bracket image
        self.display_bracket_image()  # Display the generated bracket on the canvas
        self.save_button.pack(side=tkinter.BOTTOM, pady=10)  # Show the save button

    def display_bracket_image(self):
        if self.bracket_image:
            self.canvas.delete("all")  # Clear canvas
            self.canvas.image = ImageTk.PhotoImage(self.bracket_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.canvas.image)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Update scroll region

    def save_bracket(self):
        if self.bracket_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                    initialfile="tournament_bracket.png")  # Set initial file name
            if file_path:
                self.bracket_image.save(file_path)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def destroy(self):
        self.frame.destroy()


class RandomItemPickerFrame:
    def __init__(self, master):
        self.master = master

        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        self.label = tkinter.Label(self.frame, text=translate("Random Item Picker"))
        self.label.pack(pady=10)

        self.label_items = tkinter.Label(self.frame, text=translate("Enter items below (one per line):"))
        self.label_items.pack(pady=10)

        self.item_text = tkinter.Text(self.frame, width=50, height=10)
        self.item_text.pack(padx=5, pady=5)

        self.pick_button = tkinter.Button(self.frame, text=translate("Pick Random Item"), command=self.pick_random_item)
        self.pick_button.pack(pady=10)

        self.remove_button = tkinter.Button(self.frame, text=translate("Remove Picked Item"), command=self.remove_picked_item, state=tkinter.DISABLED)
        self.remove_button.pack(pady=10)

        self.result_label = tkinter.Label(self.frame, text="")
        self.result_label.pack(pady=10)

        self.current_random_item = None

    def pick_random_item(self):
        items_input = self.item_text.get("1.0", tkinter.END).strip()
        items = [item.strip() for item in items_input.split("\n") if item.strip()]
        if not items:
            error_message = translate("Please enter at least one item.")
            tkinter.messagebox.showerror("Error", error_message)
            return

        self.current_random_item = random.choice(items)
        base_text = translate("Randomly picked item:\n")
        self.result_label.config(text=base_text + self.current_random_item)
        self.remove_button.config(state=tkinter.NORMAL)

    def remove_picked_item(self):
        if self.current_random_item:
            items_input = self.item_text.get("1.0", tkinter.END).strip()
            items = [item.strip() for item in items_input.split("\n") if item.strip()]
            items.remove(self.current_random_item)
            self.item_text.delete("1.0", tkinter.END)
            self.item_text.insert(tkinter.END, "\n".join(items))
            self.result_label.config(text="")
            self.remove_button.config(state=tkinter.DISABLED)
            self.current_random_item = None

    def destroy(self):
        self.frame.destroy()

class GroupGeneratorFrame:
    def __init__(self, master):
        self.master = master

        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        self.label = tkinter.Label(self.frame, text=translate("Group Generator"))
        self.label.pack(pady=10)

        self.label_items = tkinter.Label(self.frame, text=translate("Enter names below (one per line):"))
        self.label_items.pack(pady=10)

        self.names_text = tkinter.Text(self.frame, width=50, height=10)
        self.names_text.pack(padx=5, pady=5)

        self.label_group_number = tkinter.Label(self.frame, text=translate("Select number of groups:"))
        self.label_group_number.pack(pady=10)

        self.group_number_var = tkinter.StringVar(value="2")
        self.group_number_spinbox = tkinter.Spinbox(self.frame, from_=2, to=100, textvariable=self.group_number_var)
        self.group_number_spinbox.pack(pady=5)

        # Frame for buttons
        self.button_frame = tkinter.Frame(self.frame)
        self.button_frame.pack(pady=10)

        self.generate_button = tkinter.Button(self.button_frame, text=translate("Generate Groups"), command=self.generate_groups)
        self.generate_button.pack(side=tkinter.LEFT, padx=10)

        self.save_button = tkinter.Button(self.button_frame, text=translate("Save Group Image"), command=self.save_group_image)
        self.save_button.pack(side=tkinter.LEFT, padx=10)
        self.save_button.pack_forget()  # Initially hide the save button

        # Scrollbar and Canvas for displaying groups
        self.canvas_frame = tkinter.Frame(self.frame)
        self.canvas_frame.pack(fill=tkinter.BOTH, expand=True)

        self.scrollbar = tkinter.Scrollbar(self.canvas_frame, orient=tkinter.VERTICAL)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.result_canvas = tkinter.Canvas(self.canvas_frame, bg='white', yscrollcommand=self.scrollbar.set)
        self.result_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.scrollbar.config(command=self.result_canvas.yview)

        self.result_canvas.bind("<Configure>", self.on_canvas_resize)
        self.result_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.group_image = None

    def generate_groups(self):
        names_input = self.names_text.get("1.0", tkinter.END).strip()
        names = [name.strip() for name in names_input.split("\n") if name.strip()]
        if len(names) < 2:
            tkinter.messagebox.showerror("Error", translate("Minimum of two names required."))
            return

        random.shuffle(names)

        group_number = int(self.group_number_var.get())
        groups = [[] for _ in range(group_number)]
        for i, name in enumerate(names):
            groups[i % group_number].append(name)

        self.result_canvas.delete("all")
        self.draw_groups(groups)

        self.group_image = self.create_group_image(groups)  # Store generated group image
        self.display_group_image()  # Display the generated group image
        self.save_button.pack(side=tkinter.LEFT, padx=10)  # Show the save button

    def draw_groups(self, groups):
        if not groups:
            return

        canvas_width = self.result_canvas.winfo_width()
        group_width = 200
        group_height = 40
        padding = 20
        border_width = 2
        row_spacing = 40  # Jarak tambahan antara baris

        max_groups_per_row = 5
        total_rows = (len(groups) + max_groups_per_row - 1) // max_groups_per_row
        row_height = max(len(group) for group in groups) * group_height + padding * 2

        y_offset = 10  # Start drawing from the top with a small margin

        for row in range(total_rows):
            x_offset = (canvas_width - (min(len(groups) - row * max_groups_per_row, max_groups_per_row) * (group_width + padding))) // 2
            for idx in range(max_groups_per_row):
                group_idx = row * max_groups_per_row + idx
                if group_idx >= len(groups):
                    break

                group = groups[group_idx]
                group_box_height = (len(group) + 1) * group_height
                y_center_offset = y_offset + (row_height - group_box_height) // 2

                self.result_canvas.create_rectangle(
                    x_offset, y_center_offset, x_offset + group_width, y_center_offset + group_box_height,
                    outline="black", width=border_width
                )
                self.result_canvas.create_text(
                    x_offset + group_width / 2, y_center_offset + group_height / 2,
                    text=f"Group {group_idx + 1}", anchor="center", font=("Arial", 12, "bold")
                )

                line_y = y_center_offset + group_height
                self.result_canvas.create_line(
                    x_offset + padding, line_y,
                    x_offset + group_width - padding, line_y,
                    fill="black"
                )

                for i, name in enumerate(group):
                    self.result_canvas.create_text(
                        x_offset + group_width / 2, line_y + 10 + group_height * (i + 1),
                        text=name, anchor="center", font=("Arial", 10)
                    )
                x_offset += group_width + padding
            y_offset += row_height + row_spacing

        self.result_canvas.config(scrollregion=self.result_canvas.bbox("all"))  # Update scroll region

    def create_group_image(self, groups):
        font_size = 12
        group_margin = 20
        rectangle_padding = 20
        group_width = 200
        row_spacing = 40  # Jarak tambahan antara baris

        max_groups_per_row = 5
        total_rows = (len(groups) + max_groups_per_row - 1) // max_groups_per_row
        group_height = max(len(group) * font_size * 1.5 for group in groups) + rectangle_padding * 2

        image_width = int(min(len(groups), max_groups_per_row) * (group_width + rectangle_padding) + rectangle_padding)
        image_height = int(total_rows * (group_height + row_spacing) + rectangle_padding * 2)

        image = Image.new("RGB", (image_width, image_height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", font_size)

        for row in range(total_rows):
            x_offset = rectangle_padding
            y_offset = rectangle_padding + row * (group_height + row_spacing)
            for idx in range(max_groups_per_row):
                group_idx = row * max_groups_per_row + idx
                if group_idx >= len(groups):
                    break

                group = groups[group_idx]
                group_box_height = (len(group) + 1) * font_size * 1.5 + rectangle_padding * 2
                y_center_offset = (group_height - group_box_height) // 2 + y_offset

                draw.rectangle(
                    [x_offset, y_center_offset, x_offset + group_width, y_center_offset + group_box_height],
                    outline="black",
                    width=2
                )

                group_name_position = (x_offset + group_width / 2, y_center_offset + group_margin)
                draw.text(group_name_position, f"GROUP {group_idx + 1}", font=font, fill="black", anchor="mm")

                line_y = group_name_position[1] + font_size // 2 + 5
                draw.line(
                    [(x_offset + group_margin, line_y), (x_offset + group_width - group_margin, line_y)],
                    fill="black",
                    width=1
                )

                for i, name in enumerate(group):
                    name_position = (x_offset + group_width / 2, line_y + 10 + font_size * 1.5 * (i + 1))
                    draw.text(name_position, name, font=font, fill="black", anchor="mm")

                x_offset += group_width + rectangle_padding

        return image

    def display_group_image(self):
        if self.group_image:
            self.result_canvas.delete("all")  # Clear canvas
            
            # Get the dimensions of the canvas and the image
            canvas_width = self.result_canvas.winfo_width()
            canvas_height = self.result_canvas.winfo_height()
            image_width, image_height = self.group_image.size
            
            # Calculate the position to center the image on the canvas
            x_center = (canvas_width - image_width) // 2
            y_center = (canvas_height - image_height) // 2
            
            # Debugging: Print canvas and image dimensions
            print(f"Canvas size: {canvas_width}x{canvas_height}, Image size: {image_width}x{image_height}")
            print(f"Centered position: ({x_center}, {y_center})")
            
            # Create the image on the canvas at the centered position
            self.canvas_image = ImageTk.PhotoImage(self.group_image)
            self.result_canvas.create_image(x_center, y_center, anchor="nw", image=self.canvas_image)
            self.result_canvas.config(scrollregion=self.result_canvas.bbox("all"))  # Update scroll region

    def save_group_image(self):
        if self.group_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                    initialfile="group.png")
            if file_path:
                self.group_image.save(file_path)
                
    def on_canvas_resize(self, event):
        self.result_canvas.config(scrollregion=self.result_canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.result_canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        
    def destroy(self):
        self.frame.destroy()
        
class LoadingAnimation:
    def __init__(self, master):
        self.top = tkinter.Toplevel(master)
        self.top.title("Loading")
        self.top.geometry("200x100")
        self.top.transient(master)
        self.top.grab_set()
        
        self.label = tkinter.Label(self.top, text="Processing...", font=("Helvetica", 12))
        self.label.pack(pady=20)

        self.animating = True
        self.thread = Thread(target=self.animate)
        self.thread.start()

    def animate(self):
        while self.animating:
            for char in "|/-\\":
                self.label.config(text=f"Processing... {char}")
                time.sleep(0.1)
                if not self.animating:
                    break

    def stop(self):
        self.animating = False
        self.thread.join()
        self.top.destroy()

class ColorGeneratorFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Coloring Generator"))
        self.label.pack(pady=10)

        self.choose_button = tkinter.Button(self.frame, text=translate("Choose Image"), command=self.choose_file)
        self.choose_button.pack(pady=10)

        self.save_button = tkinter.Button(self.frame, text=translate("Save Image"), command=self.save_image, state=tkinter.DISABLED)
        self.save_button.pack(pady=10)

        self.img_label = None
        self.image = None  # Added image reference

    def apply_random_color_change(self, image_path):
        try:
            with Image.open(image_path) as img:
                img = img.convert("RGBA")
                width, height = img.size

                # Get all unique colors in the image
                unique_colors = set()
                for y in range(height):
                    for x in range(width):
                        unique_colors.add(img.getpixel((x, y)))

                # Generate pastel colors with slight transparency
                def generate_pastel_color():
                    base = 0
                    return (random.randint(base, 255), random.randint(base, 255), random.randint(base, 255), 0)

                # Map each unique color to a new pastel color
                color_map = {color: generate_pastel_color() for color in unique_colors}

                # Apply the new colors to the image
                for y in range(height):
                    for x in range(width):
                        original_color = img.getpixel((x, y))
                        new_color = color_map[original_color]
                        # Blend the new color with the original color
                        blended_color = (
                            (original_color[0] + new_color[0]) // 2,
                            (original_color[1] + new_color[1]) // 2,
                            (original_color[2] + new_color[2]) // 2,
                            255
                        )
                        img.putpixel((x, y), blended_color)

                return img
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")
            return None

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            self.loading_animation = LoadingAnimation(self.master)
            thread = Thread(target=self.process_image, args=(file_path,))
            thread.start()

    def process_image(self, file_path):
        self.image = self.apply_random_color_change(file_path)
        if self.image:
            self.preview_image(self.image)
        self.loading_animation.stop()

    def preview_image(self, img):
        img.thumbnail((400, 400))  # Resize for preview
        img_tk = ImageTk.PhotoImage(img)

        if self.img_label:
            self.img_label.config(image=img_tk)
            self.img_label.image = img_tk
        else:
            self.img_label = tkinter.Label(self.frame, image=img_tk)
            self.img_label.image = img_tk
            self.img_label.pack(pady=10)

        self.save_button.config(state=tkinter.NORMAL)

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                try:
                    self.image.save(save_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showerror("Error", "No image to save.")

    def destroy(self):
        if self.img_label:
            self.img_label.destroy()
        self.frame.destroy()
        
class RandomCardGeneratorFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Card Generator"))
        self.label.pack(pady=10)

        self.generate_button = tkinter.Button(self.frame, text=translate("Generate Random Card"), command=self.generate_card)
        self.generate_button.pack(pady=10)

        # Label to display the card image
        self.card_label = tkinter.Label(self.frame)
        self.card_label.pack(pady=10)

        # Label to display the card description
        self.card_description_label = tkinter.Label(self.frame, text="")
        self.card_description_label.pack(pady=5)

        # Load card images
        self.card_images = {
            "Hearts": {str(i): Image.open(f"images/cards/{i}_of_hearts.png") for i in range(2, 11)} | {
                "Jack": Image.open("images/cards/jack_of_hearts.png"),
                "Queen": Image.open("images/cards/queen_of_hearts.png"),
                "King": Image.open("images/cards/king_of_hearts.png"),
                "Ace": Image.open("images/cards/ace_of_hearts.png")
            },
            "Diamonds": {str(i): Image.open(f"images/cards/{i}_of_diamonds.png") for i in range(2, 11)} | {
                "Jack": Image.open("images/cards/jack_of_diamonds.png"),
                "Queen": Image.open("images/cards/queen_of_diamonds.png"),
                "King": Image.open("images/cards/king_of_diamonds.png"),
                "Ace": Image.open("images/cards/ace_of_diamonds.png")
            },
            "Clubs": {str(i): Image.open(f"images/cards/{i}_of_clubs.png") for i in range(2, 11)} | {
                "Jack": Image.open("images/cards/jack_of_clubs.png"),
                "Queen": Image.open("images/cards/queen_of_clubs.png"),
                "King": Image.open("images/cards/king_of_clubs.png"),
                "Ace": Image.open("images/cards/ace_of_clubs.png")
            },
            "Spades": {str(i): Image.open(f"images/cards/{i}_of_spades.png") for i in range(2, 11)} | {
                "Jack": Image.open("images/cards/jack_of_spades.png"),
                "Queen": Image.open("images/cards/queen_of_spades.png"),
                "King": Image.open("images/cards/king_of_spades.png"),
                "Ace": Image.open("images/cards/ace_of_spades.png")
            }    
        }

    def generate_card(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        suit = random.choice(suits)
        value = random.choice(values)
        card_image = self.card_images[suit][value]
        self.display_image(card_image, f"{value} of {suit}")

    def display_image(self, img, description):
        img.thumbnail((400, 400))  # Resize for preview
        img_tk = ImageTk.PhotoImage(img)

        self.card_label.config(image=img_tk)
        self.card_label.image = img_tk
        
        # Update the card description
        self.card_description_label.config(text=description)

    def destroy(self):
        self.frame.destroy()

class RandomDiceGeneratorFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Dice Generator"))
        self.label.pack(pady=10)

        self.choice_var = tkinter.IntVar(value=1)  # Default to 1 dice

        # Radio buttons for choosing the number of dice (horizontal)
        radio_frame = tkinter.Frame(self.frame)
        radio_frame.pack(pady=5)

        self.one_dice_radio = tkinter.Radiobutton(radio_frame, text=translate("Roll 1 Die"), variable=self.choice_var, value=1)
        self.one_dice_radio.pack(side=tkinter.LEFT, padx=5)

        self.two_dice_radio = tkinter.Radiobutton(radio_frame, text=translate("Roll 2 Dice"), variable=self.choice_var, value=2)
        self.two_dice_radio.pack(side=tkinter.LEFT, padx=5)

        self.roll_button = tkinter.Button(self.frame, text=translate("Roll Dice"), command=self.roll_dice)
        self.roll_button.pack(pady=10)

        self.result_frame = tkinter.Frame(self.frame)  # Frame for displaying dice images
        self.result_frame.pack(pady=10)

        self.count_label = tkinter.Label(self.frame)  # Label to show the results
        self.count_label.pack(pady=5)

        # Load dice images
        self.dice_images = {
            1: Image.open("images/dice/dice_1.png"),
            2: Image.open("images/dice/dice_2.png"),
            3: Image.open("images/dice/dice_3.png"),
            4: Image.open("images/dice/dice_4.png"),
            5: Image.open("images/dice/dice_5.png"),
            6: Image.open("images/dice/dice_6.png")
        }

    def roll_dice(self):
        num_dice = self.choice_var.get()
        
        if num_dice == 1:
            result = random.randint(1, 6)
            dice_image = self.dice_images[result]
            self.display_image(dice_image)
            self.count_label.config(text=f"Result: {result}")
        elif num_dice == 2:
            results = [random.randint(1, 6) for _ in range(2)]
            images = [self.dice_images[result] for result in results]
            total = sum(results)
            self.display_images(images)
            self.count_label.config(text=f"Results: {total}")
        else:
            messagebox.showerror("Error", "Invalid number of dice")

    def display_image(self, img):
        # Clear previous images
        self.clear_images()

        img.thumbnail((200, 200))  # Resize for preview
        img_tk = ImageTk.PhotoImage(img)

        self.result_label = tkinter.Label(self.result_frame, image=img_tk)
        self.result_label.image = img_tk
        self.result_label.pack()

    def display_images(self, imgs):
        # Clear previous images
        self.clear_images()

        for img in imgs:
            img.thumbnail((200, 200))  # Resize for preview
            img_tk = ImageTk.PhotoImage(img)
            label = tkinter.Label(self.result_frame, image=img_tk)
            label.image = img_tk
            label.pack(side=tkinter.LEFT, padx=5)

    def clear_images(self):
        # Remove all widgets from the result_frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

    def destroy(self):
        self.frame.destroy()
        
class RandomCoinGeneratorFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Coin Flipper"))
        self.label.pack(pady=10)

        self.flip_button = tkinter.Button(self.frame, text=translate("Flip Coin"), command=self.flip_coin)
        self.flip_button.pack(pady=10)

        self.result_label = tkinter.Label(self.frame)
        self.result_label.pack(pady=10)

        self.result_text_label = tkinter.Label(self.frame)  # Label to show heads or tails
        self.result_text_label.pack(pady=5)

        # Load coin images
        self.coin_images = {
            "Heads": Image.open("images/coin/head.png"),
            "Tails": Image.open("images/coin/tail.png")
        }

        # Desired size for coin images
        self.desired_size = (200, 200)

    def flip_coin(self):
        result = "Heads" if random.choice([True, False]) else "Tails"
        coin_image = self.coin_images[result]
        self.display_image(coin_image)
        self.result_text_label.config(text=result)

    def display_image(self, img):
        # Resize the image to the desired size
        img = img.resize(self.desired_size, Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        self.result_label.config(image=img_tk)
        self.result_label.image = img_tk

    def destroy(self):
        self.frame.destroy()

class RandomNumberSetGeneratorFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Number Set Generator"))
        self.label.pack(pady=10)

        # Widgets for user input
        self.digit_count_label = tkinter.Label(self.frame, text=translate("Number of Digits:"))
        self.digit_count_label.pack(pady=5)
        self.digit_count_entry = tkinter.Entry(self.frame)
        self.digit_count_entry.pack(pady=5)

        self.num_sets_label = tkinter.Label(self.frame, text=translate("Number of Sets:"))
        self.num_sets_label.pack(pady=5)
        self.num_sets_entry = tkinter.Entry(self.frame)
        self.num_sets_entry.insert(0, "1")  # Default number of sets is 1
        self.num_sets_entry.pack(pady=5)

        self.generate_button = tkinter.Button(self.frame, text=translate("Generate Sets"), command=self.generate_sets)
        self.generate_button.pack(pady=10)

        self.result_text = tkinter.Text(self.frame, height=15)
        self.result_text.pack(pady=10, fill=tkinter.BOTH, expand=True)

    def generate_sets(self):
        try:
            digit_count = int(self.digit_count_entry.get())
            number_of_sets = int(self.num_sets_entry.get())
            
            all_sets = []
            for _ in range(number_of_sets):
                number_set = ''.join(str(random.randint(0, 9)) for _ in range(digit_count))
                all_sets.append(number_set)
            
            self.display_sets(all_sets)
        except ValueError:
            self.result_text.delete(1.0, tkinter.END)
            translated_text = translate("enter_valid_numbers")
            self.result_text.insert(tkinter.END, translated_text)

        
    def display_sets(self, all_sets):
        self.result_text.delete(1.0, tkinter.END)
        for idx, num_set in enumerate(all_sets):
            self.result_text.insert(tkinter.END, f"Set {idx + 1}: {num_set}\n")

    def destroy(self):
        self.frame.destroy()
        
class RandomMazeGeneratorFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Maze Generator"))
        self.label.pack(pady=10)

        # Widgets for user input
        self.width_label = tkinter.Label(self.frame, text=translate("Width:"))
        self.width_label.pack(pady=5)
        self.width_entry = tkinter.Entry(self.frame)
        self.width_entry.pack(pady=5)

        self.height_label = tkinter.Label(self.frame, text=translate("Height:"))
        self.height_label.pack(pady=5)
        self.height_entry = tkinter.Entry(self.frame)
        self.height_entry.pack(pady=5)

        # Frame for the buttons
        self.button_frame = tkinter.Frame(self.frame)
        self.button_frame.pack(pady=10)

        self.generate_button = tkinter.Button(self.button_frame, text=translate("Generate Maze"), command=self.generate_maze)
        self.generate_button.pack(side=tkinter.LEFT, padx=5)

        self.save_button = tkinter.Button(self.button_frame, text=translate("Save Maze"), command=self.save_maze)
        self.save_button.pack(side=tkinter.LEFT, padx=5)
        self.save_button.pack_forget()  # Initially hide the save button

        self.canvas = tkinter.Canvas(self.frame, bg="white")
        self.canvas.pack(pady=10, fill=tkinter.BOTH, expand=True)

        self.maze_image = None

    def generate_maze(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            
            maze_generator = RandomMazeGenerator(width, height)
            maze = maze_generator.generate()

            self.draw_maze(maze)
            self.save_button.pack(side=tkinter.LEFT, padx=5)  # Show the save button after generating a maze
        except ValueError:
            print("Please enter valid numbers for width and height.")
        
    def draw_maze(self, maze):
        self.canvas.delete("all")
        cell_size = 20
        wall_thickness = 3

        img_width = len(maze[0]) * cell_size
        img_height = len(maze) * cell_size

        self.maze_image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(self.maze_image)

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size - wall_thickness, (y + 1) * cell_size - wall_thickness], fill="black")

        # Draw start and end points
        draw.rectangle([0, 0, cell_size - wall_thickness, cell_size - wall_thickness], fill="green")  # Start
        draw.rectangle([(len(maze[0]) - 1) * cell_size, (len(maze) - 1) * cell_size, len(maze[0]) * cell_size - wall_thickness, len(maze) * cell_size - wall_thickness], fill="red")  # End

        # Draw a border around the maze
        draw.rectangle([0, 0, img_width - wall_thickness, img_height - wall_thickness], outline="black", width=wall_thickness)

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.tk_image = ImageTk.PhotoImage(self.maze_image)
        self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, anchor=tkinter.CENTER, image=self.tk_image)
        self.canvas.image = self.tk_image

    def save_maze(self):
        if self.maze_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.maze_image.save(file_path)

    def destroy(self):
        self.frame.destroy()

class RandomMazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1] * width for _ in range(height)]

    def generate(self):
        self._carve_passages_from(0, 0)
        return self.maze

    def _carve_passages_from(self, cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for direction in directions:
            nx, ny = cx + direction[0] * 2, cy + direction[1] * 2
            
            if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 1:
                self.maze[cy + direction[1]][cx + direction[0]] = 0
                self.maze[ny][nx] = 0
                self._carve_passages_from(nx, ny)
    
class RandomColorPickerFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Random Color Picker"))
        self.label.pack(pady=10)

        self.pick_button = tkinter.Button(self.frame, text=translate("Pick Random Color"), command=self.pick_random_color)
        self.pick_button.pack(pady=10)

        self.result_label = tkinter.Label(self.frame, text="", bg="white", width=20, height=2)
        self.result_label.pack(pady=10)

        self.copy_button = tkinter.Button(self.frame, text=translate("Copy Color"), command=self.copy_color_to_clipboard, state=tkinter.DISABLED)
        self.copy_button.pack(pady=10)

    def pick_random_color(self):
        self.color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.result_label.config(text=self.color, bg=self.color)
        self.copy_button.config(state=tkinter.NORMAL)

    def copy_color_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.color)  
        tkinter.messagebox.showinfo("Warning", translate("copied"))
        
    def destroy(self):
        self.frame.destroy()


class RandomPasswordGeneratorFrame:
    def __init__(self, master):
        self.master = master
        
        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)
        
        self.label = tkinter.Label(self.frame, text=translate("Random Password Generator"))
        self.label.pack(pady=10)

        self.length_label = tkinter.Label(self.frame, text=translate("Password Length:"))
        self.length_label.pack(pady=5)
        self.length_entry = tkinter.Entry(self.frame)
        self.length_entry.insert(0, "10")
        self.length_entry.pack(pady=5)

        # Checkboxes for password settings
        self.use_uppercase = tkinter.BooleanVar(value=True)
        self.uppercase_checkbox = tkinter.Checkbutton(self.frame, text=translate("Include Uppercase"), variable=self.use_uppercase)
        self.uppercase_checkbox.pack(pady=5)

        self.use_lowercase = tkinter.BooleanVar(value=True)
        self.lowercase_checkbox = tkinter.Checkbutton(self.frame, text=translate("Include Lowercase"), variable=self.use_lowercase)
        self.lowercase_checkbox.pack(pady=5)

        self.use_digits = tkinter.BooleanVar(value=True)
        self.digits_checkbox = tkinter.Checkbutton(self.frame, text=translate("Include Digits"), variable=self.use_digits)
        self.digits_checkbox.pack(pady=5)

        self.use_special = tkinter.BooleanVar(value=True)
        self.special_checkbox = tkinter.Checkbutton(self.frame, text=translate("Include Special Characters"), variable=self.use_special)
        self.special_checkbox.pack(pady=5)

        self.generate_button = tkinter.Button(self.frame, text=translate("Generate Password"), command=self.generate_password)
        self.generate_button.pack(pady=10)

        self.result_text = tkinter.Text(self.frame, height=5, width=30)
        self.result_text.pack(pady=10)
        
        self.copy_button = tkinter.Button(self.frame, text=translate("Copy Password"), command=self.copy_password_to_clipboard, state=tkinter.DISABLED)
        self.copy_button.pack(pady=10)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length < 1:
                raise ValueError

            # Build character pool based on settings
            characters = ''
            if self.use_uppercase.get():
                characters += string.ascii_uppercase
            if self.use_lowercase.get():
                characters += string.ascii_lowercase
            if self.use_digits.get():
                characters += string.digits
            if self.use_special.get():
                characters += string.punctuation
            
            if not characters:
                raise ValueError("No character types selected")
            
            password = ''.join(random.choice(characters) for _ in range(length))
            self.display_password(password)
        except ValueError:
            self.result_text.delete(1.0, tkinter.END)
            self.result_text.insert(tkinter.END, translate("error_password"))
        
    def display_password(self, password):
        self.result_text.delete(1.0, tkinter.END)
        self.result_text.insert(tkinter.END, password)
        self.copy_button.config(state=tkinter.NORMAL)
    
    def copy_password_to_clipboard(self):
        password = self.result_text.get(1.0, tkinter.END).strip()
        self.master.clipboard_clear()
        self.master.clipboard_append(password)
        messagebox.showinfo("Warning", translate("password_copied"))

    def destroy(self):
        self.frame.destroy()
        
class RandomCoordinateGeneratorFrame:
    def __init__(self, master):
        self.master = master

        self.frame = tkinter.Frame(master)
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        self.label = tkinter.Label(self.frame, text=translate("Random Coordinate Generator"))
        self.label.pack(pady=10)

        self.latitude_label = tkinter.Label(self.frame, text=translate("Latitude Range:"))
        self.latitude_label.pack(pady=5)
        
        self.latitude_frame = tkinter.Frame(self.frame)
        self.latitude_frame.pack(pady=5)
        self.lat_min_entry = tkinter.Entry(self.latitude_frame, width=10)
        self.lat_min_entry.insert(0, "-90")
        self.lat_min_entry.pack(side=tkinter.LEFT, padx=5)
        self.lat_max_entry = tkinter.Entry(self.latitude_frame, width=10)
        self.lat_max_entry.insert(0, "90")
        self.lat_max_entry.pack(side=tkinter.LEFT, padx=5)

        self.longitude_label = tkinter.Label(self.frame, text=translate("Longitude Range:"))
        self.longitude_label.pack(pady=5)

        self.longitude_frame = tkinter.Frame(self.frame)
        self.longitude_frame.pack(pady=5)
        self.lon_min_entry = tkinter.Entry(self.longitude_frame, width=10)
        self.lon_min_entry.insert(0, "-180")
        self.lon_min_entry.pack(side=tkinter.LEFT, padx=5)
        self.lon_max_entry = tkinter.Entry(self.longitude_frame, width=10)
        self.lon_max_entry.insert(0, "180")
        self.lon_max_entry.pack(side=tkinter.LEFT, padx=5)

        self.num_coords_label = tkinter.Label(self.frame, text=translate("Number of Coordinates:"))
        self.num_coords_label.pack(pady=5)
        self.num_coords_entry = tkinter.Entry(self.frame)
        self.num_coords_entry.insert(0, "1")
        self.num_coords_entry.pack(pady=5)

        self.generate_button = tkinter.Button(self.frame, text=translate("Generate Coordinates"), command=self.generate_coordinates)
        self.generate_button.pack(pady=10)

        self.result_text = tkinter.Text(self.frame, height=15)
        self.result_text.pack(pady=10, fill=tkinter.BOTH, expand=True)

        self.copy_button = tkinter.Button(self.frame, text=translate("Copy Coordinates"), command=self.copy_coordinates_to_clipboard, state=tkinter.DISABLED)
        self.copy_button.pack(pady=10)
        
        self.info_label = tkinter.Label(self.frame, text=translate("You can find the location on a coordinate converter"), fg="red")
        self.info_label.pack(pady=10)

    def generate_coordinates(self):
        try:
            lat_min = float(self.lat_min_entry.get())
            lat_max = float(self.lat_max_entry.get())
            lon_min = float(self.lon_min_entry.get())
            lon_max = float(self.lon_max_entry.get())
            num_coords = int(self.num_coords_entry.get())

            if lat_min < -90 or lat_max > 90 or lon_min < -180 or lon_max > 180:
                raise ValueError(translate("coor_error"))

            coordinates = []
            for _ in range(num_coords):
                latitude = random.uniform(lat_min, lat_max)
                longitude = random.uniform(lon_min, lon_max)
                coordinates.append((latitude, longitude))

            self.display_coordinates(coordinates)
        except ValueError as e:
            self.result_text.delete(1.0, tkinter.END)
            self.result_text.insert(tkinter.END, f"Error: {e}")

    def display_coordinates(self, coordinates):
        self.result_text.delete(1.0, tkinter.END)
        for idx, (latitude, longitude) in enumerate(coordinates):
            base_text = translate("coordinate_info")
            # Format the translated text with actual values
            formatted_text = base_text.format(idx=idx + 1, latitude=latitude, longitude=longitude)
            # Insert the formatted text into the result_text widget
            self.result_text.insert(tkinter.END, formatted_text)
        self.copy_button.config(state=tkinter.NORMAL)

    def copy_coordinates_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.result_text.get(1.0, tkinter.END))
        messagebox.showinfo("Warning", translate("coor_copied"))


    def destroy(self):
        self.frame.destroy()