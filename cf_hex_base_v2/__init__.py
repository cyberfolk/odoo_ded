from . import models
from .utility.constant import BORDERS_MAP


def post_init_hook_cf_hex_base_v2(env):
    env["hex.map"].create([{"name": "Mappa V2 - 01", "type": "v2_nolimit_q"}])
