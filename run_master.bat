@echo off
echo Running master with 2 workers...
echo.
echo Enter Iris flower measurements (4 values in cm):
echo Format: sepal_length,sepal_width,petal_length,petal_width
echo Example: 5.1,3.5,1.4,0.2
echo.
set /p sample="Measurements: "
python master.py http://localhost:5000,http://localhost:5001 "%sample%"
