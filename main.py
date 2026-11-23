from pathlib import Path
import re

NOTES_DIR = Path("notes")
NOTES_DIR.mkdir(exist_ok=True)


def safe_name(title):
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", title.strip().lower()).strip("-")
    return name[:60] or "untitled"


def list_notes():
    return sorted(NOTES_DIR.glob("*.md"))


def choose_note():
    notes = list_notes()
    if not notes:
        print("No notes saved yet.")
        return None
    for number, path in enumerate(notes, 1):
        print(f"{number}. {path.stem}")
    choice = input("Choose note number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(notes):
        print("Invalid selection.")
        return None
    return notes[int(choice) - 1]


def create_note():
    title = input("Note title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    path = NOTES_DIR / f"{safe_name(title)}.md"
    if path.exists():
        print("That note already exists.")
        return
    print("Write your note. Enter END on a line by itself to save:")
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)
    path.write_text(f"# {title}\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved {path}")


def main():
    while True:
        print("\n=== MARKDOWN NOTES CLI ===")
        print("1. Create note\n2. Read note\n3. Delete note\n4. List notes\n0. Exit")
        choice = input("Select: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            create_note()
        elif choice == "2":
            path = choose_note()
            if path:
                print("\n" + path.read_text(encoding="utf-8"))
        elif choice == "3":
            path = choose_note()
            if path and input(f"Delete {path.stem}? (y/N): ").lower() == "y":
                path.unlink()
                print("Note deleted.")
        elif choice == "4":
            print("\n".join(f"- {p.stem}" for p in list_notes()) or "No notes saved.")
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()
