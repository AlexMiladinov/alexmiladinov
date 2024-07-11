import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def load_images_from_directory(directory):
    if not directory:
        return []
    supported_formats = (".png", ".jpg", ".jpeg", ".bmp")
    return [Image.open(os.path.join(directory, file)).convert('RGBA') for file in os.listdir(directory) if file.lower().endswith(supported_formats)]

def apply_overlays(base, overlays):
    result_image = base.copy()
    for overlay in overlays:
        if overlay:
            # Composite overlay onto the base image
            result_image = Image.alpha_composite(result_image, overlay)
    return result_image

def create_variations(overlay_directories, output_dir, num_variations):
    os.makedirs(output_dir, exist_ok=True)
    
    overlay_images = [load_images_from_directory(directory) for directory in overlay_directories]

    for i in range(num_variations):
        selected_overlays = [random.choice(images).resize((250, 350), Image.Resampling.LANCZOS) if images else None for images in overlay_images]
        # Start with a transparent base image
        base_image = Image.new('RGBA', (250, 350), (255, 255, 255, 0))
        result_image = apply_overlays(base_image, selected_overlays)
        output_path = os.path.join(output_dir, f'variation_{i+1}.png')
        result_image.convert('RGB').save(output_path)

    messagebox.showinfo("Completed", f"Generated {num_variations} variations.")

class VariationsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Character Customizer")

        self.overlay_directories = [None] * 6  # [background, hairstyle, eyes/sunglasses, beard/moustache, head type, clothes]
        self.output_dir = ""

        overlay_labels = ["Background Directory", "Hairstyle Directory", "Eyes/Sunglasses Directory", "Beard/Moustache Directory", "Head Type Directory", "Clothes Directory"]
        self.overlay_buttons = []
        for i, label in enumerate(overlay_labels):
            button = tk.Button(self, text=f"Select {label}", command=lambda i=i: self.select_overlay_directory(i))
            button.pack(pady=5)
            self.overlay_buttons.append(button)

        self.output_button = tk.Button(self, text="Select Output Directory", command=self.select_output_directory)
        self.output_button.pack(pady=10)

        self.variations_label = tk.Label(self, text="Number of Variations")
        self.variations_label.pack(pady=5)
        self.variations_entry = tk.Entry(self)
        self.variations_entry.pack(pady=5)

        self.generate_button = tk.Button(self, text="Generate Variations", command=self.generate_variations)
        self.generate_button.pack(pady=20)

    def select_overlay_directory(self, index):
        directory = filedialog.askdirectory(
            title=f"Select {['Background', 'Hairstyle', 'Eyes/Sunglasses', 'Beard/Moustache', 'Head Type', 'Clothes'][index]} Directory"
        )
        if directory:
            self.overlay_directories[index] = directory

    def select_output_directory(self):
        self.output_dir = filedialog.askdirectory(title="Select Output Directory")

    def generate_variations(self):
        try:
            num_variations = int(self.variations_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for variations.")
            return

        if all(self.overlay_directories) and self.output_dir and num_variations > 0:
            create_variations(self.overlay_directories, self.output_dir, num_variations)
        else:
            messagebox.showerror("Error", "Please select input directories, output directory, and specify the number of variations.")

if __name__ == "__main__":
    app = VariationsApp()
    app.mainloop()
