import json
import pathlib


ROOT_PATH = pathlib.Path(r"C:\software_projects\python\dnd-player-helper\data\feat")

KEY = "prerequisite"
SUB_KEY = "ends"
VALUE = "permanent"


def main():
    keys = set()
    keys_of_interest = set()
    for json_path in ROOT_PATH.glob("*.json"):
        with open(json_path, "r") as f:
            data = json.load(f)
        keys.update(data.keys())
        if KEY in data:
            print(data["name"])
            print(data.get(KEY))

        # for k, v in data[KEY].items():
        #     # print(k)
        #     keys_of_interest.update(v.keys()) if k == "distance" else None

    print(sorted(keys))
    # print(sorted(keys_of_interest))


if __name__ == "__main__":
    main()
