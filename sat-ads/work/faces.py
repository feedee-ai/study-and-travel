# Центр и размер лица по кадрам plate.mp4 (Haar cascade), медиана по каждому куску EDL
import sys, json, cv2, numpy as np
plate, edl = sys.argv[1], json.load(open(sys.argv[2]))
cap = cv2.VideoCapture(plate)
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
res = {}
for k, s in enumerate(edl["segments"]):
    pts = []
    for f in np.linspace(s["t0"] + 0.1, s["t0"] + s["dur"] - 0.1, 6):
        cap.set(cv2.CAP_PROP_POS_MSEC, f * 1000); ok, img = cap.read()
        if not ok: continue
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fs = casc.detectMultiScale(g, 1.1, 6, minSize=(120, 120))
        if len(fs):
            x, y, w, h = max(fs, key=lambda r: r[2] * r[3]); pts.append((x + w / 2, y + h / 2, h))
    if pts:
        m = np.median(np.array(pts), axis=0)
        res[k] = [round(float(m[0])), round(float(m[1])), round(float(m[2]))]
    print(k, s["tag"], s["src"], res.get(k))
json.dump(res, open(sys.argv[3], "w"))
