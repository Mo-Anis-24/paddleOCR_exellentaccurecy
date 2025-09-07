@echo off
echo Installing OCR Dependencies...
echo.
echo Installing core dependencies...
pip install paddlepaddle-gpu==3.0.0 paddleocr numpy==1.26.4 opencv-python matplotlib Pillow
echo.
echo Installing PDF dependencies...
pip install pdf2image PyMuPDF
echo.
echo Installation completed!
echo.
echo Note: For Windows users, you may need to install Poppler for PDF processing:
echo Download from: https://github.com/oschwartz10612/poppler-windows/releases/
echo Extract and add the 'bin' folder to your system PATH.
echo.
pause


