from moviepy.editor import VideoFileClip, vfx

# Load the video file
input_video_path = r"C:\Users\JASON\Downloads\Untitled.mp4"
output_video_path = r"C:\Users\JASON\Videos\Screen Recordings\Screen Recording LinkedIn1.75_speed_up.mp4"

# Load the video clip
clip = VideoFileClip(input_video_path)

# Set the speed factor
speed_factor = 1.75

# Speed up the video
sped_up_clip = clip.fx(vfx.speedx, speed_factor)

# Write the result to a new file
sped_up_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
