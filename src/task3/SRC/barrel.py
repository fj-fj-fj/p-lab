import datetime
import random
from pathlib import Path

MEGABYTE = 1048576

PEOPLE_COUNT = 10

FILE = 'log.log'


class Barrel:

    def __init__(self, volume=200):
        self._VOLUME = self.cur_volume = volume
        self._top_up = self._scoop = None
        self.last_act = 'no yet'

    @property
    def top_up(self): return self._top_up

    @property
    def scoop(self): return self._scoop

    @top_up.setter
    def top_up(self, vol):
        self._top_up = self._set_volume(self, vol)

    @scoop.setter
    def scoop(self, vol):
        self._scoop = self._set_volume(self, -vol)
    
    def _set_volume(self, _, vol):
        final_value = self._get_final_value(vol)
        return self._set_cur_volume(final_value)

    def _get_final_value(self, vol):
        candidat = self.cur_volume + vol
        acceptably = 0 < candidat < self._VOLUME
        self._logger_info(vol, acceptably)
        return candidat if acceptably else self._VOLUME if vol > 0 else 0

    def _set_cur_volume(self, volume):
        self.cur_volume = volume
        return volume

    def _logger_info(self, vol, status):
        self.last_act = (
            f"{datetime.datetime.today().isoformat()[:-3]}Z"
            f" - [username{random.randint(1, PEOPLE_COUNT)}] - wanna "
            f"{'top up' if vol > 0 else 'scoop'} "
            f"{abs(vol)}l ({('фейл', 'успех')[status]})\n"
        )

barrel = Barrel(200)

with open(Path(__file__).with_name(FILE), 'w', encoding='utf-8') as f:
    f.write(f"META DATA:\n{barrel._VOLUME} (объем бочки)\n")
    while Path(__file__).with_name(FILE).stat().st_size < MEGABYTE:
        setattr(barrel, random.choice(['top_up', 'scoop']), random.randint(0, barrel._VOLUME))
        f.write(barrel.last_act)
