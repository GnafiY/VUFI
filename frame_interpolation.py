import subprocess
from loguru import logger

# frame insertion by calling Practical-RIFE
def frame_interpolation(input_video, interpolated_video, source_fps, fps):
    multi = fps // source_fps   # fps multi factor, for example, a video with 30fps to 60fps has a multi 60 / 2 = 30
    if multi != fps / source_fps:
        logger.warning(f'Note that {fps}(fps) / {source_fps}(source_fps) is not an integer, which may results in incorrest destination fps.')
    
    preset_parameters = "--model ./Practical-RIFE/train_log"
    cmd = f'python ./Practical-RIFE/interpolation_inference.py --video {input_video} --output {interpolated_video} --multi {multi} {preset_parameters}'
    return subprocess.run(cmd, text=True)