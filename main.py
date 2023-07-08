import cv2
import os
import moviepy.editor as mp


def compress_video(input_file, output_file, bitrate='1000k'):
    video = mp.VideoFileClip(input_file)
    compressed_video = video.resize(height=360)
    compressed_video.write_videofile(output_file, bitrate=bitrate)


def get_file_size(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_megabytes = size_in_bytes / (1024 * 1024)
    return size_in_megabytes


# Input video file path
input_file = input("Masukkan path file video: ")

# Output video file path
output_folder = "compressed"
output_file = os.path.join(output_folder, "compressed_video.mp4")

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Compression
compress_video(input_file, output_file)

# Get initial and final file sizes
initial_size = get_file_size(input_file)
final_size = get_file_size(output_file)

print("Ukuran awal file:", initial_size, "MB")
print("Ukuran akhir file:", final_size, "MB")


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    color = "Undefined"
    if hue_value < 5:
        color = "RED"
    if hue_value < 22:
        color = "ORANGE"
    if hue_value < 33:
        color = "YELLOW"
    if hue_value < 131:
        color = "BLUE"
    if hue_value < 170:
        color = "VIOLET"
    else:
        color = "RED"

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(
        pixel_center_bgr[1]), int(pixel_center_bgr[2])

    cv2.putText(frame, color, (10, 70), 0, 1.5, (b, g, r), 2)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
