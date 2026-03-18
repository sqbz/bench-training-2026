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

The hardest part was figuring out “where the data lives” in the API response. The geocoding API gives a list of matches, so I had to grab the first one to get latitude/longitude, and then the weather API puts the actual numbers under `current`. For GitHub, each repo has its own `stargazers_count`, so I had to sort the repos by that field to get the top 5.

