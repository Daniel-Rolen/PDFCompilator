import tkinter as tk
from gui import PDFCompilerGUI
import os

if __name__ == "__main__":
    # Start the GUI
    root = tk.Tk()
    app = PDFCompilerGUI(root)
    
    # Add debug logging for PDF preview functionality
    print("Debug: PDF preview functionality initialized")
    app.file_listbox.bind('<<ListboxSelect>>', lambda event: print(f"Debug: File selected for preview: {app.current_preview_file}"))
    app.prev_page_button.config(command=lambda: print("Debug: Previous page button clicked") or app.show_previous_page())
    app.next_page_button.config(command=lambda: print("Debug: Next page button clicked") or app.show_next_page())
    
    # Add more detailed debug messages
    app.load_preview = lambda file_path: (print(f"Debug: Loading preview for file: {file_path}"), PDFCompilerGUI.load_preview(app, file_path))
    app.update_preview = lambda: (print(f"Debug: Updating preview for page {app.current_preview_page + 1}"), PDFCompilerGUI.update_preview(app))
    
    # Load the test PDF file
    test_pdf_path = os.path.join(os.getcwd(), "test.pdf")
    if os.path.exists(test_pdf_path):
        print(f"Debug: Loading test PDF: {test_pdf_path}")
        app.load_preview(test_pdf_path)
    else:
        print(f"Debug: Test PDF not found at {test_pdf_path}")
    
    root.mainloop()
