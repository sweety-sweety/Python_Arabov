import chardet
import re
from collections import Counter

def detect_encoding(filepath: str) -> str:
    """Определяет кодировку файла"""
    with open(filepath, "rb") as f:
        raw_data = f.read(100000)  # читаем кусок файла
    result = chardet.detect(raw_data)
    return result["encoding"] or "utf-8"

def load_text(filepath: str) -> str:
    """Загружает текст с правильной кодировкой"""
    encoding = detect_encoding(filepath)
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла: {e}")

def analyze_text(text: str) -> dict:
    """Выполняет анализ текста"""
    # Убираем двойные пробелы и лишние символы
    cleaned_text = text.strip()

    # Подсчёт символов
    total_chars = len(cleaned_text)
    total_chars_no_spaces = len(cleaned_text.replace(" ", ""))

    # Подсчёт слов
    words = re.findall(r"\b\w+\b", cleaned_text.lower())
    total_words = len(words)

    # Уникальные слова
    unique_words = len(set(words))

    # Подсчёт предложений
    sentences = re.split(r"[.!?]+", cleaned_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    total_sentences = len(sentences)

    # Топ-10 слов
    counter = Counter(words)
    top_words = counter.most_common(10)

    return {
        "total_words": total_words,
        "total_chars": total_chars,
        "total_chars_no_spaces": total_chars_no_spaces,
        "total_sentences": total_sentences,
        "unique_words": unique_words,
        "top_words": top_words,
    }

def save_report(report_path: str, stats: dict):
    """Сохраняет отчёт в файл"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("📊 Отчёт по анализу текста\n")
        f.write("="*40 + "\n")
        f.write(f"Всего слов: {stats['total_words']}\n")
        f.write(f"Всего символов (с пробелами): {stats['total_chars']}\n")
        f.write(f"Всего символов (без пробелов): {stats['total_chars_no_spaces']}\n")
        f.write(f"Количество предложений: {stats['total_sentences']}\n")
        f.write(f"Уникальных слов: {stats['unique_words']}\n\n")
        f.write("Топ-10 слов:\n")
        for word, count in stats["top_words"]:
            f.write(f" - {word}: {count}\n")
    print(f"✅ Отчёт сохранён в {report_path}")

def main():
    filepath = input("Введите путь к текстовому файлу: ").strip()
    try:
        text = load_text(filepath)
        stats = analyze_text(text)
        save_report("report.txt", stats)
    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()
