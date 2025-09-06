@echo off
echo Installing PDF OCR Dependencies...
echo ==================================

echo Installing pdf2image...
pip install pdf2image

echo.
echo Installing PyMuPDF...
pip install PyMuPDF

echo.
echo Installing poppler-utils (for pdf2image)...
echo Note: You may need to install poppler-utils separately on Windows
echo Download from: https://github.com/oschwartz10612/poppler-windows/releases/

echo.
echo Installation completed!
echo You can now process PDF files with the OCR tool.
pause
