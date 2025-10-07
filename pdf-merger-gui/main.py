import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from pypdf import PdfWriter
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger 📁")
        self.root.geometry("500x400") # Set a default size

        # This list will store the full paths of the selected PDF files
        self.selected_files = []

        # --- GUI Widgets ---

        # 1. Main Frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 2. Select Files Button
        select_btn = tk.Button(
            main_frame,
            text="1. Select PDF Files",
            command=self.select_files,
            font=("Helvetica", 12),
            bg="#2a9d8f",
            fg="white"
        )
        select_btn.pack(fill=tk.X, pady=5)

        # 3. Listbox to display selected files (with a scrollbar)
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.file_listbox = Listbox(
            list_frame,
            selectmode=tk.MULTIPLE, # Allows selecting multiple items
            font=("Helvetica", 10)
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # 4. Merge Files Button
        merge_btn = tk.Button(
            main_frame,
            text="2. Merge and Save PDF",
            command=self.merge_pdfs,
            font=("Helvetica", 12, "bold"),
            bg="#e76f51",
            fg="white"
        )
        merge_btn.pack(fill=tk.X, pady=10)
        
        # 5. Status Label
        self.status_label = tk.Label(main_frame, text="Ready to merge PDFs!", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)


    def select_files(self):
        """Opens a file dialog to select multiple PDF files."""
        # Open file dialog to select .pdf files
        filenames = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )

        if filenames:
            self.selected_files = list(filenames)
            # Clear the listbox before adding new files
            self.file_listbox.delete(0, tk.END)
            # Add just the file names (not full path) to the listbox
            for f in self.selected_files:
                self.file_listbox.insert(tk.END, os.path.basename(f))
            self.status_label.config(text=f"{len(self.selected_files)} file(s) selected.")


    def merge_pdfs(self):
        """Merges the selected PDFs and saves the output."""
        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please select at least one PDF file to merge.")
            return

        # Ask the user for a location to save the merged file
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            title="Save Merged PDF As...",
            filetypes=(("PDF files", "*.pdf"),)
        )

        # If the user cancels the save dialog, do nothing
        if not output_path:
            self.status_label.config(text="Save operation cancelled.")
            return

        try:
            merger = PdfWriter()
            for pdf_path in self.selected_files:
                merger.append(pdf_path)
            
            merger.write(output_path)
            merger.close()

            messagebox.showinfo("Success!", f"PDFs successfully merged into:\n{output_path}")
            self.status_label.config(text="Merge complete! ✨")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during merging:\n{e}")
            self.status_label.config(text="An error occurred.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()