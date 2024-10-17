import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from fpdf import FPDF
import os
from pydub import AudioSegment
import PyPDF2
from docx import Document

class FileConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("File Converter")
        master.geometry("500x400")

        self.dark_mode = True

        self.label = tk.Label(master, text="Choose a file to convert:", bg="black", fg="white")
        self.label.pack(pady=20)

        self.file_label = tk.Label(master, text="No file selected", bg="black", fg='red')
        self.file_label.pack(pady=10)

        self.choose_button = tk.Button(master, text="Choose File", command=self.choose_file, bg="grey", fg="white")
        self.choose_button.pack(pady=10)

        self.convert_button = tk.Button(master, text="Convert", command=self.convert_file, bg="grey", fg="white")
        self.convert_button.pack(pady=10)
        self.convert_button.config(state=tk.DISABLED)

        self.theme_button = tk.Button(master, text="Toggle Theme", command=self.toggle_theme, bg="grey", fg="white")
        self.theme_button.pack(pady=10)

        self.selected_file = None
        self.configure_theme()

    def configure_theme(self):
        if self.dark_mode:
            self.bg_color = "#2E2E2E"
            self.fg_color = "white"
            self.button_bg = "#4A4A4A"
            button_fg = "white"
        else:
            self.bg_color = "#FFFFFF"
            self.fg_color = "black"
            self.button_bg = "#DDDDDD"
            button_fg = "black"

        self.master.config(bg=self.bg_color)
        self.label.config(bg=self.bg_color, fg=self.fg_color)
        self.file_label.config(bg=self.bg_color, fg='red')
        self.choose_button.config(bg=self.button_bg, fg=button_fg)
        self.convert_button.config(bg=self.button_bg, fg=button_fg)
        self.theme_button.config(bg=self.button_bg, fg=button_fg)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.configure_theme()

    def choose_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if self.selected_file:
            self.file_label.config(text=os.path.basename(self.selected_file), fg='green')
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.file_label.config(text="No file selected", fg='red')

    def convert_file(self):
        file_extension = os.path.splitext(self.selected_file)[1].lower()

        if file_extension == '.txt':
            self.choose_text_conversion()
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']:
            self.choose_image_conversion()
        elif file_extension in ['.mp3', '.wav']:
            self.choose_audio_conversion()
        elif file_extension in ['.pdf']:
            self.choose_pdf_conversion()
        else:
            messagebox.showerror("Error", "Unsupported file format or conversion not available.")

    def choose_text_conversion(self):
        conversion_window = tk.Toplevel(self.master)
        conversion_window.title("Select Conversion")
        conversion_window.geometry("300x200")
        conversion_window.config(bg=self.bg_color)

        tk.Label(conversion_window, text="Convert TXT to:", bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        tk.Button(conversion_window, text="PDF", command=lambda: [self.convert_text_to_pdf(), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)
        tk.Button(conversion_window, text="CSV", command=lambda: [self.convert_text_to_csv(), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)
        tk.Button(conversion_window, text="DOCX", command=lambda: [self.convert_text_to_docx(), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)

    def choose_image_conversion(self):
        conversion_window = tk.Toplevel(self.master)
        conversion_window.title("Select Conversion")
        conversion_window.geometry("300x200")
        conversion_window.config(bg=self.bg_color)

        tk.Label(conversion_window, text="Convert Image to:", bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        tk.Button(conversion_window, text="PNG", command=lambda: [self.convert_image("png"), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)
        tk.Button(conversion_window, text="JPG", command=lambda: [self.convert_image("jpg"), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)
        tk.Button(conversion_window, text="BMP", command=lambda: [self.convert_image("bmp"), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)
        tk.Button(conversion_window, text="GIF", command=lambda: [self.convert_image("gif"), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)

    def choose_audio_conversion(self):
        conversion_window = tk.Toplevel(self.master)
        conversion_window.title("Select Conversion")
        conversion_window.geometry("300x200")
        conversion_window.config(bg=self.bg_color)

        tk.Label(conversion_window, text="Convert Audio to:", bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        tk.Button(conversion_window, text="MP3", command=lambda: [self.convert_audio("mp3"), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)
        tk.Button(conversion_window, text="WAV", command=lambda: [self.convert_audio("wav"), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)

    def choose_pdf_conversion(self):
        conversion_window = tk.Toplevel(self.master)
        conversion_window.title("Select Conversion")
        conversion_window.geometry("300x200")
        conversion_window.config(bg=self.bg_color)

        tk.Label(conversion_window, text="Convert PDF to:", bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        tk.Button(conversion_window, text="TXT", command=lambda: [self.convert_pdf_to_txt(), conversion_window.destroy()], bg=self.button_bg, fg="white").pack(pady=5)

    def convert_text_to_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        try:
            with open(self.selected_file, 'r') as file:
                for line in file:
                    pdf.multi_cell(0, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'))

            output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF file", "*.pdf")])
            if output_file:
                pdf.output(output_file)
                messagebox.showinfo("Success", f"File converted to PDF: {output_file}")
            else:
                messagebox.showinfo("Cancelled", "No file saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert file: {e}")

    def convert_text_to_csv(self):
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
        if output_file:
            try:
                with open(self.selected_file, 'r') as infile, open(output_file, 'w') as outfile:
                    for line in infile:
                        outfile.write(line)
                messagebox.showinfo("Success", f"File converted to CSV: {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert file: {e}")
        else:
            messagebox.showinfo("Cancelled", "No file saved.")

    def convert_text_to_docx(self):
        doc = Document()
        try:
            with open(self.selected_file, 'r') as file:
                for line in file:
                    doc.add_paragraph(line)

            output_file = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
            if output_file:
                doc.save(output_file)
                messagebox.showinfo("Success", f"File converted to DOCX: {output_file}")
            else:
                messagebox.showinfo("Cancelled", "No file saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert file: {e}")

    def convert_image(self, format):
        try:
            img = Image.open(self.selected_file)
            output_file = filedialog.asksaveasfilename(defaultextension=f".{format}", filetypes=[("Image files", f"*.{format}")])
            if output_file:
                img.save(output_file, format=format.upper())
                messagebox.showinfo("Success", f"File converted to {format.upper()}: {output_file}")
            else:
                messagebox.showinfo("Cancelled", "No file saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image: {e}")

    def convert_audio(self, format):
        try:
            audio = AudioSegment.from_file(self.selected_file)
            output_file = filedialog.asksaveasfilename(defaultextension=f".{format}", filetypes=[("Audio files", f"*.{format}")])
            if output_file:
                audio.export(output_file, format=format)
                messagebox.showinfo("Success", f"File converted to {format.upper()}: {output_file}")
            else:
                messagebox.showinfo("Cancelled", "No file saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert audio: {e}")

    def convert_pdf_to_txt(self):
        try:
            with open(self.selected_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
                if output_file:
                    with open(output_file, 'w', encoding='utf-8') as txt_file:
                        for page in pdf_reader.pages:
                            txt_file.write(page.extract_text())
                    messagebox.showinfo("Success", f"File converted to TXT: {output_file}")
                else:
                    messagebox.showinfo("Cancelled", "No file saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert PDF: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
