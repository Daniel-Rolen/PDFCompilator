# The Binder

A Python-based desktop application for PDF compilation with local file handling and a fun, user-friendly interface.

## 🎨 Branding

The Binder is represented by our lovable eyeball logo, symbolizing the watchful gaze that keeps your PDFs organized and bound together. Our mascot, Bindy the Eyeball, is always here to guide you through your PDF compilation journey!

## Features

- **PDF Compilation**: Combine multiple PDF files into a single document.
- **Page Selection**: Choose specific pages from each PDF to include in the final compilation.
- **Cover Page Settings**: Add custom cover pages to your compiled PDF.
- **Table of Contents Integration**: 
  - While not explicitly implemented as a separate feature, the cover page settings and page selection functionality work together to create a pseudo table of contents.
  - Users can select specific pages from the first PDF to serve as cover pages or a table of contents.
  - These pages are then followed by the selected content pages from all PDFs.
- **Fun Naming**: Automatically generate unique, space-themed names for output files.
- **Report Saving and Loading**: Save your compilation settings as reports and load them later.
- **User-Friendly GUI**: Colorful and intuitive interface for easy navigation and use.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/the-binder.git
   cd the-binder
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Using the GUI:
   - Click "Add PDF" to select PDF files for compilation.
   - Use "Remove PDF" to remove any unwanted files from the list.
   - Select an output folder using "Select Output Folder".

3. Cover Page Settings:
   - Check the "Use cover pages" box to enable cover page functionality.
   - Enter the page numbers you want to use as cover pages in the "Cover pages" field (e.g., 1,2,3-5).
   - The cover pages will be taken from the first PDF in your list.

4. Compiling PDFs:
   - Click "Compile PDFs" to start the compilation process.
   - You'll be prompted to enter the pages you want to include from each PDF.
   - The Binder will generate a fun, space-themed name for your output file.

5. Saving and Loading Reports:
   - Use "Save Report" to save your current compilation settings.
   - Use "Load Report" to recall previously saved settings.

Note: The table of contents functionality is integrated with the cover page settings and page selection. By carefully selecting cover pages and content pages, you can effectively create a table of contents for your compiled PDF.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
