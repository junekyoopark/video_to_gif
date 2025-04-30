import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_video():
    filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv")])
    if filepath:
        entry_video_path.delete(0, tk.END)
        entry_video_path.insert(0, filepath)

def toggle_duration_field():
    if var_full_length.get():
        entry_duration.config(state=tk.DISABLED)
    else:
        entry_duration.config(state=tk.NORMAL)

def convert_to_gif():
    video_path = entry_video_path.get().strip()
    start_time = entry_start_time.get().strip()
    duration = entry_duration.get().strip()
    width = entry_width.get().strip()
    use_full_length = var_full_length.get()

    if not video_path:
        messagebox.showerror("Error", "Please select a video file.")
        return

    gif_path = os.path.splitext(video_path)[0] + ".gif"
    palette_path = "palette.png"

    try:
        filters = f"fps=10,scale={width}:-1:flags=lanczos"

        # Base commands with ffmpeg as first argument
        palette_cmd = ["ffmpeg", "-y"]
        gif_cmd = ["ffmpeg"]

        if start_time:
            palette_cmd += ["-ss", start_time]
            gif_cmd += ["-ss", start_time]

        if not use_full_length:
            palette_cmd += ["-t", duration]
            gif_cmd += ["-t", duration]

        palette_cmd += ["-i", video_path, "-vf", f"{filters},palettegen", palette_path]
        gif_cmd += ["-i", video_path, "-i", palette_path,
                    "-filter_complex", f"{filters}[x];[x][1:v]paletteuse",
                    gif_path]

        subprocess.run(palette_cmd, check=True)
        subprocess.run(gif_cmd, check=True)
        os.remove(palette_path)

        messagebox.showinfo("Success", f"GIF saved to:\n{gif_path}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("FFmpeg Error", f"Conversion failed:\n{e}")

# GUI setup
root = tk.Tk()
root.title("FFmpeg Video to GIF Converter")
root.geometry("460x350")

# Video file input
tk.Label(root, text="Video file:").pack(pady=5)
entry_video_path = tk.Entry(root, width=55)
entry_video_path.pack()
tk.Button(root, text="Browse", command=select_video).pack(pady=5)

# Start time
tk.Label(root, text="Start time (hh:mm:ss):").pack()
entry_start_time = tk.Entry(root)
entry_start_time.insert(0, "00:00:00")
entry_start_time.pack()

# Duration + Checkbox
tk.Label(root, text="Duration (seconds):").pack()
entry_duration = tk.Entry(root)
entry_duration.insert(0, "5")
entry_duration.pack()

var_full_length = tk.BooleanVar()
check_full = tk.Checkbutton(root, text="Convert until end of video", variable=var_full_length, command=toggle_duration_field)
check_full.pack()

# Width
tk.Label(root, text="Output GIF width (e.g., 800):").pack()
entry_width = tk.Entry(root)
entry_width.insert(0, "800")
entry_width.pack()

# Convert button
tk.Button(root, text="Convert to GIF", command=convert_to_gif).pack(pady=20)

root.mainloop()
