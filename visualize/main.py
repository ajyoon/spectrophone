import ctypes
import os
import shutil
import subprocess
import multiprocessing
import random
import time
from collections import namedtuple

import numpy as np
from PIL import Image, ImageDraw
from tqdm import tqdm


length = 60 * 59  # seconds
frames_per_second = 19359 / length  # 1 pix column per frame
video_width = 1920
video_height = 1080
strip_ratio = 0.381966
path = 'resources/the_transistorized_radio.png'
working_dir_location = '.tmp'
working_file_fmt = 'working_%08d.png'
out_path = 'out.mp4'

DEBUG = False

total_frames = int(frames_per_second * length)
strip_width = int(strip_ratio * video_width)
image_display_width = video_width - strip_width


CreateFrameWork = namedtuple('CreateFrameWork',
                             ['process', 'progress', 'progress_bar'])


def create_frames(source_image):
    frame_numbers = [i for i in range(total_frames)]
    random.shuffle(frame_numbers)
    remaining_work = []
    for frame_group in np.array_split(frame_numbers,
                                      multiprocessing.cpu_count()):
        progress = multiprocessing.Value(ctypes.c_ulong, 0)
        process = multiprocessing.Process(
            target=create_frames_worker,
            args=(frame_group, source_image, progress))
        process.start()
        progress_bar = tqdm(total=len(frame_group),
                            desc=f'rendering at {process.pid}')
        remaining_work.append(
            CreateFrameWork(process, progress, progress_bar))

    while True:
        for work in remaining_work:
            work.progress_bar.update(work.progress.value - work.progress_bar.n)
            if not work.process.is_alive():
                work.progress_bar.close()
        remaining_work = [w for w in remaining_work if w.process.is_alive()]
        if not remaining_work:
            break
        time.sleep(0.5)

    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')


def create_frames_worker(frame_numbers, source_image, progress_tracker):
    for i, frame_number in enumerate(frame_numbers):
        create_frame(frame_number, source_image)
        progress_tracker.value = i


def create_frame(frame_number, source):
    if os.path.exists(os.path.join(working_dir_location,
                                   working_file_fmt % frame_number)):
        return
    x_in_source = frame_to_x(frame_number, total_frames, source.width)
    frame = Image.new('L', (video_width, video_height), '#ffffff')
    crop_bbox = source_bbox_at_x(x_in_source,
                                 image_display_width, source)
    cropped_source = source.crop(crop_bbox)
    draw_strip(frame, cropped_source)
    frame.paste(cropped_source, (strip_width, 0))
    save_frame(frame, frame_number)


def source_bbox_at_x(x, max_width, source_image):
    x0 = x
    x1 = min(source_image.width, x0 + max_width)
    return (x0, 0, x1, source_image.height)


def frame_to_x(frame_number, total_frames, image_width):
    return int(image_width * (frame_number / total_frames))


def draw_strip(frame, cropped_source):
    drawer = ImageDraw.Draw(frame, 'L')
    for y in range(frame.height):
        row_color = cropped_source.getpixel((0, y))
        drawer.line([(0, y), (strip_width, y)], fill=row_color)


def save_frame(image, frame_number):
    image.save(os.path.join(working_dir_location,
                            working_file_fmt % frame_number),
               optimize=True,
               compress_level=9)


def create_video():
    command = [
        'ffmpeg',
        '-framerate', str(frames_per_second),
        '-i', os.path.join(working_dir_location, working_file_fmt),
        '-r', str(25),
        '-s', f'{video_width}x{video_height}',
        '-vcodec', 'libx264',
        '-y',
        out_path
    ]
    print(' '.join(command))
    subprocess.call(command)


def clean_up():
    if os.path.isdir(working_dir_location):
        shutil.rmtree(working_dir_location)


if __name__ == '__main__':
    print('preparing workspace')
    if os.path.isdir(working_dir_location):
        shutil.rmtree(working_dir_location)
    os.mkdir(working_dir_location)

    try:
        print('loading source image')
        source = Image.open(path).convert('L')
        source = source.resize(
            (int(source.width * (video_height / source.height)),
             video_height),
            Image.BICUBIC)

        create_frames(source)

        print('stitching video together with ffmpeg')
        create_video()

    finally:
        if not DEBUG:
            print('cleaning up')
            clean_up()

    print('done')
