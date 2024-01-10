# Character Data Structure

```mermaid
erDiagram
    Character {
        int character_id PK
        string Name
        string Race
        string Class
        int Level
        ANY TBD
    }
    Class {
    }
    Race {
    }
    AttributeSet {
        int character_id PK, FK
        string attribute PK
        int value
    }

    Character ||--|{ Class : "has at least one"
    Character ||--|| Race : "has one"
    Character ||--|| AttributeSet : "has one"

```
