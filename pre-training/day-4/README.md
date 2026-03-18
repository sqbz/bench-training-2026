## Example output (GitHub profile fetcher)

```bash
python3 pre-training/day-4/exercise_1.py octocat
username: octocat
bio: None
public repos: 8
followers: 22083

top 5 repos by stars:
- Spoon-Knife | ⭐ 3530 | HTML
- Hello-World | ⭐ 3492 | Unknown
- octocat.github.io | ⭐ 834 | CSS
- hello-worId | ⭐ 723 | Unknown
- git-consortium | ⭐ 699 | Unknown
```

## Example output (Weather CLI)

```bash
python3 pre-training/day-4/exercise_2.py Karachi
city: Karachi, Pakistan
temperature: 27.9°C / 82.2°F
wind speed: 11.2 km/h
description: Overcast
```

## Hardest part

The hardest part was reading the raw JSON carefully and figuring out the exact keys and nesting (`results[0]` from geocoding, then `current` fields from the weather response, and `stargazers_count` from the GitHub repos list) before trying to extract values.

