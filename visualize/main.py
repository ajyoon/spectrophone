import sys
import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageColor

from tqdm import tqdm


length = 20  # seconds
frames_per_second = 1
video_width = 1920
video_height = 1080
strip_ratio = 0.381966
path = 'resources/score.png'
working_dir_location = '.tmp'
working_file_fmt = 'working_%08d.png'
out_path = 'out.mp4'

DEBUG = False

total_frames = frames_per_second * length
strip_width = int(strip_ratio * video_width)
image_display_width = video_width - strip_width


def create_frame(frame_number):
    x_in_source = frame_to_x(frame_number, total_frames, source.width)
    frame = Image.new('RGB', (video_width, video_height), '#ffffff')
    crop_bbox = source_bbox_at_x(x_in_source,
                                 image_display_width, source)
    cropped_source = source.crop(crop_bbox)
    draw_strip(frame, cropped_source)
    frame.paste(cropped_source, (strip_width, 0))
    save_frame(frame, frame_number)


def source_bbox_at_x(x, max_width, source_image):
    x0 = x
    x1 = min(source_image.width - 1, x0 + max_width)
    return (x0, 0, x1, source_image.height)


def frame_to_x(frame_number, total_frames, image_width):
    return int(image_width * (frame_number / total_frames))


def draw_strip(frame, cropped_source):
    drawer = ImageDraw.Draw(frame, 'RGB')
    for y in range(frame.height):
        row_color = cropped_source.getpixel((0, y))
        drawer.line([(0, y), (strip_width, y)], fill=row_color)


def save_frame(image, frame_number):
    image.save(os.path.join(working_dir_location,
                            working_file_fmt % frame_number))


def create_video():
    subprocess.call([
        'ffmpeg',
        '-framerate', str(frames_per_second),
        '-i', os.path.join(working_dir_location, working_file_fmt),
        '-s', f'{video_width}x{video_height}',
        '-vcodec', 'libx264',
        out_path
    ])


def view_result():
    subprocess.call([
        'xdg-open',
        out_path
    ])


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
        source = Image.open(path)
        source = source.resize(
            (int(source.width * (video_height / source.height)),
             video_height),
            Image.BICUBIC)

        for frame_number in tqdm(range(total_frames), 'rendering frames'):
            create_frame(frame_number)

        print('stitching video together with ffmpeg')
        create_video()

        print('launching preview')
        view_result()
    finally:
        if not DEBUG:
            print('cleaning up')
            clean_up()

    print('done')
