import shutil
import sys
import os

import synthesis.generate
import synthesis.clear

def main():
    pass

def startup():
    if not os.path.exists('synthesis/sounds/'):
        synthesis.generate.generate_beeps()

    main()

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-clr':
        synthesis.clear.main()
        exit(0)

    startup()