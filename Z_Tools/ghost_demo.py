import pyautogui
import math
import time

pyautogui.FAILSAFE = True

# Brief pause to let the user get ready
time.sleep(1)

w, h = pyautogui.size()
cx, cy = w/2, h/2

# 1. Take control of mouse and smoothly move to center
pyautogui.moveTo(cx, cy, duration=1.5, tween=pyautogui.easeInOutQuad)

# 2. Draw infinity shape to demonstrate fluid kinematics
for i in range(120):
    t = i / 120 * 2 * math.pi
    x = cx + 300 * math.cos(t)
    # y = A * sin(2t)/2 (Lissajous figure for infinity)
    y = cy + 150 * math.sin(2*t)
    pyautogui.moveTo(x, y, duration=0.01)

# 3. Return to center
pyautogui.moveTo(cx, cy, duration=0.5)

# 4. Show success message (will popup exactly in front of them)
pyautogui.alert(
    text='System Override Complete!\n\nCon chuột của Sếp vừa bị Antigravity AI điều khiển hoàn toàn bằng Toán Học và Python.\n\nNếu sếp đồng ý, lần xuất MP4 tiếp theo em có thể dùng thuật toán này tự động bấm nút "Run iLogic" trong Inventor mà sếp không cần đụng tay!',
    title='🤖 Antigravity Ghost Protocol',
    button='Đỉnh của chóp!'
)
