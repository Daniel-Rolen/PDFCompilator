import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QFileDialog, QListWidget, QLabel, QMessageBox, QInputDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pdf_compiler import PDFCompiler

class PDFCompilerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Compiler")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("assets/app_icon.svg"))

        self.selected_files = {}
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # File selection
        file_layout = QHBoxLayout()
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list)

        button_layout = QVBoxLayout()
        add_button = QPushButton("Add PDF")
        add_button.clicked.connect(self.add_pdf)
        remove_button = QPushButton("Remove PDF")
        remove_button.clicked.connect(self.remove_pdf)
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addStretch()

        file_layout.addLayout(button_layout)
        layout.addLayout(file_layout)

        # Compilation
        compile_button = QPushButton("Compile PDFs")
        compile_button.clicked.connect(self.compile_pdfs)
        layout.addWidget(compile_button)

    def add_pdf(self):
        file_dialog = QFileDialog()
        files, _ = file_dialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")
        
        for file_path in files:
            pdf_info = PDFCompiler.get_pdf_info(file_path)
            if pdf_info:
                self.selected_files[file_path] = pdf_info
                self.file_list.addItem(f"{pdf_info['file_name']} ({pdf_info['num_pages']} pages)")

    def remove_pdf(self):
        current_item = self.file_list.currentItem()
        if current_item:
            file_path = list(self.selected_files.keys())[self.file_list.row(current_item)]
            del self.selected_files[file_path]
            self.file_list.takeItem(self.file_list.row(current_item))

    def compile_pdfs(self):
        if not self.selected_files:
            QMessageBox.warning(self, "No PDFs", "Please add PDF files before compiling.")
            return

        selected_pages = {}
        for file_path, pdf_info in self.selected_files.items():
            pages, ok = QInputDialog.getText(self, f"Select pages for {pdf_info['file_name']}",
                                             f"Enter page numbers (1-{pdf_info['num_pages']}, comma-separated):")
            if ok:
                try:
                    page_list = [int(p.strip()) for p in pages.split(',') if 1 <= int(p.strip()) <= pdf_info['num_pages']]
                    if page_list:
                        selected_pages[file_path] = page_list
                except ValueError:
                    QMessageBox.warning(self, "Invalid Input", "Please enter valid page numbers.")
                    return

        if not selected_pages:
            QMessageBox.warning(self, "No Pages Selected", "Please select pages from at least one PDF.")
            return

        output_file, _ = QFileDialog.getSaveFileName(self, "Save Compiled PDF", "", "PDF Files (*.pdf)")
        if output_file:
            if PDFCompiler.compile_pdfs(self.selected_files.keys(), selected_pages, output_file):
                QMessageBox.information(self, "Success", "PDFs compiled successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to compile PDFs. Please try again.")

