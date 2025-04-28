import sys
from json_stream_parser import load_iter
import json
import traceback
import csv

specializations = {
    250: {
        'class': 'death-knight',
        'specialization': 'blood',
        'role': 'tank'
    },
    251: {
        'class': 'death-knight',
        'specialization': 'frost',
        'role': 'dps'
    },
    252: {
        'class': 'death-knight',
        'specialization': 'unholy',
        'role': 'dps'
    },
    577: {
        'class': 'demon-hunter',
        'specialization': 'havoc',
        'role': 'dps'
    },
    581: {
        'class': 'demon-hunter',
        'specialization': 'vengeance',
        'role': 'tank'
    },
    102: {
        'class': 'druid',
        'specialization': 'balance',
        'role': 'dps'
    },
    103: {
        'class': 'druid',
        'specialization': 'feral',
        'role': 'dps'
    },
    104: {
        'class': 'druid',
        'specialization': 'guardian',
        'role': 'tank'
    },
    105: {
        'class': 'druid',
        'specialization': 'restoration',
        'role': 'healer'
    },
    1467: {
        'class': 'evoker',
        'specialization': 'devastation',
        'role': 'dps'
    },
    1468: {
        'class': 'evoker',
        'specialization': 'preservation',
        'role': 'healer'
    },
    1473: {
        'class': 'evoker',
        'specialization': 'augmentation',
        'role': 'dps'
    },
    253: {
        'class': 'hunter',
        'specialization': 'beast-mastery',
        'role': 'dps'
    },
    254: {
        'class': 'hunter',
        'specialization': 'marksmanship',
        'role': 'dps'
    },
    255: {
        'class': 'hunter',
        'specialization': 'survival',
        'role': 'dps'
    },
    62: {
        'class': 'mage',
        'specialization': 'arcane',
        'role': 'dps'
    },
    63: {
        'class': 'mage',
        'specialization': 'fire',
        'role': 'dps'
    },
    64: {
        'class': 'mage',
        'specialization': 'frost',
        'role': 'dps'
    },
    268: {
        'class': 'monk',
        'specialization': 'brewmaster',
        'role': 'tank'
    },
    270: {
        'class': 'monk',
        'specialization': 'mistweaver',
        'role': 'healer'
    },
    269: {
        'class': 'monk',
        'specialization': 'windwalker',
        'role': 'dps'
    },
    65: {
        'class': 'paladin',
        'specialization': 'holy',
        'role': 'healer'
    },
    66: {
        'class': 'paladin',
        'specialization': 'protection',
        'role': 'tank'
    },
    70: {
        'class': 'paladin',
        'specialization': 'retribution',
        'role': 'dps'
    },
    256: {
        'class': 'priest',
        'specialization': 'discipline',
        'role': 'healer'
    },
    257: {
        'class': 'priest',
        'specialization': 'holy',
        'role': 'healer'
    },
    258: {
        'class': 'priest',
        'specialization': 'shadow',
        'role': 'dps'
    },
    259: {
        'class': 'rogue',
        'specialization': 'assassination',
        'role': 'dps'
    },
    260: {
        'class': 'rogue',
        'specialization': 'outlaw',
        'role': 'dps'
    },
    261: {
        'class': 'rogue',
        'specialization': 'subtlety',
        'role': 'dps'
    },
    262: {
        'class': 'shaman',
        'specialization': 'elemental',
        'role': 'dps'
    },
    263: {
        'class': 'shaman',
        'specialization': 'enhancement',
        'role': 'dps'
    },
    264: {
        'class': 'shaman',
        'specialization': 'restoration',
        'role': 'healer'
    },
    265: {
        'class': 'warlock',
        'specialization': 'affliction',
        'role': 'dps'
    },
    266: {
        'class': 'warlock',
        'specialization': 'demonology',
        'role': 'dps'
    },
    267: {
        'class': 'warlock',
        'specialization': 'destruction',
        'role': 'dps'
    },
    71: {
        'class': 'warrior',
        'specialization': 'arms',
        'role': 'dps'
    },
    72: {
        'class': 'warrior',
        'specialization': 'fury',
        'role': 'dps'
    },
    73: {
        'class': 'warrior',
        'specialization': 'protection',
        'role': 'tank'
    }
}

