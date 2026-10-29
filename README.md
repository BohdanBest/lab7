# Лабораторна робота №7: Підготовка власного набору зображень в Keras

**Дисципліна:** Глибокі нейронні мережі (Deep Learning)  
**Рівень:** 4 курс  
**Виконано згідно з методичними вказівками до лабораторної роботи 7 та індивідуальними умовами кафедри.**

---

## 📌 Огляд проєкту

У роботі реалізовано повний цикл підготовки, потокового завантаження та класифікації зображень за допомогою згорткових нейромереж (CNN) в екосистемі **TensorFlow / Keras**:
1. **Завдання 1 (Horses vs Humans, $300 \times 300$):** Потоковий пайплайн `ImageDataGenerator`, автоматична валідація, аналіз кривих збіжності, стрес-тестування на нетипових фото з інтернету (спроби "обдурити" модель).
2. **Завдання 2 (Horses vs Humans, $150 \times 150$):** Дослідження впливу просторового стиснення зображень (зменшення пікселів у 4 рази) та скорочення кількості згорткових блоків (вилучення 4-го та 5-го блоків, вихідна розмірність $17 \times 17$ перед `Flatten`), порівняльний бенчмаркінг ресурсів і точності.
3. **Завдання 3 (Happy or Sad, 80 смайлів):** Згорткова нейромережа з кастомним `Callback` (`tf.keras.callbacks.Callback`), що гарантує зупинку при досягненні точності $\ge 99.9\%$ менш ніж за 15 епох із обов'язковим повідомленням:  
   `"Досягнуто 99,9% точності, тому скасовуємо навчання!"`.
4. **Завдання 4 (Dogs vs Cats, 25 000 фото):** 
   - Автономний скрипт підготовки та валідації цілісності даних `src/prepare_dogs_cats_data.py` (спліт: 80% train, 10% validation, 10% test).
   - Побудова та навчання згорткової нейромережі з регулярним шаром `Dropout(0.5)` та оптимізатором `RMSprop(learning_rate=0.001)`.
   - Збереження навченої моделі в `models/dogs_vs_cats_model.keras`.
   - Оцінка на тестовому наборі даних (Test Set Accuracy, Confusion Matrix).
   - Тестування на 20 власних фотографіях (10 котів і 10 собак).
   - Експеримент з кадруванням (Crop): аналіз 6 зображень на складному фоні до та після обрізки, дослідження локалізації рецептивного поля.

---

## 📁 Структура репозиторію

```text
lab7/
├── data/
│   ├── HappyVsSad/data/               # Датасет смайлів (happy: 40, sad: 40)
│   ├── horses-vs-humans/              # Датасети коней та людей (train: 1027, validation: 256)
│   │   ├── train/ {horses, humans}
│   │   └── validation/ {horses, humans}
│   ├── dogs-vs-cats/train/            # Вихідний архів Kaggle (25 000 фото)
│   └── dogs-vs-cats-processed/        # Результат роботи скрипта підготовки
│       ├── train/ {cats: 10000, dogs: 10000}
│       ├── validation/ {cats: 1250, dogs: 1250}
│       └── test/ {cats: 1250, dogs: 1250}
├── notebooks/
│   ├── 01_horses_vs_humans_validation.ipynb       # Ноутбук з кодом: завдання 1
│   ├── 02_horses_vs_humans_compression.ipynb      # Ноутбук з кодом: завдання 2
│   ├── 03_happy_or_sad_callback.ipynb             # Ноутбук з кодом: завдання 3
│   └── 04_dogs_vs_cats_classification.ipynb       # Ноутбук з кодом: завдання 4
├── src/
│   ├── prepare_dogs_cats_data.py      # Скрипт валідації та розділення датасету Dogs vs Cats
│   ├── setup_test_images.py           # Підготовка тестових фото та генерація cropped-версій
│   ├── train_all_models.py            # Повний пайплайн навчання всіх 4 моделей
│   ├── build_notebooks.py             # Генератор інтерактивних Jupyter ноутбуків
│   └── generate_docx_report.py        # Генератор академічного звіту у Word (.docx)
├── test_images/
│   ├── horses_humans/                 # Нетипові сторонні фото (сукня, вершник, тощо)
│   ├── custom_cats/                   # 10 тестових зображень котів
│   ├── custom_dogs/                   # 10 тестових зображень собак
│   ├── raw/                           # 6 складних фото на строкатому фоні
│   └── cropped/                       # 6 обрізаних версій (Crop)
├── models/
│   ├── horses_vs_humans_300.keras     # Збережена модель Завдання 1
│   ├── horses_vs_humans_150.keras     # Збережена модель Завдання 2
│   ├── happy_or_sad_model.keras       # Збережена модель Завдання 3
│   └── dogs_vs_cats_model.keras       # Збережена модель Завдання 4
├── results/
│   ├── figures/                       # Графіки навчання, матриці помилок та порівняння кадрування
│   └── metrics/                       # JSON-файли з фінальними метриками
├── docs/
│   ├── Lab7_Report.md                 # Повний звіт у форматі Markdown
│   └── Lab7_Report.docx               # Офіційний звіт у форматі Microsoft Word
└── requirements.txt                   # Зафіксовані залежності проєкту
```

---

## 🚀 Інструкція запуску та відтворення результатів

### 1. Активація віртуального середовища та встановлення залежностей
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Розділення датасету Dogs vs Cats (Завдання 2.1)
```bash
python src/prepare_dogs_cats_data.py --source-dir data/dogs-vs-cats/train --output-dir data/dogs-vs-cats-processed
```

### 3. Підготовка тестових фото та кадрування (Завдання 2.3)
```bash
python src/setup_test_images.py
```

### 4. Навчання моделей та збереження результатів
```bash
python src/train_all_models.py
```

### 5. Генерація Jupyter ноутбуків та офіційного звіту
```bash
python src/build_notebooks.py
python src/generate_docx_report.py
```

---

## 📊 Матриця обов'язкових результатів (Checklist захисту)

| № | Вимога кафедри | Файл у репозиторії |
|---|---|---|
| 1 | Ноутбук з кодом: завдання 1 | `notebooks/01_horses_vs_humans_validation.ipynb` |
| 2 | Ноутбук з кодом: завдання 2 | `notebooks/02_horses_vs_humans_compression.ipynb` |
| 3 | Ноутбук з кодом: завдання 3 | `notebooks/03_happy_or_sad_callback.ipynb` |
| 4 | Код по підготовці і розділенню даних | `src/prepare_dogs_cats_data.py` |
| 5 | Структура каталогів із даними | `data/dogs-vs-cats-processed/` |
| 6 | Ноутбук з кодом: завдання 4 | `notebooks/04_dogs_vs_cats_classification.ipynb` |
| 7 | Результат тестування, оцінка на test, Crop | `results/figures/` + `models/dogs_vs_cats_model.keras` |
| 8 | Звіт і ЗАХИСТ | `docs/Lab7_Report.docx` та `docs/Lab7_Report.md` |
