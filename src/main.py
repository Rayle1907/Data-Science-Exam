from functools import reduce
from scraping.blizzard import Blizzard
import json

blizz = Blizzard(
    client_id = "71506919f732462aa5dd046cf0094930", 
    client_secret = "GLENN3yAxE6PNvwoWVlTowd7gLflRdpx",
    redirect_uri = "https://mandl.tv/"
)
blizz.authorize()
realms = blizz.realms(region = "eu")
seasons = blizz.seasons(region = "eu")
last_season_id = reduce(lambda x, y: x if x > y else y, seasons)
season_info = blizz.season(region = "eu", season = last_season_id)
for x in realms:
    dungeons = blizz.season_dungeons(region = "eu", realm = x)
    for y in dungeons:
        print(json.dumps(blizz.leaderboard(region = "eu", realm = x, dungeon = y['dungeon'], period = y['period'])))