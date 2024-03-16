import os
from moviepy.editor import ImageSequenceClip, AudioFileClip

# sort video by pre-defined rule, see line 14 in `upscale.py`
def get_image_index(x) -> int:
    return int(os.path.basename(x).split('_')[1])

# merge images in the `image folder` into `output_video`
def make_video(image_folder, audio_track, output_video, fps=24):
    # read and sort image list
    image_files = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]
    image_files.sort(key=lambda x: get_image_index(x))
    
    # merge the audio and video
    video = ImageSequenceClip(image_files, fps=fps)
    audio = AudioFileClip(audio_track)
    video = video.set_audio(audio)
    
    # create an output
    video.write_videofile(output_video)