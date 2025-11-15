"""
PDF yaratish uchun helper funksiya
Railway va local muhitda ishlashi uchun
"""
import os
import pdfkit

def get_pdfkit_config():
    """
    PDFkit konfiguratsiyasini qaytaradi.
    Railway yoki local muhitni avtomatik aniqlaydi.
    """
    # Railway yoki Linux muhitida
    if os.path.exists("/usr/bin/wkhtmltopdf"):
        return pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    
    # Windows muhitida
    windows_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    if os.path.exists(windows_path):
        return pdfkit.configuration(wkhtmltopdf=windows_path)
    
    # Agar wkhtmltopdf topilmasa, None qaytaradi
    # Bu holda PDF yaratish ishlamaydi
    return None

def create_pdf(html_content: str, output_path: str) -> bool:
    """
    HTML dan PDF yaratadi.
    Muvaffaqiyatli bo'lsa True, aks holda False qaytaradi.
    """
    try:
        config = get_pdfkit_config()
        if config is None:
            print("⚠️ wkhtmltopdf topilmadi. PDF yaratib bo'lmaydi.")
            return False
        
        pdfkit.from_string(html_content, output_path, configuration=config)
        return True
    except Exception as e:
        print(f"⚠️ PDF yaratishda xatolik: {e}")
        return False

