from . import models
from .utility.constant import BORDERS_MAP


def post_init_hook_cf_hex_base(env):
    env["hex.macro"].create([{"name": "Mappa V2 - 01", "type": "v2_nolimit_q"}])
    env["hex.macro"].create([{"name": "Mappa V1 - 01", "type": "v1_19_q"}])
