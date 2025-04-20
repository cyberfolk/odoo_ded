import logging

from . import models

_logger = logging.getLogger(__name__)


# Nascondo le APP necessarie a installare contacts ma che non mi interessano
def post_init_hook_cf_ded_campaign(env):
    _logger.info("* START * post_init_hook_cf_ded_campaign()")
    env["res.partner"].search([]).write({"rpg_type": ''})
    menu_name_list = [
        "Discuss",
        "Integrations",
        "Project",
        "Planning",
        "Link Tracker",
        "Email Marketing",
        "Sign",
        "Knowledge",
        "Appointments",
        "Surveys",
        "Employees",
        "Calendar",
        "Calendar",
    ]
    menu_list = env['ir.ui.menu'].search([('name', 'in', menu_name_list)])
    menu_list.write({'active': False})
    _logger.info("* END   * post_init_hook_cf_ded_campaign()")
