#!/usr/bin/env python3
# Created By: Atri Sarker
# Date: June 4, 2025
# Module used for handling input + OTHER UTILITY


from ugame import audio


# PREPARE THE AUDIO PLAYER
audio.stop()
audio.mute(False)


class Sound:
    # CONSTRUCTOR
    def __init__(self, sound_name: str):
        # GET THE FILE PATH
        sound_file_path = f"Sounds/{sound_name}.wav"
        # READ THE WAV FILE IN BINARY MODE
        self.file = open(sound_file_path, "rb")

    def play(self):
        # PLAY THE AUDIO
        audio.play(self.file)


class Button:
    def __init__(self, bit):
        self.button_bit = bit
        self.state = "NOT_PRESSED"

    def get_state(self, keys_pressed) -> str:
        if keys_pressed & self.button_bit:
            if self.state == "NOT_PRESSED":
                self.state = "PRESSED"
            elif self.state == "PRESSED":
                self.state = "STILL_PRESSED"
        else:
            if self.state == "STILL_PRESSED":
                self.state = "RELEASED"
            else:
                self.state = "NOT_PRESSED"
        # RETURN THE BUTTON STATE
        return self.state


# CLAMPING FUNCTION FOR NUMBERS
def clamp(num: int, min_value: int, max_value: int) -> int:
    if num <= min_value:
        return min_value
    elif num >= max_value:
        return max_value
    else:
        return num
