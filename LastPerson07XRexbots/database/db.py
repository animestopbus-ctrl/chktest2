# db.py
# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official
# DEVs: 1. @DmOwner 2. @akaza7902

import motor.motor_asyncio
import datetime
from config import DB_NAME, DB_URI
from LastPerson07XRexbots.logger import LOGGER
from cachetools import TTLCache  # Added for caching (high traffic)

logger = LOGGER(__name__)

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        # Cache for frequent checks (TTL 60s)
        self.cache = TTLCache(maxsize=10000, ttl=60)

    async def async_init(self):
        # Index for high traffic queries (async creation with sparse=True to avoid conflicts)
        await self.col.create_index([("id", 1)], unique=True, sparse=True)
        logger.info("Database indexes created successfully")

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            session = None,
            daily_usage = 0,
            limit_reset_time = None,
            is_premium = False,
            premium_expiry = None,
            total_saves = 0,
            caption = None,
            thumbnail = None,
            delete_words = [],
            replace_words = {},
            dump_chat = None,
            is_banned = False
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
        self.cache[f"user_exist_{id}"] = True
        logger.info(f"New user added to DB: {id} - {name}")
    
    async def is_user_exist(self, id):
        cache_key = f"user_exist_{id}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        user = await self.col.find_one({'id':int(id)})
        exists = bool(user)
        self.cache[cache_key] = exists
        return exists
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
        del self.cache[f"user_exist_{user_id}"]
        logger.info(f"User deleted from DB: {user_id}")

    async def set_session(self, id, session):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': session}})

    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('session') if user else None

    async def del_session(self, id):
        await self.col.update_one({'id': int(id)}, {'$unset': {'session': ""}})

    # Caption Support
    async def set_caption(self, id, caption):
        await self.col.update_one({'id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None)

    async def del_caption(self, id):
        await self.col.update_one({'id': int(id)}, {'$unset': {'caption': ""}})

    # Thumbnail Support
    async def set_thumbnail(self, id, thumbnail):
        await self.col.update_one({'id': int(id)}, {'$set': {'thumbnail': thumbnail}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail', None)

    async def del_thumbnail(self, id):
        await self.col.update_one({'id': int(id)}, {'$unset': {'thumbnail': ""}})

    # Delete Words
    async def set_delete_words(self, id, words):
        await self.col.update_one({'id': int(id)}, {'$addToSet': {'delete_words': {'$each': words}}})

    async def get_delete_words(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('delete_words', [])

    async def remove_delete_words(self, id, words):
        await self.col.update_one({'id': int(id)}, {'$pull': {'delete_words': {'$in': words}}})

    # Replace Words
    async def set_replace_words(self, id, repl_dict):
        user = await self.col.find_one({'id': int(id)})
        current_repl = user.get('replace_words', {})
        current_repl.update(repl_dict)
        await self.col.update_one({'id': int(id)}, {'$set': {'replace_words': current_repl}})

    async def get_replace_words(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('replace_words', {})

    async def remove_replace_words(self, id, targets):
        user = await self.col.find_one({'id': int(id)})
        current_repl = user.get('replace_words', {})
        for t in targets:
            current_repl.pop(t, None)
        await self.col.update_one({'id': int(id)}, {'$set': {'replace_words': current_repl}})

    # Dump Chat Support
    async def set_dump_chat(self, id, chat_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'dump_chat': int(chat_id)}})

    async def get_dump_chat(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('dump_chat', None)

    # Premium Support (Merged from OG)
    async def add_premium(self, id, expiry_date):
        # When user buys premium, we also reset their limits just in case
        await self.col.update_one({'id': int(id)}, {
            '$set': {
                'is_premium': True,
                'premium_expiry': expiry_date,
                'daily_usage': 0,
                'limit_reset_time': None
            }
        })
        logger.info(f"User {id} granted premium until {expiry_date}")

    async def remove_premium(self, id):
        await self.col.update_one({'id': int(id)}, {'$set': {'is_premium': False, 'premium_expiry': None}})
        logger.info(f"User {id} removed from premium")

    async def check_premium(self, id):
        user = await self.col.find_one({'id': int(id)})
        if not user or not user.get('is_premium'):
            return False
        expiry = user.get('premium_expiry')
        if expiry and datetime.datetime.fromisoformat(expiry) < datetime.datetime.now():
            await self.remove_premium(id)
            return False
        return True

    async def get_premium_users(self):
        return self.col.find({'is_premium': True})

    # Ban Support (Merged from OG)
    async def ban_user(self, id):
        await self.col.update_one({'id': int(id)}, {'$set': {'is_banned': True}})
        logger.warning(f"User banned: {id}")

    async def unban_user(self, id):
        await self.col.update_one({'id': int(id)}, {'$set': {'is_banned': False}})
        logger.info(f"User unbanned: {id}")

    async def is_banned(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('is_banned', False) if user else False

    # Daily Limits (Merged and Optimized from OG)
    async def check_limit(self, id):
        """
        Checks if a user has hit their daily limit.
        Returns: True if BLOCKED (limit reached), False if ALLOWED.
        """
        if await self.check_premium(id):
            return False  # Premium unlimited
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return False
        
        now = datetime.datetime.now()
        reset_time = user.get('limit_reset_time')
        
        if reset_time is None or now >= reset_time:
            await self.col.update_one(
                {'id': int(id)}, 
                {'$set': {'daily_usage': 0, 'limit_reset_time': now + datetime.timedelta(hours=24)}}
            )
            return False

        usage = user.get('daily_usage', 0)
        return usage >= 10

    async def add_traffic(self, id):
        if await self.check_premium(id):
            await self.col.update_one({'id': int(id)}, {'$inc': {'total_saves': 1}})
            return

        user = await self.col.find_one({'id': int(id)})
        now = datetime.datetime.now()
        reset_time = user.get('limit_reset_time')

        if reset_time is None:
            new_reset = now + datetime.timedelta(hours=24)
            await self.col.update_one(
                {'id': int(id)}, 
                {'$set': {'daily_usage': 1, 'limit_reset_time': new_reset}, '$inc': {'total_saves': 1}}
            )
        else:
            await self.col.update_one(
                {'id': int(id)}, 
                {'$inc': {'daily_usage': 1, 'total_saves': 1}}
            )

db = Database(DB_URI, DB_NAME)

# LastPerson07XRexbots V2
# Don't Remove Credit
# Telegram Channel @RexBots_Official

# DEVs: 1. @DmOwner 2. @akaza7902
