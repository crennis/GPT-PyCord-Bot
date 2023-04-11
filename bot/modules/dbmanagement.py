import os
import aiosqlite

DB_FILE = os.path.join("config", "database.db")


async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS servers
                (id INTEGER PRIMARY KEY AUTOINCREMENT, server_id TEXT UNIQUE, is_premium INTEGER)'''
        )
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS channels
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id TEXT,
                channel_id TEXT UNIQUE,
                FOREIGN KEY(server_id) REFERENCES servers(id))'''
        )
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS config
                (server_id TEXT,
                channel_id TEXT,
                prefix TEXT,
                gpt INTEGER,
                systemmsg TEXT,
                FOREIGN KEY(server_id) REFERENCES servers(id),
                FOREIGN KEY(channel_id) REFERENCES channels(id))'''
        )
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS chats
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id TEXT,
                channel_id TEXT,
                user_id TEXT,
                username TEXT,
                msgrole TEXT,
                message_id TEXT UNIQUE,
                message TEXT,
                messagecount INTEGER,
                FOREIGN KEY(server_id) REFERENCES servers(id),
                FOREIGN KEY(channel_id) REFERENCES channels(id))'''
        )
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS summaries
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id TEXT,
                channel_id TEXT,
                summary TEXT,
                summarycount INTEGER,
                FOREIGN KEY(server_id) REFERENCES servers(id),
                FOREIGN KEY(channel_id) REFERENCES channels(id))'''
        )
        await db.commit()


async def add_server(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR IGNORE INTO servers (server_id) VALUES (?)', (server_id,))
        await db.commit()


async def remove_server(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM servers WHERE server_id = ?', (server_id,))
        await db.commit()


async def list_servers():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM servers')
        servers = await cursor.fetchall()
        return servers

async def is_premium(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM servers WHERE server_id = ?', (server_id,))
        server = await cursor.fetchone()
        if server[2] == 1:
            return True
        else:
            return False

async def default_premium(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE servers SET is_premium = 0 WHERE server_id = ?', (server_id,))
        await db.commit()

async def set_premium(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE servers SET is_premium = 1 WHERE server_id = ?', (server_id,))
        await db.commit()

async def unset_premium(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('UPDATE servers SET is_premium = 0 WHERE server_id = ?', (server_id,))
        await db.commit()

async def get_server_by_id(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM servers WHERE server_id = ?', (server_id,))
        server = await cursor.fetchone()
        return server

async def add_channel(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR IGNORE INTO channels (server_id, channel_id) VALUES (?, ?)', (server_id, channel_id))
        await db.commit()

async def remove_channel(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM channels WHERE server_id = ? AND channel_id = ?', (server_id, channel_id))
        await db.commit()

async def list_channels(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM channels WHERE server_id = ?', (server_id,))
        channels = await cursor.fetchall()
        return channels

async def get_channel_by_id(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM channels WHERE server_id = ? AND channel_id = ?', (server_id, channel_id))
        channel = await cursor.fetchone()
        return channel

async def add_config(server_id, channel_id, prefix, gpt, systemmsg):
    msg = f'Users are named like this: Username#1234 the #1234 is an identifier and can be ignored. {systemmsg}'
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR IGNORE INTO config (server_id, channel_id, prefix, gpt, systemmsg) VALUES (?, ?, ?, ?, ?)', (server_id, channel_id, prefix, gpt, msg))
        await db.commit()

async def remove_config(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM config WHERE server_id = ? AND channel_id = ?', (server_id, channel_id))
        await db.commit()

async def list_configs(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM config WHERE server_id = ?', (server_id,))
        configs = await cursor.fetchall()
        return configs

async def get_config_by_id(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM config WHERE server_id = ? AND channel_id = ?', (server_id, channel_id))
        config = await cursor.fetchone()
        return config

async def get_channels_by_server(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM channels WHERE server_id = ?', (server_id,))
        channels = await cursor.fetchall()
        return channels

async def get_configs_by_server(server_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM config WHERE server_id = ?', (server_id,))
        configs = await cursor.fetchall()
        return configs

async def add_chat(server_id, channel_id, user_id, username, msgrole, message_id, message, messagecount):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR IGNORE INTO chats (server_id, channel_id, user_id, username, msgrole, message_id, message, messagecount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (server_id, channel_id, user_id, username, msgrole, message_id, message, messagecount))
        await db.commit()

async def remove_chat(server_id, channel_id, message_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM chats WHERE server_id = ? AND channel_id = ? AND message_id = ?', (server_id, channel_id, message_id))
        await db.commit()

async def remove_all_chats(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM chats WHERE server_id = ? AND channel_id = ?', (server_id, channel_id))
        await db.commit()

async def list_chats(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM chats WHERE server_id = ? AND channel_id = ? ORDER BY id ASC LIMIT 150', (server_id, channel_id))
        chats = await cursor.fetchall()
        return chats

async def get_chats_custom(server_id, channel_id, limit):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM chats WHERE server_id = ? AND channel_id = ? ORDER BY id ASC LIMIT ?', (server_id, channel_id, limit))
        chats = await cursor.fetchall()
        return chats

async def get_chat_by_id(server_id, channel_id, message_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM chats WHERE server_id = ? AND channel_id = ? AND message_id = ?', (server_id, channel_id, message_id))
        chat = await cursor.fetchone()
        return chat

async def get_last_chat(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM chats WHERE server_id = ? AND channel_id = ? ORDER BY id DESC LIMIT 1', (server_id, channel_id))
        chat = await cursor.fetchone()
        return chat

async def get_chat_range(server_id, channel_id, start, end):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM chats WHERE server_id = ? AND channel_id = ? AND messagecount >= ? AND messagecount <= ? ORDER BY id ASC', (server_id, channel_id, start, end))
        chats = await cursor.fetchall()
        return chats

async def get_last_twenty_chats(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM chats WHERE server_id = ? AND channel_id = ? ORDER BY id ASC LIMIT 20', (server_id, channel_id))
        chats = await cursor.fetchall()
        return chats

async def add_summary(server_id, channel_id, summary, summarycount):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR IGNORE INTO summaries (server_id, channel_id, summary, summarycount) VALUES (?, ?, ?, ?)', (server_id, channel_id, summary, summarycount))
        await db.commit()

async def remove_summary(id, server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM summaries WHERE id = ? AND server_id = ? AND channel_id = ?', (id, server_id, channel_id))
        await db.commit()

async def list_summaries(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM summaries WHERE server_id = ? AND channel_id = ?', (server_id, channel_id))
        summaries = await cursor.fetchall()
        return summaries

async def get_summary_by_id(id, server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM summaries WHERE id = ? AND server_id = ? AND channel_id = ?', (id, server_id, channel_id))
        summary = await cursor.fetchone()
        return summary

async def get_summary_by_count(server_id, channel_id, summarycount):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM summaries WHERE server_id = ? AND channel_id = ? AND summarycount = ?', (server_id, channel_id, summarycount))
        summary = await cursor.fetchone()
        return summary

async def get_latest_summary(server_id, channel_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT * FROM summaries WHERE server_id = ? AND channel_id = ? ORDER BY id DESC LIMIT 1', (server_id, channel_id))
        summary = await cursor.fetchone()
        return summary

async def add_summary_zero(server_id, channel_id):
    summary = ''
    summarycount = 0
    if await get_latest_summary(server_id, channel_id) is not None:
        if await get_last_chat(server_id, channel_id) is not None:
            new_summary_point = await get_last_chat(server_id, channel_id)
            new_summary_point = int(new_summary_point[8])
            summarycount = new_summary_point + 1


    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR IGNORE INTO summaries (server_id, channel_id, summary, summarycount) VALUES (?, ?, ?, ?)', (server_id, channel_id, summary, summarycount))
        await db.commit()