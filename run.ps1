param(
    [string]$py_path = "C:\Users\91997\AppData\Local\Programs\Python\Python311",
    [string]$env_path = 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\pptgen'
)

$env:Path = $py_path + ";" + $env:Path

& $env_path\Scripts\Activate.ps1

python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\topics_generator.py'
python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\content_generator.py'
python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\JSON_generator.py'
python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\PPT_generator.py'
python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\pptx_to_png.py'
python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\annotations.py'
python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\utils\tracer.py'
# python 'D:\Research_work\Experimentation_Results\py_pptx_code_gen_using_LLMs\pptGEN\code\utils\junkfiles.py'