# Character Data Structure

Name
Level
Attributes
Race
Class

```mermaid
erDiagram
    Character {
        string Name
        string Race
        string Class
        int Level
    }
    Class {
        string Name
        string source
        list proficiencies
        list optionalfeatureProgression
        dict startingProficiencies
        dict startingEquipment
        dict multiclassing
        list classTableGroups
        list classFeatures
        dict hit_dice
        string(optional) spellcastingAbility
        string(optional) casterProgression
        int(optional) number_of_prepared_spells
        list[int](optional) cantrip_progression


    }
    Race {
        string Name
        string Source
        string Size
        int speed
        list abilities
        int max_age
        int mature_age
        int darkvision
        list trait_tags
        list language_proficiencies
        list weapon_proficiencies
        list resist
        list flavour_text

    }
    AttributeSet {
        int Strength
        int Dexterity
        int Constitution
        int Intelligence
        int Wisdom
        int Charisma
    }

    Feature {
        string name
        string source
        string class_name
        string class_source
        int level
        list entries
    }

    SubclassFeature {
        string name
        string source
        string class_name
        string class_source
        string subclassShortName
        string subclassSource
        int level
        list entries
    }

    Subclass {
        string Name
        string ShortName
        string Source
        string ClassName
        string ClassSource
        list(optional) Spells

    }

    Character ||--|{ Class : "has at least one"
    Character ||--|| Race : "has one"
    Character ||--|| AttributeSet : "has one"
    Class ||--o{ Feature : "has 0 or more"
    Class ||--o{ Subclass : "has 0 or more"
    Subclass ||--o{ SubclassFeature : "has 0 or more"

```
