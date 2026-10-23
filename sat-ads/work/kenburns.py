# Пролёт камеры по фото (субпиксельно, без дрожи): kenburns.py IN.jpg OUT.mp4 DUR "cx0,cy0,h0" "cx1,cy1,h1"
# окно 9:16 с центром (cx,cy) и высотой h в пикселях исходника; кривая — sine.inOut
import sys, subprocess, math, cv2, numpy as np
src, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
a = [float(v) for v in sys.argv[4].split(",")]; b = [float(v) for v in sys.argv[5].split(",")]
img = cv2.imread(src, cv2.IMREAD_COLOR)
W, H, FPS = 1080, 1920, 30
n = round(dur * FPS)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-vf", "eq=contrast=1.04:saturation=1.05,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "15",
                      "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / max(1, n - 1); e = 0.5 - 0.5 * math.cos(math.pi * t)
    # масштаб интерполируем логарифмически — скорость наезда ощущается равномерной
    h = math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * e)
    cx = a[0] + (b[0] - a[0]) * e; cy = a[1] + (b[1] - a[1]) * e
    s = H / h
    M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
    p.stdin.write(cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
p.stdin.close(); p.wait()
