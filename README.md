# The Binder

Current development is on the 'Bubbles' branch.

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

## Dependencies

The Binder relies on the following Python libraries:

1. tkinter: Used for creating the graphical user interface.
   - Installation: Typically comes pre-installed with Python.

2. PyPDF2: Handles PDF file operations such as merging and page extraction.
   - Installation: `pip install PyPDF2`

3. Pillow (PIL): Used for image processing, particularly for handling the application icon.
   - Installation: `pip install Pillow`

4. json: Used for saving and loading report data.
   - Installation: Part of Python's standard library, no additional installation required.

5. threading: Used for running the HTTP server alongside the GUI.
   - Installation: Part of Python's standard library, no additional installation required.

6. http.server and socketserver: Used for creating a simple HTTP server.
   - Installation: Part of Python's standard library, no additional installation required.

7. Flask: Web framework used for the backend API.
   - Installation: `pip install flask`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/the-binder.git
   cd the-binder
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   pip install flask  # Ensure Flask is installed
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

6. The Binder's Cosmic Collection:
   - View the list of PDFs you've added to your compilation project.
   - This section displays file names and page counts for easy reference.

Note: The table of contents functionality is integrated with the cover page settings and page selection. By carefully selecting cover pages and content pages, you can effectively create a table of contents for your compiled PDF.

## Known Issues

1. The Flask application shows a warning about being a development server, which is expected and not an issue for our current development work.
2. The Electron app is currently failing to start due to a missing shared library (libxshmfence.so.1).
3. Unable to select specific PDFs from "The Binder's Cosmic Collection" list to modify page numbers or ranges.
4. The "Remove PDF" button functionality is inconsistent.
5. Flask module not found: Ensure Flask is installed properly using `pip install flask`.
6. Buttons are missing from the GUI.
7. Files selected and files available sections are absent from the GUI.
8. The interface now follows a cyberpunk and zef-inspired aesthetic with neon colors and glitch effects.
9. Animated background with floating particles has been implemented.
10. Buttons and UI elements have been redesigned with angular, polygon-based shapes.
11. Eyeball mascots have been updated to look more robotic or cybernetic.
12. A subtle screen flicker effect has been added to enhance the cyberpunk feel.
13. Performance issues may occur with the new animations on lower-end devices.
14. Compatibility issues across different browsers or devices may exist due to the advanced CSS and JavaScript effects.
15. Some features are still not fully implemented, such as actual PDF compilation and file handling.

## Current Status

We have successfully implemented the initial prototype with a cyberpunk-inspired GUI using Electron.js. The interface now features neon colors, glitch effects, and animated elements that align with the desired cyberpunk and zef culture aesthetic. The current focus is on optimizing performance for smoother animations, especially on lower-end devices, and adding more interactive elements to enhance user experience.

The next steps include:
1. Optimizing the performance of animations and effects.
2. Implementing the core PDF compilation functionality.
3. Enhancing the interactivity of UI elements.
4. Ensuring cross-platform compatibility.
5. Integrating the backend Python functionality with the new Electron.js frontend.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
