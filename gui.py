import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinter.font import Font
from pdf_compiler import PDFCompiler
from name_generator import generate_space_name
import json
from PIL import Image, ImageTk
import threading
import http.server
import socketserver

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

class BubblyStyle(ttk.Style):
    def __init__(self):
        super().__init__()
        self.theme_use('clam')
        
        self.bg_color = "#FF69B4"
        self.fg_color = "#00FF00"
        self.accent_color = "#FFD700"
        
        self.configure("TFrame", background=self.bg_color)
        self.configure("TButton", 
                       background=self.fg_color, 
                       foreground="white", 
                       font=("Comic Sans MS", 12, "bold"), 
                       borderwidth=0, 
                       padding=10)
        self.map("TButton", 
                 background=[("active", self.accent_color)],
                 relief=[("pressed", "sunken")])
        
        self.layout("TButton", [
            ("Button.padding", {"children": [
                ("Button.label", {"side": "left", "expand": 1})
            ], "sticky": "nswe"})
        ])
        
        self.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Comic Sans MS", 12))
        self.configure("TCheckbutton", background=self.bg_color, foreground=self.fg_color, font=("Comic Sans MS", 12))
        self.configure("Listbox", background="#FFE5EC", foreground=self.fg_color, font=("Comic Sans MS", 12), borderwidth=0)

class PDFCompilerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Super Fun PDF Compiler!")
        self.master.geometry("700x800")
        
        self.style = BubblyStyle()
        
        icon_path = os.path.join('assets', 'app_icon.png')
        if os.path.exists(icon_path):
            try:
                self.pdf_icon = ImageTk.PhotoImage(Image.open(icon_path).resize((50, 50)))
                icon_label = ttk.Label(self.master, image=self.pdf_icon, background=self.style.bg_color)
                icon_label.pack(pady=10)
            except Exception as e:
                print(f'Error loading icon: {str(e)}')
        else:
            print(f'Icon file not found: {icon_path}')
        
        self.selected_files = {}
        self.output_folder = None
        self.reports = []
        self.load_reports_from_file()
        self.init_ui()

    def init_ui(self):
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        file_frame = ttk.Frame(main_frame, padding=10)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        ttk.Label(file_frame, text="Selected PDFs:", font=("Comic Sans MS", 14, "bold")).pack(anchor=tk.W)

        self.file_listbox = tk.Listbox(file_frame, width=50, height=10, bg="#FFE5EC", fg=self.style.fg_color, font=("Comic Sans MS", 12))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.config(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.create_bubbly_button(button_frame, "📁 Add PDF", self.add_pdf).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "🗑️ Remove PDF", self.remove_pdf).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "📂 Select Output Folder", self.select_output_folder).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "💾 Save Report", self.save_report).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "📤 Load Report", self.load_report).pack(side=tk.LEFT, padx=5)

        cover_frame = ttk.Frame(main_frame, padding=10)
        cover_frame.pack(fill=tk.X, pady=10)

        self.use_cover_pages_var = tk.BooleanVar()
        ttk.Checkbutton(cover_frame, text="Use cover pages", variable=self.use_cover_pages_var, command=self.update_cover_source_label).pack(side=tk.LEFT)

        ttk.Label(cover_frame, text="Cover pages:").pack(side=tk.LEFT, padx=(10, 0))
        self.cover_pages_entry = ttk.Entry(cover_frame, width=20, font=("Comic Sans MS", 12))
        self.cover_pages_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(cover_frame, text="(e.g., 1,2,3-5)").pack(side=tk.LEFT)

        self.cover_source_label = ttk.Label(cover_frame, text="Cover Source: None (0 pages)")
        self.cover_source_label.pack(side=tk.BOTTOM, pady=5)

        self.create_bubbly_button(main_frame, "🚀 Compile PDFs", self.compile_pdfs).pack(pady=10)

        self.output_folder_label = ttk.Label(main_frame, text="Output Folder: none", wraplength=600)
        self.output_folder_label.pack(pady=5)

        report_frame = ttk.Frame(main_frame, padding=10)
        report_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        ttk.Label(report_frame, text="Saved Reports:", font=("Comic Sans MS", 14, "bold")).pack(anchor=tk.W)

        self.report_listbox = tk.Listbox(report_frame, width=50, height=5, bg="#FFE5EC", fg=self.style.fg_color, font=("Comic Sans MS", 12))
        self.report_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        report_scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL)
        report_scrollbar.config(command=self.report_listbox.yview)
        report_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.report_listbox.config(yscrollcommand=report_scrollbar.set)

        self.update_report_listbox()

    def create_bubbly_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command, style="TButton")
        button.bind("<Enter>", lambda e: e.widget.configure(cursor="hand2"))
        button.bind("<Leave>", lambda e: e.widget.configure(cursor=""))
        return button

    def add_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        
        for file_path in files:
            pdf_info = PDFCompiler.get_pdf_info(file_path)
            if pdf_info:
                self.selected_files[file_path] = pdf_info
                self.file_listbox.insert(tk.END, f"{pdf_info['file_name']} ({pdf_info['num_pages']} pages)")
        self.update_cover_source_label()

    def remove_pdf(self):
        selection = self.file_listbox.curselection()
        if selection:
            file_path = list(self.selected_files.keys())[selection[0]]
            del self.selected_files[file_path]
            self.file_listbox.delete(selection[0])
        self.update_cover_source_label()

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
                self.update_cover_source_label()
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

    def update_cover_source_label(self):
        if self.use_cover_pages_var.get() and self.selected_files:
            first_file = list(self.selected_files.keys())[0]
            file_info = self.selected_files[first_file]
            self.cover_source_label.config(text=f"Cover Source: {file_info['file_name']} ({file_info['num_pages']} pages)")
        else:
            self.cover_source_label.config(text="Cover Source: None (0 pages)")

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

    def start_http_server(self):
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"PDF Compiler is running!")

        port = 8080
        handler = Handler
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"Serving at port {port}")
            httpd.serve_forever()

def main():
    root = tk.Tk()
    app = PDFCompilerGUI(root)
    
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=app.start_http_server)
    server_thread.daemon = True
    server_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()