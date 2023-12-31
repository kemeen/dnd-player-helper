# Database Structure

```mermaid
erDiagram
    Character {
        string Name
        int Level
        list Attributes
        list Skills
        list Feats
        list Features
    }
    Class {
        string Name
    }
    Race {
        string Name
    }
    Character ||--|| Class : "main"
    Character ||--o{ Class : "multi"
    Character ||--|| Race : "has a"

```
