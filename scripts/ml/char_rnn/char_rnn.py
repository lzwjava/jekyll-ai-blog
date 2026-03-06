import os


def main():
    dir_path = "data/names"
    for name in os.listdir(dir_path):
        print(name)
        with open(os.path.join(dir_path, name)) as f:
            # print('name')
            pass
            # print(f.read())


if __name__ == "__main__":
    main()
