from ruamel.yaml import YAML
import os


def get_oldest_year():
    try:
        files = os.listdir("original")
        years = []
        for file in files:
            # Split the filename by '-' and try to extract the year
            parts = file.split("-")
            for part in parts:
                if len(part) == 4 and part.isdigit() and part.startswith("20"):
                    year = int(part)
                    years.append(year)
                    break
                elif len(part) == 4 and part.isdigit() and int(part) > 1900:
                    year = int(part)
                    years.append(year)
                    break
        return min(years) if years else None
    except Exception as e:
        print(f"Error getting oldest year: {e}")
        return None


def update_year(starting_year):
    config_path = "_config.yml"
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    try:
        with open(config_path, "r") as file:
            config = yaml.load(file)

        if "starting_year" in config:
            config["starting_year"] = starting_year
        else:
            print("Could not find starting_year in _config.yml, adding it")
            config["starting_year"] = starting_year

        with open(config_path, "w") as file:
            yaml.dump(config, file)
        print(f"Updated starting_year to {starting_year} in _config.yml")
    except Exception as e:
        print(f"Error updating _config.yml: {e}")


def main():
    starting_year = get_oldest_year()
    if starting_year:
        update_year(starting_year)


if __name__ == "__main__":
    main()
