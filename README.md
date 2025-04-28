# Data-Science-Exam

Blizzard Entertainment maintains a near-realtime API collating all Mythic+ leaderboard successfully completed keys, sorted by score. Score is an arbitrary metric calculated based on expected dungeon completion time, actual dungeon completion time and key level.

API details, including all of the calls and their format, is described here: Battle.net API.

For the purpose of this, a third-party library was used: python-ndev-blizzardapi. This API needed a small modification to pass a namespace parameter and the authentication header was passed improperly and needed fixing.

The code to fetch the data is in main.py. This generates a list of JSON objects fetched from the API, one for each request; this is unfiltered.

The API Blizzard provides is structured such that each connected realm (a "grouping" of player servers) has a leaderboard for each dungeon per season. This means that, after fetching all of the data, the dungeon runs need to be compared to isolate these duplicate runs and remove up to 4 additional copies of each.

In addition to this, to make the data more useable in Jupyter, I opted to reformat and curate it in the following ways:
The CSV keys are then keyed by tank_, healer_, dps1_, dps2_, dps3_
The specialization of the character is decoded into a class, specialization and role tuple in order to make data filtering easier
The name and realm of every character is also separated into different parameters

All of this is done in retrofit.py, which uses the leaderboards.jsonstream file generated from main.py