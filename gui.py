import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pdf_compiler import PDFCompiler

def parse_page_selection(pages_str, max_pages):
    pages = set()
    for part in pages_str.split(','):
        part = part.strip()
        try:
            if '-' in part:
                start, end = map(int, part.split('-'))
                if start > end:
                    raise ValueError(f"Invalid range: {start}-{end}")
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
        except ValueError:
            raise ValueError(f"Invalid input: {part}")
    return sorted([p for p in pages if 1 <= p <= max_pages])

class PDFCompilerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Compiler")
        self.master.geometry("600x400")

        self.selected_files = {}
        self.init_ui()

    def init_ui(self):
        # File selection
        file_frame = tk.Frame(self.master)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.file_listbox = tk.Listbox(file_frame, width=50)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(file_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(self.master)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        add_button = tk.Button(button_frame, text="Add PDF", command=self.add_pdf)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Remove PDF", command=self.remove_pdf)
        remove_button.pack(side=tk.LEFT, padx=5)

        compile_button = tk.Button(self.master, text="Compile PDFs", command=self.compile_pdfs)
        compile_button.pack(pady=10)

    def add_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        
        for file_path in files:
            pdf_info = PDFCompiler.get_pdf_info(file_path)
            if pdf_info:
                self.selected_files[file_path] = pdf_info
                self.file_listbox.insert(tk.END, f"{pdf_info['file_name']} ({pdf_info['num_pages']} pages)")

    def remove_pdf(self):
        selection = self.file_listbox.curselection()
        if selection:
            file_path = list(self.selected_files.keys())[selection[0]]
            del self.selected_files[file_path]
            self.file_listbox.delete(selection[0])

    def compile_pdfs(self):
        if not self.selected_files:
            messagebox.showwarning("No PDFs", "Please add PDF files before compiling.")
            return

        selected_pages = {}
        for file_path, pdf_info in self.selected_files.items():
            pages = simpledialog.askstring(f"Select pages for {pdf_info['file_name']}",
                                           f"Enter page numbers or ranges (1-{pdf_info['num_pages']}, comma-separated):\n"
                                           f"Example: 1,3,5-7,10-12")
            if pages:
                try:
                    page_list = parse_page_selection(pages, pdf_info['num_pages'])
                    if page_list:
                        selected_pages[file_path] = page_list
                    else:
                        messagebox.showwarning("Invalid Input", f"No valid pages selected for {pdf_info['file_name']}.")
                        return
                except ValueError as e:
                    messagebox.showwarning("Invalid Input", f"Error parsing pages for {pdf_info['file_name']}: {str(e)}")
                    return

        if not selected_pages:
            messagebox.showwarning("No Pages Selected", "Please select pages from at least one PDF.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_file:
            if PDFCompiler.compile_pdfs(self.selected_files.keys(), selected_pages, output_file):
                messagebox.showinfo("Success", "PDFs compiled successfully.")
            else:
                messagebox.showerror("Error", "Failed to compile PDFs. Please try again.")

def main():
    root = tk.Tk()
    PDFCompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
