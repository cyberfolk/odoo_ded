from . import models


def post_init_hook_cf_hex_base_v3(env):
    env["hex.map"].create([{"name": "Mappa V3 - 03", "type": "v3_no_q"}])
