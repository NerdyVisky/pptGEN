param(
    [string]$py_path = "C:\Users\aakas\AppData\Local\Programs\Python\Python312\",
    [string]$env_path = 'D:\AakashYadav\00 IITJ RAI\00_SlideReconstruction\pptGEN\pptENV'
)

$env:Path = $py_path + ";" + $env:Path

& $env_path\Scripts\Activate.ps1

python 'D:\AakashYadav\00 IITJ RAI\00_SlideReconstruction\pptGEN\code\content_generator.py'
python 'D:\AakashYadav\00 IITJ RAI\00_SlideReconstruction\pptGEN\code\JSON_generator.py'
python 'D:\AakashYadav\00 IITJ RAI\00_SlideReconstruction\pptGEN\code\PPT_generator.py'