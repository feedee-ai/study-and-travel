# broll.py — вставки из стока Mixkit: кроп 9:16, 1080x1920, 30 к/с, мягкий грейд под тёплый осенний футаж
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); STOCK = os.environ["STOCK"]
GRADE = "eq=contrast=1.04:saturation=0.95,colortemperature=temperature=5800:mix=0.25,curves=all='0/0.03 0.5/0.5 1/0.98'"
# (ролик, имя, клип Mixkit, старт, длительность, центр кропа по x)
CLIPS = [
    ("v1", "travel1", "v8954", 2.0, 1.4, 0.45),   # девушка с рюкзаком кружится на старой европейской улице
    ("v1", "travel2", "v4683", 0.8, 1.4, 0.62),   # девушка у телескопа над городом
    ("v2", "friends", "v8900", 1.0, 1.9, 0.52),   # студенты с кофе смеются на улице
    ("v2", "campus",  "v5937", 3.3, 2.2, 0.30),   # студентки смеются на кампусе
]
for vid, name, clip, ss, dur, xc in CLIPS:
    out = f"{HERE}/../{vid}/hf/assets/media/{name}.mp4"
    vf = (f"setpts=PTS-STARTPTS,fps=30,crop=ih*9/16:ih:max(0\\,min(iw-ih*9/16\\,iw*{xc}-ih*9/32)):0,"
          f"scale=1080:1920:flags=lanczos,{GRADE},unsharp=5:5:0.5:5:5:0,setsar=1,format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(dur + 0.5), "-i", f"{STOCK}/{clip}.mp4", "-vf", vf, "-t", str(dur + 0.4),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-an",
                    "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], check=True)
    print(name, "ok")
