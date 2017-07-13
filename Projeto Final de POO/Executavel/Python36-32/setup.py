from cx_Freeze import setup, Executable
 
setup(
    name="jogo EXECUTABLE",
    version = "1.0.0",
    description = ".py to .exe",
    executables = [Executable("jogo.py")])
