$pythonPath = "C:\Users\91997\AppData\Local\Programs\Python\Python311"
$env:Path = $pythonPath + ";" + $env:Path

& 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\pptgen\Scripts\Activate.ps1'

python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\JSON_generator.py'
python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\PPT_generator.py'