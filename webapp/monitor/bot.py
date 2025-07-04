#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple polling bot to handle inline keyboard actions."""

import json
import io
import logging
from openpyxl import Workbook
import telebot
from telebot import apihelper

from django.conf import settings
from webapp.monitor.zbxTelegram import (
    zabbix_api_request,
    get_chart_png,
    get_offline_hosts,
    get_problems,
    get_zabbix_user,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(settings.tg_token)
if settings.tg_proxy:
    apihelper.proxy = settings.tg_proxy_server


def authorize_user(tg_id):
    user = get_zabbix_user(tg_id)
    if not user:
        return None
    return int(user.get('type', 1))


def acknowledge_event(eventid, message="Acknowledged via bot"):
    res = zabbix_api_request('event.acknowledge', {
        'eventids': [eventid],
        'message': message,
    })
    return res is not None


def event_items(eventid):
    data = zabbix_api_request('event.get', {
        'eventids': [eventid],
        'selectItems': 'extend',
        'selectHosts': 'extend',
    })
    if data:
        items = data[0].get('items', [])
        triggerid = data[0].get('objectid')
        host = data[0].get('hosts', [{}])[0].get('host')
        return triggerid, host, [item['itemid'] for item in items]
    return None, None, []


def send_last_value(chat_id, eventid):
    _, host, items = event_items(eventid)
    if not items:
        bot.send_message(chat_id, 'No items found')
        return
    messages = []
    for itemid in items:
        res = zabbix_api_request('item.get', {
            'itemids': [itemid],
            'output': ['name', 'lastvalue'],
        })
        if res:
            item = res[0]
            messages.append(f"{item['name']}: {item['lastvalue']}")
    if messages:
        bot.send_message(chat_id, '\n'.join(messages))
    else:
        bot.send_message(chat_id, 'No values found')


def send_history(chat_id, eventid):
    triggerid, host, _ = event_items(eventid)
    if not triggerid:
        bot.send_message(chat_id, 'No history found')
        return
    events = zabbix_api_request('event.get', {
        'objectids': [triggerid],
        'sortfield': 'clock',
        'sortorder': 'DESC',
        'limit': 5,
        'output': 'extend',
    }) or []
    lines = [f"{e['clock']}: {e['name']}" if 'name' in e else str(e['clock']) for e in events]
    if lines:
        bot.send_message(chat_id, '\n'.join(lines))
    else:
        bot.send_message(chat_id, 'No history available')


def send_graph(chat_id, eventid):
    _, _, items = event_items(eventid)
    if not items:
        bot.send_message(chat_id, 'No graph data')
        return
    img = get_chart_png(items[0], 'graph')
    if img and 'img' in img:
        bot.send_photo(chat_id, img['img'])
    else:
        bot.send_message(chat_id, 'Failed to get graph')


def send_event_messages(chat_id, eventid):
    data = zabbix_api_request('event.get', {
        'eventids': [eventid],
        'select_acknowledges': 'extend',
    })
    if data:
        ack = data[0].get('acknowledges', [])
        if ack:
            lines = [a.get('message', '') for a in ack]
            bot.send_message(chat_id, '\n'.join(lines))
            return
    bot.send_message(chat_id, 'No messages')


def send_offline(chat_id, groups=None):
    offline = get_offline_hosts(groups)
    if offline:
        wb = Workbook()
        ws = wb.active
        ws.append(['Group', 'Host'])
        for grp, host in offline:
            ws.append([grp, host])
        buff = io.BytesIO()
        wb.save(buff)
        buff.seek(0)
        buff.name = 'offline_hosts.xlsx'
        bot.send_document(chat_id, buff,
                          caption=f"Offline hosts: {len(offline)}")
    else:
        bot.send_message(chat_id, 'No offline hosts found')


def send_problems(chat_id, groups=None, severity=None):
    problems = get_problems(groups, severity)
    if not problems:
        bot.send_message(chat_id, 'No active problems')
        return
    lines = []
    for host, name, sev, clk in problems:
        lines.append(f'{host}: {name} (S{sev}) at {clk}')
    bot.send_message(chat_id, '\n'.join(lines))


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_type = authorize_user(message.from_user.id)
    if user_type is None:
        bot.reply_to(message, 'Access denied')
        return
    levels = {1: 'user', 2: 'admin', 3: 'super admin'}
    bot.reply_to(message, f"Zabbix helper bot active. Your role: {levels.get(user_type, 'user')}")


@bot.message_handler(commands=['offline'])
def handle_offline(message):
    if authorize_user(message.from_user.id) is None:
        bot.reply_to(message, 'Access denied')
        return
    parts = message.text.split(maxsplit=1)
    groups = parts[1] if len(parts) > 1 else None
    send_offline(message.chat.id, groups)


@bot.message_handler(commands=['problems'])
def handle_problems(message):
    if authorize_user(message.from_user.id) is None:
        bot.reply_to(message, 'Access denied')
        return
    parts = message.text.split(maxsplit=2)
    groups = parts[1] if len(parts) > 1 else None
    severity = int(parts[2]) if len(parts) > 2 else None
    send_problems(message.chat.id, groups, severity)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if authorize_user(call.from_user.id) is None:
        bot.answer_callback_query(call.id, 'Access denied')
        return
    try:
        data = json.loads(call.data)
    except Exception:
        bot.answer_callback_query(call.id, 'Unknown action')
        return
    action = data.get('action')
    eventid = data.get('eventid')
    chat_id = call.message.chat.id
    if action == 'offline':
        groups = data.get('groups')
        send_offline(chat_id, groups)
        bot.answer_callback_query(call.id)
        return
    if action == 'problems':
        groups = data.get('groups')
        send_problems(chat_id, groups)
        bot.answer_callback_query(call.id)
        return
    if not eventid:
        bot.answer_callback_query(call.id, 'No event id')
        return
    if action == 'acknowledge':
        if acknowledge_event(eventid):
            bot.answer_callback_query(call.id, 'Acknowledged')
        else:
            bot.answer_callback_query(call.id, 'Ack failed')
    elif action == 'messages':
        send_event_messages(chat_id, eventid)
        bot.answer_callback_query(call.id)
    elif action == 'history':
        send_history(chat_id, eventid)
        bot.answer_callback_query(call.id)
    elif action == 'last value':
        send_last_value(chat_id, eventid)
        bot.answer_callback_query(call.id)
    elif action == 'graphs':
        send_graph(chat_id, eventid)
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, 'Unknown')


if __name__ == '__main__':
    logger.info('Starting polling bot')
    bot.infinity_polling()
