echo off
color 0a
REM Non-admin path: C:\Users\%USERNAME%\AppData\Roaming\Python\Python311\Scripts
cls
echo.
echo Pip3 installs needed packages. Requires internet. Run as administrator.
echo.
pause
echo Updating pip as needed...
python.exe -m pip install --upgrade pip
echo Downloading and Installing required packages...
REM for function overloading
pip3 install multipledispatch
REM for mouse and keyboard automation
pip3 install point2d
pip3 install pyautogui
REM for Windows OS functionality
pip3 install pywin32
REM for screen grab
pip3 install dxcam
REM for OCR
pip3 install tensorflow
pip3 install keras-ocr
echo.
echo Script completed.
echo.
pause