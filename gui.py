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
import fitz  # PyMuPDF

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
        self.master.title("The Binder")
        self.master.geometry("1000x800")
        
        self.style = BubblyStyle()
        
        icon_path = os.path.join('assets', 'app_icon.png')
        if os.path.exists(icon_path):
            try:
                self.pdf_icon = ImageTk.PhotoImage(Image.open(icon_path).resize((50, 50)))
                icon_label = ttk.Label(self.master, image=self.pdf_icon)
                icon_label.pack(pady=10)
            except Exception as e:
                print(f'Error loading icon: {str(e)}')
        else:
            print(f'Icon file not found: {icon_path}')
        
        self.selected_files = []
        self.output_folder = None
        self.reports = []
        self.load_reports_from_file()
        self.init_ui()

    def init_ui(self):
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        file_frame = ttk.Frame(left_frame, padding=10)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        ttk.Label(file_frame, text="Selected PDFs:", font=("Comic Sans MS", 14, "bold")).pack(anchor=tk.W)

        self.file_listbox = tk.Listbox(file_frame, width=50, height=10, bg="#FFE5EC", fg=self.style.fg_color, font=("Comic Sans MS", 12))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.config(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.create_bubbly_button(button_frame, "📁 Add PDF", self.add_pdf).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "🗑️ Remove PDF", self.remove_pdf).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "⬆️ Move Up", self.move_pdf_up).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "⬇️ Move Down", self.move_pdf_down).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "📂 Select Output Folder", self.select_output_folder).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "💾 Save Report", self.save_report).pack(side=tk.LEFT, padx=5)
        self.create_bubbly_button(button_frame, "📤 Load Report", self.load_report).pack(side=tk.LEFT, padx=5)

        cover_frame = ttk.Frame(left_frame, padding=10)
        cover_frame.pack(fill=tk.X, pady=10)

        self.use_cover_pages_var = tk.BooleanVar()
        ttk.Checkbutton(cover_frame, text="Use cover pages", variable=self.use_cover_pages_var, command=self.update_cover_source_label).pack(side=tk.LEFT)

        ttk.Label(cover_frame, text="Cover pages:").pack(side=tk.LEFT, padx=(10, 0))
        self.cover_pages_entry = ttk.Entry(cover_frame, width=20, font=("Comic Sans MS", 12))
        self.cover_pages_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(cover_frame, text="(e.g., 1,2,3-5)").pack(side=tk.LEFT)

        self.cover_source_label = ttk.Label(cover_frame, text="Cover Source: None (0 pages)")
        self.cover_source_label.pack(side=tk.BOTTOM, pady=5)

        # New page selection frame
        page_selection_frame = ttk.Frame(left_frame, padding=10)
        page_selection_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        ttk.Label(page_selection_frame, text="Available PDFs:", font=("Comic Sans MS", 14, "bold")).pack(anchor=tk.W)

        self.pdf_info_text = tk.Text(page_selection_frame, width=50, height=5, bg="#FFE5EC", fg=self.style.fg_color, font=("Comic Sans MS", 12))
        self.pdf_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pdf_info_scrollbar = ttk.Scrollbar(page_selection_frame, orient=tk.VERTICAL, command=self.pdf_info_text.yview)
        pdf_info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pdf_info_text.config(yscrollcommand=pdf_info_scrollbar.set)

        ttk.Label(page_selection_frame, text="Enter page numbers or ranges (e.g., 1,3,5-7,10-12):", font=("Comic Sans MS", 12)).pack(anchor=tk.W, pady=(10, 0))
        self.page_selection_entry = ttk.Entry(page_selection_frame, width=50, font=("Comic Sans MS", 12))
        self.page_selection_entry.pack(fill=tk.X, pady=5)

        self.create_bubbly_button(left_frame, "🚀 Compile PDFs", self.compile_pdfs).pack(pady=10)

        self.output_folder_label = ttk.Label(left_frame, text="Output Folder: none", wraplength=600)
        self.output_folder_label.pack(pady=5)

        report_frame = ttk.Frame(left_frame, padding=10)
        report_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        ttk.Label(report_frame, text="Saved Reports:", font=("Comic Sans MS", 14, "bold")).pack(anchor=tk.W)

        self.report_listbox = tk.Listbox(report_frame, width=50, height=5, bg="#FFE5EC", fg=self.style.fg_color, font=("Comic Sans MS", 12))
        self.report_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        report_scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL)
        report_scrollbar.config(command=self.report_listbox.yview)
        report_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.report_listbox.config(yscrollcommand=report_scrollbar.set)

        # Preview frame
        preview_frame = ttk.Frame(right_frame, padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(preview_frame, text="PDF Preview:", font=("Comic Sans MS", 14, "bold")).pack(anchor=tk.W)

        self.preview_canvas = tk.Canvas(preview_frame, bg="white", width=400, height=600)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)

        preview_controls = ttk.Frame(right_frame, padding=10)
        preview_controls.pack(fill=tk.X)

        self.prev_page_button = self.create_bubbly_button(preview_controls, "◀ Previous", self.show_previous_page)
        self.prev_page_button.pack(side=tk.LEFT, padx=5)

        self.next_page_button = self.create_bubbly_button(preview_controls, "Next ▶", self.show_next_page)
        self.next_page_button.pack(side=tk.RIGHT, padx=5)

        self.page_label = ttk.Label(preview_controls, text="Page: 0 / 0")
        self.page_label.pack(side=tk.LEFT, expand=True)

        self.current_preview_file = None
        self.current_preview_page = 0
        self.current_preview_doc = None

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
                self.selected_files.append((file_path, pdf_info))
                self.file_listbox.insert(tk.END, f"{pdf_info['file_name']} ({pdf_info['num_pages']} pages)")
        self.update_cover_source_label()
        self.update_pdf_info_display()

    def remove_pdf(self):
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            del self.selected_files[index]
            self.file_listbox.delete(index)
            self.update_cover_source_label()
            self.update_pdf_info_display()
            print(f"Removed PDF at index: {index}")
            print(f"Remaining files: {self.selected_files}")

    def move_pdf_up(self):
        selection = self.file_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            self.selected_files[index-1], self.selected_files[index] = self.selected_files[index], self.selected_files[index-1]
            self.update_file_listbox()
            self.file_listbox.selection_set(index-1)
            self.update_pdf_info_display()

    def move_pdf_down(self):
        selection = self.file_listbox.curselection()
        if selection and selection[0] < len(self.selected_files) - 1:
            index = selection[0]
            self.selected_files[index], self.selected_files[index+1] = self.selected_files[index+1], self.selected_files[index]
            self.update_file_listbox()
            self.file_listbox.selection_set(index+1)
            self.update_pdf_info_display()

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.output_folder_label.config(text=f"Output Folder: {self.output_folder}")
        else:
            self.output_folder_label.config(text="Output Folder: none")

    def update_pdf_info_display(self):
        self.pdf_info_text.delete('1.0', tk.END)
        for _, pdf_info in self.selected_files:
            if pdf_info:
                self.pdf_info_text.insert(tk.END, f"{pdf_info['file_name']} ({pdf_info['num_pages']} pages)\n")

    def save_report(self):
        name = generate_space_name()
        page_selections = self.get_page_selections()
        if page_selections:
            use_cover_pages = self.use_cover_pages_var.get()
            cover_pages = parse_page_selection(self.cover_pages_entry.get(), max(info['num_pages'] for _, info in self.selected_files if info)) if use_cover_pages else None
            report = Report(name, [file_path for file_path, _ in self.selected_files], page_selections, use_cover_pages, cover_pages)
            self.reports.append(report)
            self.save_reports_to_file()
            self.update_report_listbox()
            messagebox.showinfo("Report Saved", f"Report '{name}' has been saved.")
            print(f"Debug: Report saved - {name}")
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
                self.selected_files = [(path, PDFCompiler.get_pdf_info(path)) for path in selected_report.file_paths]
                self.update_file_listbox()
                self.use_cover_pages_var.set(selected_report.use_cover_pages)
                self.cover_pages_entry.delete(0, tk.END)
                if selected_report.cover_pages:
                    self.cover_pages_entry.insert(0, ','.join(map(str, selected_report.cover_pages)))
                self.update_cover_source_label()
                self.update_pdf_info_display()
                self.page_selection_entry.delete(0, tk.END)
                self.page_selection_entry.insert(0, ','.join(str(page) for pages in selected_report.page_selections.values() for page in pages))
                print(f"Debug: Report loaded - {selected_name}")
            else:
                messagebox.showerror("Error", "Selected report not found.")

    def save_reports_to_file(self):
        with open('reports.json', 'w') as f:
            json.dump([report.__dict__ for report in self.reports], f)
        print(f"Debug: Reports saved to file - {len(self.reports)} reports")

    def load_reports_from_file(self):
        try:
            with open('reports.json', 'r') as f:
                report_data = json.load(f)
                self.reports = [Report(**data) for data in report_data]
            print(f"Debug: Reports loaded from file - {len(self.reports)} reports")
        except FileNotFoundError:
            self.reports = []
            print("Debug: No reports file found, starting with empty list")

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for _, pdf_info in self.selected_files:
            if pdf_info:
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
            _, file_info = self.selected_files[0]
            if file_info:
                self.cover_source_label.config(text=f"Cover Source: {file_info['file_name']} ({file_info['num_pages']} pages)")
            else:
                self.cover_source_label.config(text="Cover Source: None (0 pages)")
        else:
            self.cover_source_label.config(text="Cover Source: None (0 pages)")

    def get_page_selections(self):
        page_input = self.page_selection_entry.get()
        if not page_input:
            messagebox.showwarning("No Pages Selected", "Please enter page numbers or ranges before compiling.")
            return None

        selected_pages = {}
        for file_path, pdf_info in self.selected_files:
            if pdf_info:
                try:
                    page_list = parse_page_selection(page_input, pdf_info['num_pages'])
                    if page_list:
                        selected_pages[file_path] = page_list
                except ValueError as e:
                    messagebox.showwarning("Invalid Input", f"Error parsing pages for {pdf_info['file_name']}: {str(e)}")
                    return None
            else:
                messagebox.showwarning("Invalid PDF", f"Error: Could not read PDF information for {file_path}")
                return None

        return selected_pages

    def compile_pdfs(self, page_selections=None):
        if not self.selected_files:
            messagebox.showwarning("No PDFs", "Please add PDF files before compiling.")
            return

        if not self.output_folder:
            self.select_output_folder()
            if not self.output_folder:
                return

        if not hasattr(self, 'current_report'):
            save_report = messagebox.askyesno("Save Report", "No report is currently loaded. Would you like to save the current configuration as a report before compiling?")
            if save_report:
                self.save_report()
            else:
                proceed = messagebox.askyesno("Proceed", "Do you want to proceed with compilation without saving a report?")
                if not proceed:
                    return

        if page_selections is None:
            page_selections = self.get_page_selections()
        if not page_selections:
            return

        use_cover_pages = self.use_cover_pages_var.get()
        cover_pages = None
        if use_cover_pages:
            try:
                cover_pages = parse_page_selection(self.cover_pages_entry.get(), max(info['num_pages'] for _, info in self.selected_files if info))
            except ValueError as e:
                messagebox.showwarning("Invalid Input", f"Error parsing cover pages: {str(e)}")
                return

        output_filename = f"{generate_space_name()}.pdf"
        output_file = os.path.join(self.output_folder, output_filename)

        input_files = [file_path for file_path, _ in self.selected_files]
        if PDFCompiler.compile_pdfs(input_files, page_selections, output_file, use_cover_pages, cover_pages):
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

    def on_file_select(self, event):
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            file_path, _ = self.selected_files[index]
            self.load_preview(file_path)

    def load_preview(self, file_path):
        self.current_preview_file = file_path
        self.current_preview_page = 0
        self.current_preview_doc = fitz.open(file_path)
        self.update_preview()

    def update_preview(self):
        if self.current_preview_doc:
            page = self.current_preview_doc[self.current_preview_page]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img = img.resize((400, int(400 * img.height / img.width)))
            photo = ImageTk.PhotoImage(img)
            
            self.preview_canvas.delete("all")
            self.preview_canvas.config(width=img.width, height=img.height)
            self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.preview_canvas.photo = photo  # Keep a reference to avoid garbage collection

            self.page_label.config(text=f"Page: {self.current_preview_page + 1} / {len(self.current_preview_doc)}")

    def show_previous_page(self):
        if self.current_preview_doc and self.current_preview_page > 0:
            self.current_preview_page -= 1
            self.update_preview()

    def show_next_page(self):
        if self.current_preview_doc and self.current_preview_page < len(self.current_preview_doc) - 1:
            self.current_preview_page += 1
            self.update_preview()

def main():
    root = tk.Tk()
    app = PDFCompilerGUI(root)
    
    server_thread = threading.Thread(target=app.start_http_server)
    server_thread.daemon = True
    server_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()
