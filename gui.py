import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from pdf_compiler import PDFCompiler
from name_generator import generate_space_name
import json

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

class Report:
    def __init__(self, name, file_paths, page_selections, use_cover_pages=False, cover_pages=None):
        self.name = name
        self.file_paths = file_paths
        self.page_selections = page_selections
        self.use_cover_pages = use_cover_pages
        self.cover_pages = cover_pages

class PDFCompilerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Compiler")
        self.master.geometry("600x700")  # Increased height to accommodate new sections

        self.selected_files = {}
        self.output_folder = None
        self.reports = []
        self.load_reports_from_file()
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

        select_output_button = tk.Button(button_frame, text="Select Output Folder", command=self.select_output_folder)
        select_output_button.pack(side=tk.LEFT, padx=5)

        save_report_button = tk.Button(button_frame, text="Save Report", command=self.save_report)
        save_report_button.pack(side=tk.LEFT, padx=5)

        load_report_button = tk.Button(button_frame, text="Load Report", command=self.load_report)
        load_report_button.pack(side=tk.LEFT, padx=5)

        # Cover pages section
        cover_frame = tk.Frame(self.master)
        cover_frame.pack(fill=tk.X, padx=10, pady=5)

        self.use_cover_pages_var = tk.BooleanVar()
        self.use_cover_pages_check = tk.Checkbutton(cover_frame, text="Use cover pages", variable=self.use_cover_pages_var)
        self.use_cover_pages_check.pack(side=tk.LEFT)

        tk.Label(cover_frame, text="Cover pages:").pack(side=tk.LEFT, padx=(10, 0))
        self.cover_pages_entry = tk.Entry(cover_frame, width=20)
        self.cover_pages_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(cover_frame, text="(e.g., 1,2,3-5)").pack(side=tk.LEFT)

        compile_button = tk.Button(self.master, text="Compile PDFs", command=self.compile_pdfs)
        compile_button.pack(pady=10)

        # Output folder display
        self.output_folder_label = tk.Label(self.master, text="Output Folder: none")
        self.output_folder_label.pack(pady=5)

        # Saved reports section
        report_frame = tk.Frame(self.master)
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(report_frame, text="Saved Reports:").pack(anchor=tk.W)

        self.report_listbox = tk.Listbox(report_frame, width=50)
        self.report_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        report_scrollbar = tk.Scrollbar(report_frame, orient=tk.VERTICAL)
        report_scrollbar.config(command=self.report_listbox.yview)
        report_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.report_listbox.config(yscrollcommand=report_scrollbar.set)

        self.update_report_listbox()

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

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.output_folder_label.config(text=f"Output Folder: {self.output_folder}")
        else:
            self.output_folder_label.config(text="Output Folder: none")

    def get_page_selections(self):
        pdf_info = "\n".join([f"{info['file_name']} ({info['num_pages']} pages)" for info in self.selected_files.values()])
        page_input = simpledialog.askstring("Select Pages", 
            f"Enter page numbers or ranges for all PDFs (comma-separated):\n"
            f"Example: 1,3,5-7,10-12\n\n"
            f"Available PDFs:\n{pdf_info}")
        
        if not page_input:
            return None

        selected_pages = {}
        for file_path, pdf_info in self.selected_files.items():
            try:
                page_list = parse_page_selection(page_input, pdf_info['num_pages'])
                if page_list:
                    selected_pages[file_path] = page_list
            except ValueError as e:
                messagebox.showwarning("Invalid Input", f"Error parsing pages for {pdf_info['file_name']}: {str(e)}")
                return None

        return selected_pages

    def save_report(self):
        name = simpledialog.askstring("Save Report", "Enter a name for this report:")
        if name:
            page_selections = self.get_page_selections()
            if page_selections:
                use_cover_pages = self.use_cover_pages_var.get()
                cover_pages = parse_page_selection(self.cover_pages_entry.get(), max(info['num_pages'] for info in self.selected_files.values())) if use_cover_pages else None
                report = Report(name, list(self.selected_files.keys()), page_selections, use_cover_pages, cover_pages)
                self.reports.append(report)
                self.save_reports_to_file()
                self.update_report_listbox()
                messagebox.showinfo("Report Saved", f"Report '{name}' has been saved.")
            else:
                messagebox.showwarning("Invalid Input", "Please select valid pages before saving the report.")

    def load_report(self):
        if not self.reports:
            messagebox.showinfo("No Reports", "No saved reports found.")
            return

        report_names = [report.name for report in self.reports]
        selected_name = simpledialog.askstring("Load Report", "Select a report to load:", initialvalue=report_names[0])
        
        if selected_name:
            selected_report = next((report for report in self.reports if report.name == selected_name), None)
            if selected_report:
                self.selected_files = {path: PDFCompiler.get_pdf_info(path) for path in selected_report.file_paths}
                self.update_file_listbox()
                self.use_cover_pages_var.set(selected_report.use_cover_pages)
                self.cover_pages_entry.delete(0, tk.END)
                if selected_report.cover_pages:
                    self.cover_pages_entry.insert(0, ','.join(map(str, selected_report.cover_pages)))
                self.compile_pdfs(selected_report.page_selections)
            else:
                messagebox.showerror("Error", "Selected report not found.")

    def save_reports_to_file(self):
        with open('reports.json', 'w') as f:
            json.dump([report.__dict__ for report in self.reports], f)

    def load_reports_from_file(self):
        try:
            with open('reports.json', 'r') as f:
                report_data = json.load(f)
                self.reports = [Report(**data) for data in report_data]
        except FileNotFoundError:
            self.reports = []

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for pdf_info in self.selected_files.values():
            self.file_listbox.insert(tk.END, f"{pdf_info['file_name']} ({pdf_info['num_pages']} pages)")

    def update_report_listbox(self):
        self.report_listbox.delete(0, tk.END)
        if self.reports:
            for report in self.reports:
                self.report_listbox.insert(tk.END, report.name)
        else:
            self.report_listbox.insert(tk.END, "none")

    def compile_pdfs(self, page_selections=None):
        if not self.selected_files:
            messagebox.showwarning("No PDFs", "Please add PDF files before compiling.")
            return

        if not self.output_folder:
            self.select_output_folder()
            if not self.output_folder:
                return

        if page_selections is None:
            page_selections = self.get_page_selections()
        if not page_selections:
            return

        use_cover_pages = self.use_cover_pages_var.get()
        cover_pages = None
        if use_cover_pages:
            try:
                cover_pages = parse_page_selection(self.cover_pages_entry.get(), max(info['num_pages'] for info in self.selected_files.values()))
            except ValueError as e:
                messagebox.showwarning("Invalid Input", f"Error parsing cover pages: {str(e)}")
                return

        output_filename = f"{generate_space_name()}.pdf"
        output_file = os.path.join(self.output_folder, output_filename)

        if PDFCompiler.compile_pdfs(list(self.selected_files.keys()), page_selections, output_file, use_cover_pages, cover_pages):
            messagebox.showinfo("Success", f"PDFs compiled successfully.\nOutput file: {output_file}")
        else:
            messagebox.showerror("Error", "Failed to compile PDFs. Please try again.")

def main():
    root = tk.Tk()
    PDFCompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