class MythicPlusRun:
    def __init__(self, data):
        self.keystone_level = data['keystone_level']
        self.keystone_completed_at = data['keystone_completed_at']
        self.keystone_completion_ms = data['keystone_completion_ms']
        self.healer_name = data['healer_name']
        self.healer_realm = data['healer_realm']
        self.tank_name = data['tank_name']
        self.tank_realm = data['tank_name']
        self.dps1_name = data['dps1_name']
        self.dps1_realm = data['dps1_realm']
        self.dps2_name = data['dps2_name']
        self.dps2_realm = data['dps2_realm']
        self.dps3_name = data['dps3_name']
        self.dps3_realm = data['dps3_realm']
        self.data = data
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __hash__(self):
        return hash((
            'keystone_level', self.keystone_level,
            'keystone_completion_ms', self.keystone_completion_ms,
            'keystone_completed_at', self.keystone_completed_at,
            'healer_name', self.healer_name,
            'healer_realm', self.healer_realm,
            'tank_name', self.tank_name,
            'tank_realm', self.tank_realm,
            'dps1_name', self.dps1_name,
            'dps1_realm', self.dps1_realm,
            'dps2_name', self.dps2_name,
            'dps2_realm', self.dps2_realm,
            'dps3_name', self.dps3_name,
            'dps3_realm', self.dps3_realm,
        ))
        

def augment_player(player):
    specialization_data = specializations[player['specialization']['id']]
    return {
        'name': player['profile']['name'],
        'realm': player['profile']['realm']['slug'],
        'faction': player['faction'],
        'role': specialization_data['role'],
        'specialization': specialization_data['specialization'],
        'class': specialization_data['class']
    }
with open('leaderboards.csv', 'w', newline='', encoding='utf-8') as leaderboard, open('./leaderboards.jsonstream', encoding="utf-16-le", errors='ignore') as f:
    writer = csv.writer(leaderboard, quotechar="\"", quoting=csv.QUOTE_NONNUMERIC)
    leaderboard_rows = [
    ]
    while line := f.readline():
        raw_leaderboard = json.loads(line.encode('utf-8'))
        dungeon_id = raw_leaderboard['map']['id']
        dungeon_name = raw_leaderboard['map']['name']['en_US']
        for keystone in raw_leaderboard['leading_groups']:
            try:
                keystone_level = keystone['keystone_level']
                keystone_completion_ms = keystone['duration']
                keystone_completed_at = keystone['completed_timestamp']
                mapped_members = list(map(augment_player, keystone['members']))
                tank_list = list(filter(lambda x: x['role'] == 'tank', mapped_members))
                healer_list = list(filter(lambda x: x['role'] == 'healer', mapped_members))
                dps_list = list(filter(lambda x: x['role'] == 'dps', mapped_members))
                row = {
                    'keystone_level': keystone_level,
                    'keystone_completed_at': keystone_completed_at,
                    'keystone_completion_ms': keystone_completion_ms,
                    'tank_specialization': tank_list[0]['specialization'] if len(tank_list) >= 1 else None,
                    'tank_class': tank_list[0]['class'] if len(tank_list) >= 1 else None,
                    'tank_name': tank_list[0]['name'] if len(tank_list) >= 1 else None,
                    'tank_realm': tank_list[0]['realm'] if len(tank_list) >= 1 else None,
                    'healer_specialization': healer_list[0]['specialization'] if len(healer_list) >= 1 else None,
                    'healer_class': healer_list[0]['class'] if len(healer_list) >= 1 else None,
                    'healer_name': healer_list[0]['name'] if len(healer_list) >= 1 else None,
                    'healer_realm': healer_list[0]['realm'] if len(healer_list) >= 1 else None,
                    'dps1_specialization': dps_list[0]['specialization'] if len(dps_list) >= 1 else None,
                    'dps1_class': dps_list[0]['class'] if len(dps_list) >= 1 else None,
                    'dps1_name': dps_list[0]['name'] if len(dps_list) >= 1 else None,
                    'dps1_realm': dps_list[0]['realm'] if len(dps_list) >= 1 else None,
                    'dps2_specialization': dps_list[1]['specialization'] if len(dps_list) >= 2 else None,
                    'dps2_class': dps_list[1]['class'] if len(dps_list) >= 2 else None,
                    'dps2_name': dps_list[1]['name'] if len(dps_list) >= 2 else None,
                    'dps2_realm': dps_list[1]['realm'] if len(dps_list) >= 2 else None,
                    'dps3_specialization': dps_list[2]['specialization'] if len(dps_list) >= 3 else None,
                    'dps3_class': dps_list[2]['class'] if len(dps_list) >= 3 else None,
                    'dps3_name': dps_list[2]['name'] if len(dps_list) >= 3 else None,
                    'dps3_realm': dps_list[2]['realm'] if len(dps_list) >= 3 else None,
                }
                leaderboard_rows.append(MythicPlusRun(row))
            except Exception as inst:
                print(inst)
                traceback.print_exc()
    filtered_data = set(leaderboard_rows)
    writer.writerow(leaderboard_rows[0].data.keys())
    writer.writerows(map(lambda x: x.data.values(), filtered_data))