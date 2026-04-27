import flet as ft
import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
import base64
from io import BytesIO

# --- настройки ---
GRID_SIZE = 10  # размер ячейки (чем меньше — тем детальнее)
SIZES = [8, 10, 12, 15]  # размеры страз (условные)
THRESHOLDS = [60, 120, 180]  # пороги яркости

def main(page: ft.Page):
    page.title = "Загрузка и обработка изображения"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Переменные для хранения данных
    selected_file = ft.Text("Файл не выбран")
    image_display = ft.Image(src="", width=400, height=400)  # Убрали fit=ft.ImageFit.CONTAIN, так как ImageFit не найден в модуле flet
    result_text = ft.Text("Результат обработки: ")

    # Функция выбора размера (из вашего кода)
    def get_size(brightness):
        if brightness < THRESHOLDS[0]:
            return SIZES[3]
        elif brightness < THRESHOLDS[1]:
            return SIZES[2]
        elif brightness < THRESHOLDS[2]:
            return SIZES[1]
        else:
            return SIZES[0]

    # Функция обработки изображения (адаптированная из вашего кода)
    def process_image(file_path):
        img = cv2.imread(file_path)
        if img is None:
            return "Ошибка: Не удалось загрузить изображение"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # создаём белый холст
        canvas = Image.new("RGB", (w, h), "white")
        draw = ImageDraw.Draw(canvas)

        # счётчик страз
        rhinestones_count = {size: 0 for size in SIZES}

        # --- основной цикл ---
        for y in range(0, h, GRID_SIZE):
            for x in range(0, w, GRID_SIZE):
                block = gray[y:y+GRID_SIZE, x:x+GRID_SIZE]
                if block.size == 0:
                    continue
                avg = int(np.mean(block))
                size = get_size(avg)
                rhinestones_count[size] += 1

                # рисуем круг (страза)
                draw.ellipse((x - size//2, y - size//2, x + size//2, y + size//2), fill=(0, 0, 0))

        # сохраняем результат
        output_path = "output.png"
        canvas.save(output_path)
        return f"Обработка завершена. Сохранено как {output_path}. Количество страз: {rhinestones_count}"

    # Функция для конвертации изображения в base64
    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"

    # Обработчик выбора файла
    def on_file_selected(e):
        if e.files:
            file = e.files[0]
            selected_file.value = f"Выбран файл: {file.name}"
            # Исправление: конвертируем изображение в base64 для отображения
            image_display.src = image_to_base64(file.path)
            result = process_image(file.path)
            result_text.value = result
        else:
            selected_file.value = "Файл не выбран"
            image_display.src = ""
            result_text.value = "Результат обработки: "
        page.update()

    # Создаём FilePicker
    file_picker = ft.FilePicker()
    file_picker.on_result = on_file_selected
    page.overlay.append(file_picker)

    # Кнопка для открытия диалога выбора файла
    pick_button = ft.ElevatedButton(
        "Выбрать изображение",
        on_click=lambda _: file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)
    )

    # Добавляем элементы на страницу
    page.add(
        ft.Column([
            pick_button,
            selected_file,
            image_display,
            result_text,
        ])
    )

# Запуск приложения
ft.app(target=main)