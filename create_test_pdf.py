from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "This is a test PDF file")
    c.drawString(100, 730, "Page 1")
    c.showPage()
    c.drawString(100, 750, "This is page 2 of the test PDF file")
    c.drawString(100, 730, "Page 2")
    c.save()

if __name__ == "__main__":
    create_test_pdf("test.pdf")
    print("Test PDF created successfully.")
