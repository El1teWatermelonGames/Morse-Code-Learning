import os
import shutil

def main():
    if os.path.exists('sounds/'):
        shutil.rmtree('sounds/')

if __name__ == '__main__':
    main()