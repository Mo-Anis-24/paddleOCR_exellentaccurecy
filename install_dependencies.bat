@echo off
echo Installing PaddleOCR Dependencies...
echo ====================================

echo Installing PaddlePaddle GPU...
pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

echo.
echo Installing PaddleOCR...
pip install paddleocr

echo.
echo Installing numpy...
pip install -U numpy==1.26.4

echo.
echo Upgrading PaddleOCR...
pip install --upgrade paddleocr

echo.
echo Installing additional dependencies...
pip install opencv-python matplotlib

echo.
echo Cloning PaddleOCR repository...
if not exist "PaddleOCR" (
    git clone https://github.com/PaddlePaddle/PaddleOCR.git
) else (
    echo PaddleOCR directory already exists
)

echo.
echo Installation completed!
echo You can now run: python paddle_ocr_working.py
pause
