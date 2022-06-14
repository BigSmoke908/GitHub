import cv2
from moviepy.editor import *


def split_video(path, video, new_folder):
    # Tutorial bei : https://www.youtube.com/watch?v=RCiJA9GEq-U
    movie = cv2.VideoCapture(path + video)
    counter = 0

    video.split('.')

    while movie.isOpened():
        status, frame = movie.read()
        if not status:
            break
        cv2.imwrite(path + new_folder + str(counter) + '.jpg', frame)
        counter += 1


def recombine(framepath, framecounter, videoname, fps, filetype='.jpg'):
    # Tutorial bei: https://www.youtube.com/watch?v=X4Jw8egqGzI
    clip = []

    for counter in range(1, framecounter):
        clip.append(ImageClip(framepath + str(counter) + filetype).set_duration(1/fps))
    video = concatenate_videoclips(clip, method='compose')
    video.write_videofile(str(videoname) + '.mp4', fps=fps, codec='libx264')
    video.close()


split_video('videotest/', 'recombined.mp4', 'neu/')
# recombine('videotest/split/', 16, 'videotest/recombined', 1)
