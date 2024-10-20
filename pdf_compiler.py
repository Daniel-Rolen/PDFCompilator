import os
from PyPDF2 import PdfReader, PdfWriter

class PDFCompiler:
    @staticmethod
    def compile_pdfs(input_files, selected_pages, output_file, use_cover_pages=False, cover_pages=None):
        """
        Compile selected pages from multiple PDFs into a single PDF.

        :param input_files: List of input PDF file paths
        :param selected_pages: Dictionary with file paths as keys and lists of selected page numbers as values
        :param output_file: Output PDF file path
        :param use_cover_pages: Boolean to indicate if cover pages should be used
        :param cover_pages: List of cover page numbers to include
        :return: True if compilation is successful, False otherwise
        """
        try:
            pdf_writer = PdfWriter()

            # Handle cover pages if enabled
            if use_cover_pages and cover_pages and input_files:
                first_pdf = PdfReader(input_files[0])
                for page_num in cover_pages:
                    if 0 <= page_num < len(first_pdf.pages):
                        pdf_writer.add_page(first_pdf.pages[page_num])

            # Compile the rest of the pages
            for file_path, pages in selected_pages.items():
                pdf_reader = PdfReader(file_path)
                for page_num in pages:
                    if 0 <= page_num - 1 < len(pdf_reader.pages):
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
