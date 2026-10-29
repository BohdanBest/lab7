"""
Скрипт для підготовки та розділення набору даних Dogs vs Cats (Завдання 4).
- Перевіряє цілісність кожного зображення (PIL verify).
- Відсіює пошкоджені або порожні файли.
- Розподіляє зображення у співвідношенні 80% Train, 10% Validation, 10% Test.
- Зберігає ідеально збалансовану структуру класів (cats / dogs: 10000 / 1250 / 1250).
"""

import os
import shutil
import random
from pathlib import Path
from PIL import Image

def verify_image(file_path: Path) -> bool:
    """Перевіряє, чи файл є валідним зображенням."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def prepare_dogs_cats_dataset(
    source_dir: Path,
    output_dir: Path,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    seed: int = 42
):
    random.seed(seed)
    splits = ['train', 'validation', 'test']
    classes = ['cats', 'dogs']
    
    print(f"[INFO] Створення цільової структури каталогів: {output_dir}")
    for split in splits:
        for cls in classes:
            target_path = output_dir / split / cls
            shutil.rmtree(target_path, ignore_errors=True)
            target_path.mkdir(parents=True, exist_ok=True)
            
    print(f"[INFO] Сканування вихідної директорії: {source_dir}")
    
    for cls in classes:
        pattern = 'cat.*.jpg' if cls == 'cats' else 'dog.*.jpg'
        files = sorted(list(source_dir.glob(pattern)))
        
        if not files and (source_dir / cls).exists():
            files = sorted(list((source_dir / cls).glob('*.jpg')))
            
        print(f"[INFO] Знайдено {len(files)} зображень для класу '{cls}'")
        
        valid_files = [f for f in files if verify_image(f)]
        print(f"[INFO] Валідних зображень: {len(valid_files)}")
        
        random.shuffle(valid_files)
        
        n_total = len(valid_files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        
        train_files = valid_files[:n_train]
        val_files = valid_files[n_train:n_train + n_val]
        test_files = valid_files[n_train + n_val:]
        
        for split_name, file_list in [('train', train_files), ('validation', val_files), ('test', test_files)]:
            dest_dir = output_dir / split_name / cls
            print(f"[INFO] Копіювання {len(file_list)} файлів -> {dest_dir}")
            for src_file in file_list:
                shutil.copy2(src_file, dest_dir / src_file.name)
                
    print("\n[SUCCESS] Підготовка даних завершена успішно!")
    for split in splits:
        for cls in classes:
            count = len(list((output_dir / split / cls).glob('*')))
            print(f"  - {split}/{cls}: {count} зображень")

if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent.parent
    SRC = BASE_DIR / 'data' / 'dogs-vs-cats' / 'train'
    DST = BASE_DIR / 'data' / 'dogs-vs-cats-processed'
    
    if SRC.exists():
        prepare_dogs_cats_dataset(SRC, DST)
    else:
        print(f"[INFO] Перевірка існуючого каталогу {DST}:")
        for s in ['train', 'validation', 'test']:
            for c in ['cats', 'dogs']:
                p = DST / s / c
                cnt = len(list(p.glob('*'))) if p.exists() else 0
                print(f"  - {s}/{c}: {cnt}")
