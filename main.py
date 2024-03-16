import argparse
import os
from loguru import logger

# import sub modules
from upscale import upscale
from make_video import make_video
from extract_frames import extract_frames
from frame_interpolation import frame_interpolation

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--input_file', help='dir to input video clip', required=True, type=str)
    parser.add_argument('--output_file', help='this is an end-to-end script, thus only final output file(at output/{project_name})/{output_file}) name is needed', required=True, type=str)
    parser.add_argument('--fps', help='desired interpolation fps', required=True, type=int)
    parser.add_argument('--num_processes', help='number of process to create for upscaling', default=1, type=int)
    parser.add_argument('--scale_factor', help='upscale factor for each edge', default=2, type=int)
    parser.add_argument('--audio_track', help='audio track for the output video, in case a better audio quality is needed',type=str)
    
    return parser

def main(args):
    # get file name of the input video and remove its postfix
    project_name = os.path.basename(args.input_file).split('.')[0]
    args.output_file = os.path.join(f'./output/{project_name}', args.output_file)
    logger.add(f'./output/{project_name}/execution.log')
    logger.info(f'Output file is located at {args.output_file}.')
    
    # output dirs, no need to modify
    video_frames_extraction_folder = f'./output/{project_name}/images'
    upscale_output_folder = f'./output/{project_name}/images_upscaled'
    upscaled_video = f'./output/{project_name}/upscaled.mp4'
    
    # make output dies
    if not os.path.exists(video_frames_extraction_folder) or not os.path.exists(upscale_output_folder):
        os.makedirs(video_frames_extraction_folder, exist_ok=True)
        os.makedirs(upscale_output_folder, exist_ok=True)
    
    # extract input video into images
    logger.info(f'Extracting video frames to `{video_frames_extraction_folder}`...')
    source_fps, frame_count = extract_frames(args.input_file, video_frames_extraction_folder)
    source_fps = round(source_fps)  # deal with fps like 29.97
    
    # upscale frames to a higher resolution
    logger.info(f'Upscaling video frames from `{video_frames_extraction_folder}` to `{upscale_output_folder}`...')
    upscale(input_folder=video_frames_extraction_folder, 
            output_folder=upscale_output_folder, 
            frame_count=frame_count,
            num_processes=args.num_processes,
            scale_factor=args.scale_factor)
    
    # first output the upscaled video
    logger.info(f'Exporting the upscaled video to `{upscaled_video}`...')
    make_video(image_folder=upscale_output_folder,
               audio_track=args.audio_track, 
               output_video=upscaled_video,
               fps=source_fps)
    
    # then do the frame interpolation
    if source_fps != args.fps:
        logger.info(f'Executing frame interpolation with output `args.output_file`...')
        frame_interpolation(
            input_video=upscaled_video, 
            interpolated_video=args.output_file,
            source_fps=source_fps, fps=args.fps,
        )
    
    logger.info(f'All done with output file `{args.output_file}`.')

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    main(args)