# ../synthesis/main.py

import shutil
import numpy
import wave
import os

SAMPLE_RATE = 44100

AUDIO_DOT = None
AUDIO_DASH = None

LIST_BASE = ['A', 'B', 'C', 'D', 'E',
             'F', 'G', 'H', 'I', 'J',
             'K', 'L', 'M', 'N', 'O',
             'P', 'Q', 'R', 'S', 'T',
             'U', 'V', 'W', 'X', 'Y',
             'Z',
             '1', '2', '3', '4', '5',
             '6', '7', '8', '9', '0',
             '?', '!', '.', ',', ';',
             ':', '+', '-', '/', '=',
             ' ']

LIST_MORSE = ['.-', '-...', '-.-.', '-..', '.',
              '..-.', '--.', '....', '..', '.---',
              '-.-', '.-..', '--', '-.', '---',
              '.--.', '--.-', '.-.', '...', '-',
              '..-', '...-', '.--', '-..-', '-.--',
              '--..',
              '.----', '..---', '...--', '....-', '.....',
              '-....', '--...', '---..', '----.', '-----',
              '..--..', '-.-.--', '.-.-.-', '--..--', '-.-.-.',
              '---...', '.-.-.', '-....-', '-..-.', '-...-',
              ' ']

LIST_MORSE = [s + '|' for s in LIST_MORSE]

SPECIAL_CHARACTERS_BASE = ['?', '!', '.', ',', ';',
                           ':', '+', '-', '/', '=',
                           ' ']

SPECIAL_CHARACTERS_SAFE = ['~question~', '~exclamation~', '~period~', '~comma~', '~semi_colon~',
                           '~colon~', '~plus~', '~dash~', '~f_slash~', '~equal~',
                           '~space~']

os.chdir(os.path.dirname(__file__))

def save_wav(audio, filename) -> None:
    with wave.open(f'sounds/{filename}.wav', 'w') as wav_file:
        wav_file.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        wav_file.writeframes(audio.tobytes())

def generate_noise(duration) -> numpy.ndarray:
    t = numpy.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    signal = 1 * numpy.sin(2 * numpy.pi * 440 * t)
    return numpy.int16(signal * 32767)

def generate_single(duration, name) -> None:
    save_wav(generate_noise(duration), name)
    print(f'Generated: {name}.wav')

def generate_multiple(string) -> None:
    audio_clips = []
    for char in string.upper():
        char_morse = LIST_MORSE[LIST_BASE.index(char)]
        for i in range(len(char_morse)):
            if char_morse[i] == '.':
                audio_clips.append('sounds/!DOT.wav')
            elif char_morse[i] == '-':
                audio_clips.append('sounds/!DASH.wav')
            elif char_morse[i] == '|' or char_morse[i] == ' ':
                pass
            else:
                raise Exception('Invalid morse character')
            
            if char_morse[i] == '|':
                audio_clips.append('sounds/!GAP_LETTER.wav')
            elif char_morse[i + 1] != '|':
                audio_clips.append('sounds/!GAP_SYMBOL.wav')
            elif char_morse[i] == ' ':
                audio_clips.append('sounds/!GAP_WORD.wav')
    
    combine_wav(audio_clips, string)

def replace_characters(string, chars_to_replace, replacement_chars):
    if len(chars_to_replace) != len(replacement_chars):
        raise ValueError('Lists have differing lengths')
    
    trans_table = {ord(char): repl for char, repl in zip(chars_to_replace, replacement_chars)}
    modified_string = string.translate(trans_table)

    return modified_string

def combine_wav(audio_clips, name):
    if ' '.join(LIST_BASE) == name:
        name = '~ALL_SOUNDS'
    name = replace_characters(name, SPECIAL_CHARACTERS_BASE, SPECIAL_CHARACTERS_SAFE)

    with wave.open(f'sounds/{name}.wav', 'wb') as wav_file:
        wav_file.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))

        for audio_clip in audio_clips:
            with wave.open(audio_clip, 'rb') as wav_input:
                if (wav_input.getnchannels() != 1 or
                    wav_input.getsampwidth() != 2 or
                    wav_input.getframerate() != SAMPLE_RATE):
                    print(f'WARNING: \'{audio_clip}\' does not have matching parameters')
                    continue

                frames = wav_input.readframes(wav_input.getnframes())
                wav_file.writeframes(frames)
    print(f'Generated: {name}.wav')

def generate_silence(duration, name):
    num_channels = 1
    sample_width = 2

    num_frames = int(SAMPLE_RATE * duration)
    silent_sample = b'\x00\x00'

    with wave.open(f'sounds/{name}.wav', 'w') as wave_file:
        wave_file.setparams((num_channels, sample_width, SAMPLE_RATE, num_frames, 'NONE', 'not compressed'))

        empty_bytes = silent_sample * num_frames

        #for _ in range(num_frames):
        #    empty_bytes += silent_sample
        wave_file.writeframes(empty_bytes)

    print(f'Generated: {name}.wav')

def generate_beeps() -> None:
    if os.path.exists('sounds/'):
        shutil.rmtree('sounds/')

    os.mkdir('sounds/')

    # 1 time unit is 0.25s

    # --- BASE SOUNDS ---
    generate_single(0.25, '!DOT')
    generate_single(0.75, '!DASH')

    # --- SILENCE SOUNDS ---
    generate_silence(0.25, '!GAP_SYMBOL')
    generate_silence(0.75, '!GAP_LETTER')
    generate_silence(1.75, '!GAP_WORD')

    # --- CYCLE ALPHABETICAL SOUNDS ---
    for character in LIST_BASE[:-1]:
        generate_multiple(character)

    # --- ALL SOUNDS ---
    generate_multiple(' '.join(LIST_BASE))

if __name__ == '__main__':
    generate_beeps()