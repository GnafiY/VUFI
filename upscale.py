import subprocess
import multiprocessing
from tqdm import tqdm

# define such a class for using `multiprocessing.Pool.imap_unordered`
class image_upscaler:
    def __init__(self, input_folder, output_folder, scale_factor):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.scale_factor = scale_factor
    
    # call executable by Real-ESRGAN(https://github.com/xinntao/Real-ESRGAN/)
    def upscale_single_image(self, frame_index):
        # here name rule for upscaled frames is defined, i.e. `{self.output_folder}/frame_{frame_index}_upscaled.jpg` 
        preset_parameters = '-m ./Real-SERGAN/models -n realesr-animevideov3'
        cmd = f'./Real-SERGAN/realesrgan-ncnn-vulkan.exe -i {self.input_folder}/frame_{frame_index}.jpg -o {self.output_folder}/frame_{frame_index}_upscaled.jpg -s {self.scale_factor} {preset_parameters}'
        return subprocess.run(cmd, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

def upscale(input_folder, output_folder, frame_count, num_processes, scale_factor):
    upscaler = image_upscaler(
        input_folder=input_folder,
        output_folder=output_folder,
        scale_factor=scale_factor,
    )
    
    pool = multiprocessing.Pool(num_processes)
    with tqdm(total=frame_count) as pbar:
        for _ in pool.imap_unordered(upscaler.upscale_single_image, range(frame_count)):
            pbar.update()
    
    pool.close()
    pool.join()