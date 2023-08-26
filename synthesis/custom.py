import generate
import os

os.chdir(os.path.dirname(__file__))

def generate_custom():
    while True:
        string = input('Type "e" to exit or type a string to generate audio for:\n').lower()
        if string == 'e':
            break
        else:
            generate.generate_multiple('#' + string)

if __name__ == '__main__':
    if not os.path.exists('sounds/'):
        generate.generate_beeps()

    generate_custom()