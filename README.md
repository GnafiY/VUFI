Anime video upscaler and frame-interpolator made from [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN/) and [Practical-RIFE](https://github.com/hzwer/Practical-RIFE/).

create environment:
```bash
conda env create -f environment.yml -n video-upscale
conda activate video-upscale
```

usage: 
```bash
python main.py --input_file ./test/test.mp4 --audio_track ./test/test.wav --output_file test_processed.mp4
               --fps 60 --num_processes 8 --scale_factor 2
```

You may first generate a pair test data to get familiar with the script.
```python
from moviepy.editor import VideoFileClip

video = VideoFileClip("test.mp4")
audio = video.audio
audio.write_audiofile("test.wav")
```