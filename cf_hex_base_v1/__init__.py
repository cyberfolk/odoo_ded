from . import models
from .utility.constant import BORDERS_MAP


def post_init_hook_cf_hex_base_v1(env):
    env["hex.map"].create([{"name": "Mappa V1 - 01", "type": "v1_19_q"}])
