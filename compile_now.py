import os
from local_overleaf import compile_latex

if __name__ == "__main__":
    print("Starting compilation...")
    success, message = compile_latex()
    if success:
        print("Success!")
        print(message)
    else:
        print("Failed!")
        print(message)
