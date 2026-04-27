import cv2
import numpy as np
from PIL import Image, ImageDraw

# --- настройки ---
INPUT_IMAGE = "input.jpg"
OUTPUT_IMAGE = "output.png"

GRID_SIZE = 10  # размер ячейки (чем меньше — тем детальнее)
SIZES = [8, 10, 12, 15]  # размеры страз (условные)
THRESHOLDS = [60, 120, 180]  # пороги яркости

# --- загрузка изображения ---
img = cv2.imread(INPUT_IMAGE)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h, w = gray.shape

# создаём белый холст
canvas = Image.new("RGB", (w, h), "white")
draw = ImageDraw.Draw(canvas)

# счётчик страз
rhinestones_count = {size: 0 for size in SIZES}

# --- функция выбора размера ---
def get_size(brightness):
    if brightness < THRESHOLDS[0]:
        return SIZES[3]
    elif brightness < THRESHOLDS[1]:
        return SIZES[2]
    elif brightness < THRESHOLDS[2]:
        return SIZES[1]
    else:
        return SIZES[0]

# --- основной цикл ---
for y in range(0, h, GRID_SIZE):
    for x in range(0, w, GRID_SIZE):

        # берём участок
        block = gray[y:y+GRID_SIZE, x:x+GRID_SIZE]
        if block.size == 0:
            continue

        # средняя яркость
        avg = int(np.mean(block))

        # выбираем размер страза
        size = get_size(avg)

        # координаты центра
        cx = x + GRID_SIZE // 2
        cy = y + GRID_SIZE // 2

        # радиус (масштабируем)
        radius = size // 2

        # рисуем круг (страз)
        draw.ellipse(
            (cx - radius, cy - radius, cx + radius, cy + radius),
            fill="black"
        )

        # считаем
        rhinestones_count[size] += 1

# --- сохраняем ---
canvas.save(OUTPUT_IMAGE)

# --- вывод статистики ---
print("Готово!")
print("Количество страз:")
for size, count in rhinestones_count.items():
    print(f"{size} ss: {count}")