# from requests_oauthlib import OAuth2Session
import re
from .api import BlizzardAPI

def extract_leaderboard_data_from_season_record(record):
    realm, dungeon, period = re.findall(r'\d+', record['key']['href'])
    return { 'realm': int(realm), 'dungeon': int(dungeon), 'period': int(period) }
class Blizzard:
    def __init__(self, client_id, client_secret):
        self.clientId = client_id
        self.clientSecret = client_secret
    
    def realms(self, region):
        realms = self.api.wow.game.connected_realm.get_connected_realms_index(region = region, locale = "en_US", namespace = "dynamic")
        return list(map(lambda x: re.findall(r'\d+', x['href'])[0], realms['connected_realms']))
    def leaderboard_periods(self, connected_realm_id):
        self.api.wow.game_data.get_mythic_keystone_leaderboards_index()
    def seasons(self, region):
        seasons = self.api.wow.game.mythic_keystone_dungeon.get_mythic_keystone_seasons_index(region = region, namespace = "dynamic")
        return list(map(lambda x: int(x['id']), seasons['seasons']))
    def season(self, region, season):
        season_data = self.api.wow.game.mythic_keystone_dungeon.get_mythic_keystone_season(season_id = season, region = region, namespace = "dynamic")
        return season_data
    def season_dungeons(self, region, realm):
        seasons = self.api.wow.game.mythic_keystone_leaderboard.get_mythic_keystone_leaderboards_index(region = region, namespace = "dynamic", connected_realm_id = realm)
        return list(map(extract_leaderboard_data_from_season_record, seasons['current_leaderboards']))
    def leaderboard(self, region, realm, dungeon, period):
        return self.api.wow.game.mythic_keystone_leaderboard.get_mythic_keystone_leaderboard(realm, dungeon, period, region = region)
    def authorize(self):
        self.api = BlizzardAPI(self.clientId, self.clientSecret)