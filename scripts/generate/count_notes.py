import os


def count_notes(since_mtime=None):
    try:
        files = [
            f for f in os.listdir("notes") if os.path.isfile(os.path.join("notes", f))
        ]
        if since_mtime is not None:
            files = [
                f
                for f in files
                if os.path.getmtime(os.path.join("notes", f)) >= since_mtime
            ]
        return len(files)
    except FileNotFoundError:
        return 0


if __name__ == "__main__":
    print(count_notes())
