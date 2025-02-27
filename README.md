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

8. PyMuPDF (fitz): Used for PDF processing.
   - Installation: `pip install PyMuPDF`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/the-binder.git
   cd the-binder
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   pip install flask PyMuPDF
   ```

Note: If you encounter issues with tkinter, you may need to install it separately. On macOS, you can use Homebrew:
```
brew install python-tk
```
On Linux, you can use your package manager. For example, on Ubuntu:
```
sudo apt-get install python3-tk
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
5. Some features are still not fully implemented, such as actual PDF compilation and file handling.
6. Need to implement functionality to add a cover page with new page numbers and a cover letter to the final compiled PDF.
7. Space in file names may cause issues with PDF compilation and handling.
8. ModuleNotFoundError: No module named 'frontend' when running main.py. This might be due to a missing or incorrectly installed dependency.
9. ModuleNotFoundError: No module named '_tkinter' when running main.py. This is likely due to tkinter not being installed or properly configured.
10. On lower-end devices, the animated background and UI effects may cause slight performance issues. The number of particles and animation frequencies have been reduced to mitigate this, but further optimization may be necessary for very low-end devices.
11. The shiny, reflective surface effect on UI elements may not be visible on devices with lower screen resolutions or older graphics cards.

## Current Status

We have successfully implemented the initial prototype with a cyberpunk-inspired GUI using Electron.js and Flask. The interface now features neon colors, glitch effects, and animated elements that align with the desired cyberpunk and zef culture aesthetic. Here's an update on our progress:

1. Cyberpunk-inspired GUI:
   - The interface has been redesigned with a dark background, neon colors, and angular UI elements.
   - Animated background with floating particles has been implemented, creating a futuristic atmosphere.
   - Eyeball mascots have been updated to look more robotic or cybernetic, fitting the cyberpunk theme.

2. Animated background and UI elements:
   - A subtle screen flicker effect has been added to enhance the cyberpunk feel.
   - Buttons and other UI elements now have glitch effects and neon glow animations.
   - Shiny, bubbly surfaces have been added to UI elements with subtle animations.

3. Performance optimization:
   - Animations and effects have been optimized for better performance on lower-end devices.
   - The number of particles, animation frequencies, and effect intensities have been adjusted for a balance between visual appeal and performance.

4. PDF compilation functionality:
   - Basic backend functionality for PDF compilation has been implemented using PyPDF2.
   - Frontend integration with the backend for PDF compilation is in progress.

5. File management:
   - Users can now add and remove PDF files from the compilation list.
   - The interface displays both selected and available PDF files.

6. Cover page and report functionality:
   - Users can enable cover pages and specify page numbers for cover pages.
   - Save and load report functionality has been implemented.

The current focus is on further optimizing performance for smoother animations, especially on lower-end devices, and completing the integration of PDF compilation functionality with the frontend.

Next steps include:
1. Further optimizing the performance of animations and effects for very low-end devices.
2. Completing the integration of PDF compilation functionality with the frontend.
3. Implementing file selection for modifying page ranges of specific PDFs.
4. Enhancing the interactivity of UI elements.
5. Ensuring cross-platform compatibility.
6. Implementing the functionality to add a cover page with new page numbers and a cover letter to the final compiled PDF.
7. Addressing the issue with spaces in file names for PDF compilation and handling.

## Future Improvements

1. Implement better management of report patterns for compilations directly within the application.
2. Add a low-performance mode for devices that struggle with the current animations and effects.
3. Implement progressive enhancement for the shiny, reflective surface effects to ensure compatibility with a wider range of devices.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
