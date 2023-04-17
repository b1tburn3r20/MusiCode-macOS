import cv2
import numpy as np
import pygame


def play_audio(audio_file, volume=1.0):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    # Set the volume here, with the 'volume' argument
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


def pixel_to_ascii(pixel_val):
    ascii_chars = "';, -~|}/#@e+=.$_"
    return ascii_chars[int(pixel_val * len(ascii_chars) / 256)]


# Ascii Art Types below
# ';-~|}/+= - Too Dark
# ';-~|}/#@+= - Right on the cusp.. too much dark
# ';-~|}/#@e+= - Nearly Perfect (issues with eye being too dark and start too light)
# ';, -~|}/#@e+=.$_ - Really really good but could be better
# ';, -~|}/#@e+=.$_
# ';-~|}/#@e+=._ -
# _*!~+^()#&$%@ - Not Dark Enough

# TikTok Filter


def frame_to_ascii(frame, max_width, max_height):
    height, width = frame.shape
    aspect_ratio = width / height

    if max_width / max_height > aspect_ratio:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)

    resized_frame = cv2.resize(
        frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

    ascii_frame = ''
    for i in range(new_height):
        for j in range(new_width):
            ascii_frame += pixel_to_ascii(resized_frame[i][j])
        ascii_frame += '\n'
    return ascii_frame


def main():
    video_path = 'videos/madara.mp4'
    audio_path = 'audios/madaraiam.mp3'

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file.")
        return

    width = 200
    height = 120

    play_audio(audio_path, volume=0.5)  # Set the volume here

    while cap.isOpened() and pygame.mixer.music.get_busy():
        ret, frame = cap.read()

        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(
            gray_frame, (width, height), interpolation=cv2.INTER_AREA)

        ascii_frame = frame_to_ascii(resized_frame, width, height)

        print(ascii_frame)

        cv2.waitKey(30)  # Adjust this value to control the frame rate

    cap.release()
    cv2.destroyAllWindows()

    pygame.mixer.music.stop()  # Stop the audio when the video ends


if __name__ == '__main__':
    main()
