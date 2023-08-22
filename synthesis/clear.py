import os
import shutil

os.chdir(os.path.dirname(__file__))

def main():
    if os.path.exists('sounds/'):
        shutil.rmtree('sounds/')

if __name__ == '__main__':
    main()