from . import models


def post_init_hook_cf_hex_base_v2(env):
    env["hex.map"].create([{"name": "Mappa V2 - 01", "type": "v2_nolimit_q"}])
