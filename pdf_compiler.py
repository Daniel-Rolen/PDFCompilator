import os
from PyPDF2 import PdfReader, PdfWriter

class PDFCompiler:
    @staticmethod
    def compile_pdfs(input_files, selected_pages, output_file):
        """
        Compile selected pages from multiple PDFs into a single PDF.

        :param input_files: List of input PDF file paths
        :param selected_pages: Dictionary with file paths as keys and lists of selected page numbers as values
        :param output_file: Output PDF file path
        :return: True if compilation is successful, False otherwise
        """
        try:
            pdf_writer = PdfWriter()

            for file_path, pages in selected_pages.items():
                pdf_reader = PdfReader(file_path)
                for page_num in pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])

            with open(output_file, 'wb') as output:
                pdf_writer.write(output)

            return True
        except Exception as e:
            print(f"Error compiling PDFs: {str(e)}")
            return False

    @staticmethod
    def get_pdf_info(file_path):
        """
        Get information about a PDF file.

        :param file_path: Path to the PDF file
        :return: Dictionary containing file name and number of pages
        """
        try:
            pdf_reader = PdfReader(file_path)
            return {
                'file_name': os.path.basename(file_path),
                'num_pages': len(pdf_reader.pages)
            }
        except Exception as e:
            print(f"Error reading PDF info: {str(e)}")
            return None
