import fitz  # PyMuPDF
import os
from PIL import Image

def generate_pdf_thumbnail(pdf_path, output_path, width=400):
    """
    Generate a thumbnail image from the first page of a PDF.
    """
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        # Get the first page
        page = doc.load_page(0)
        # Render page to a pixmap (image)
        pix = page.get_pixmap()
        
        # Save pixmap to a temporary file
        temp_img_path = output_path + ".temp.png"
        pix.save(temp_img_path)
        
        # Open with PIL for resizing and final saving
        img = Image.open(temp_img_path)
        
        # Calculate height to maintain aspect ratio
        w_percent = (width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        
        img = img.resize((width, h_size), Image.Resampling.LANCZOS)
        
        # Save as JPG
        img.convert('RGB').save(output_path, 'JPEG', quality=85)
        
        # Clean up temp file
        os.remove(temp_img_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Error generating thumbnail: {str(e)}")
        return False
