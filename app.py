import moviepy.editor as mp

# Load the video to check its details
video_path = '/mnt/data/画面録画 2025-11-23 221540.mp4'
video_clip = mp.VideoFileClip(video_path)

# Get video details such as duration and resolution
video_duration = video_clip.duration
video_resolution = video_clip.size

video_duration, video_resolution
