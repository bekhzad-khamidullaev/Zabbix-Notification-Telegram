#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################
#    Sokolov Dmitry    #
# xx.sokolov@gmail.com #
#  https://t.me/ZbxNTg #
########################
# Detailed instructions for all parameters on https://github.com/xxsokolov/Zabbix-Notification-Telegram
__author__ = "Sokolov Dmitry"
__maintainer__ = "Sokolov Dmitry"
__license__ = "MIT"

config_debug_mode = False
config_exc_info = False
config_cache_file = './monitor/zbxTelegram_files/id.cache'
config_log_file = './monitor/zbxTelegram_files/znt.log'

tg_proxy = False
tg_proxy_server = {'https': 'socks5://username:password@domen:port'}
tg_token = '123123123123:ADDDD_er9beG-fGx33ktYqFkUpAdUtWe2s'

watermark = True
watermark_label = 'Dmitry Sokolov (https://github.com/xxsokolov)'
watermark_font = './monitor/zbxTelegram_files/ArialMT.ttf'
watermark_minimal_height = 30
watermark_fill = 255
watermark_rotate = 0
watermark_expand = True
watermark_text_color = (60, 60, 60)

body_messages = '<b>{subject}</b>{body}{links}{tags}{mentions}'
body_messages_cut_symbol = True
body_messages_max_symbol = 600
body_messages_title = '{title} ({period_time})'

body_messages_url = True
body_messages_url_notes = True
body_messages_url_graphs = True
body_messages_url_host = True
body_messages_url_ack = True
body_messages_url_event = True
body_messages_url_template = '<a href="{url}">{icon}</a>'
body_messages_url_delimiter = ' '
body_messages_url_emoji_no_url = '➖'
body_messages_url_emoji_notes = 'ℹ️'  # URL in trigger
body_messages_url_emoji_graphs = '📊'  # URL history graph item
body_messages_url_emoji_host = '📟'  # URL host
body_messages_url_emoji_ack = '✉️'  # URL update problem
body_messages_url_emoji_event = '📋'  # URL in event

body_messages_tags = True
body_messages_tags_event = True
body_messages_tags_eventid = True
body_messages_tags_itemid = True
body_messages_tags_triggerid = True
body_messages_tags_actionid = True
body_messages_tags_hostid = True
body_messages_tags_trigger_settings = True
body_messages_mentions_settings = True
body_messages_tags_no = '#no_tags'
body_messages_tags_delimiter = ' '
body_messages_tags_prefix_eventid = 'eid_'
body_messages_tags_prefix_itemid = 'iid_'
body_messages_tags_prefix_triggerid = 'tid_'
body_messages_tags_prefix_actionid = 'aid_'
body_messages_tags_prefix_hostid = 'hid_'

trigger_settings_tag = 'ZNTSettings'
trigger_settings_tag_no_graph = 'no_graph'
trigger_settings_tag_no_alert = 'no_alert'
trigger_settings_tag_not_notify = 'not_notify'
trigger_settings_tag_graph_normal = 'graph_normal'
trigger_settings_tag_graph_stacked = 'graph_stacked'
trigger_settings_tag_graph_pie = 'graph_pie'
trigger_settings_tag_graph_exploded = 'graph_exploded'
trigger_settings_tag_graph_period = 'period='  # period=43200

trigger_info_mentions_tag = 'ZNTMentions'

zabbix_keyboard = True
zabbix_keyboard_button_message = 'Message'
zabbix_keyboard_button_acknowledge = 'Acknowledge'
zabbix_keyboard_button_history = 'History'
zabbix_keyboard_button_lastvalue = 'Last value'
zabbix_keyboard_button_graphs = 'Graphs'
zabbix_keyboard_button_offline = 'Offline'
zabbix_keyboard_button_problems = 'Problems'
zabbix_keyboard_row_width = 3

zabbix_api_url = 'http://127.0.0.1/zabbix/'
zabbix_api_login = 'Admin'
zabbix_api_pass = 'zabbix'

zabbix_graph = True
zabbix_graph_period_default = 10800  # 3h
zabbix_graph_chart = '{zabbix_server}chart3.php?' \
                     'name={name}&' \
                     'from=now-{range_time}&' \
                     'to=now&' \
                     'width=900&' \
                     'height=200&' \
                     'items[0][itemid]={itemid}&' \
                     'legend=1&' \
                     'showtriggers=1&' \
                     'showworkperiod=1'

zabbix_host_link = "{zabbix_server}zabbix.php?action=search&search={host}"
zabbix_graph_link = "{zabbix_server}history.php?action=showgraph&itemids[]={itemid}&from=now-{range_time}&to-now"
#zabbix_ack_link = "{zabbix_server}zabbix.php?action=acknowledge.edit&eventids[0]={eventid}"  # Zabbix Server ver > 5
zabbix_ack_link = "{zabbix_server}zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]={eventid}"  # Zabbix Server ver <= 5
zabbix_event_link = "{zabbix_server}tr_events.php?triggerid={triggerid}&eventid={eventid}"


zabbix_status_emoji_map = {
    "Problem": "🚨",
    "Resolved": "✅",
    "Update": "🚧",
    "Not classified": "⁉️",
    "Information": "💙",
    "Warning": "💛",
    "Average": "🧡",
    "High": "❤️",
    "Disaster": "💔",
    "Test": "🚽💩"}

