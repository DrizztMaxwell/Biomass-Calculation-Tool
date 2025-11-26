@echo off
flet build windows ^
  --hidden-import pandas ^
  --hidden-import numpy ^
  --hidden-import sklearn ^
  --hidden-import PIL ^
  --hidden-import flet.core ^
  --add-data "assets;assets" ^
  --product-name "MyApp" ^
  --file-description "My Flet Application"
pause