from sqlmodel import Session
from dnd_player_helper.dnd_model.dnd_model import DNDModel


def main() -> None:
    model = DNDModel(echo=False)
    races = model.get_all_races()
    for r in races:
        print(r.name, r.source)
        print("-" * 20)
        for age in r.ages:
            print(age.age_type, age.age_in_years)
        print("-" * 20)
        for w in r.weapon_proficiencies:
            print(w.weapon, w.source)
        print("-" * 20)
        for d in r.descriptions:
            print(d)
            for l in d.list_data:
                print(l)
            for t in d.table_data:
                print(t)
            for inset in d.inset_data:
                print(inset)

        print("=" * 20)


if __name__ == "__main__":
    main()
