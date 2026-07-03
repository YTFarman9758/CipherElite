"""
Auto Chat Flirting Plugin
Automatically responds to private messages with AI-powered flirty replies
"""

import asyncio
import logging
from telethon import events
from telethon.tl.types import PeerUser
import openai
from config.config import Config
from utils.decorators import sudo_only

logger = logging.getLogger(__name__)

# Store flirting settings
FLIRT_SETTINGS = {
    "enabled": True,
    "style": "playful",  # playful, romantic, confident, sweet
    "auto_reply": True,
    "blacklist": [],
    "response_delay": 0,  # seconds
}

FLIRT_PROMPTS = {
    "playful": """You are a flirty, playful, and witty chat bot. 
    Respond to this message with a short, cheeky, and fun flirty reply (max 100 chars).
    Keep it light-hearted and teasing. Use emojis if appropriate.
    Message: {msg}
    Reply:""",
    
    "romantic": """You are a romantic and charming chat bot.
    Respond to this message with a sweet, romantic flirty reply (max 100 chars).
    Be genuine and heartfelt. Use emojis if appropriate.
    Message: {msg}
    Reply:""",
    
    "confident": """You are a confident and bold chat bot.
    Respond to this message with a confident and flirty reply (max 100 chars).
    Be bold but respectful. Use emojis if appropriate.
    Message: {msg}
    Reply:""",
    
    "sweet": """You are a cute and sweet chat bot.
    Respond to this message with an adorable and flirty reply (max 100 chars).
    Be wholesome and kind. Use emojis if appropriate.
    Message: {msg}
    Reply:""",
}

class AutoFlirtManager:
    def __init__(self, client):
        self.client = client
        self.settings = FLIRT_SETTINGS.copy()
        
    async def generate_flirty_reply(self, message_text: str) -> str:
        """Generate flirty reply using AI"""
        try:
            style = self.settings["style"]
            prompt = FLIRT_PROMPTS[style].format(msg=message_text)
            
            # Using OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly flirty chat bot."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50,
            )
            
            reply = response.choices[0].message.content.strip()
            return reply
            
        except Exception as e:
            logger.error(f"Error generating flirty reply: {e}")
            return self.get_fallback_reply(message_text)
    
    def get_fallback_reply(self, message_text: str) -> str:
        """Fallback replies if AI fails"""
        fallbacks = {
            "playful": [
                "Ooh, interesting! 😏",
                "Got my attention 👀",
                "Smooth talker, huh? 😉",
                "I like where this is going 😏",
                "Not bad, not bad 😏💕",
            ],
            "romantic": [
                "You're making me blush 😊💕",
                "That's sweet of you 🥰",
                "You know how to charm someone 💕",
                "Getting romantic, are we? 😘",
                "My heart just skipped a beat 💗",
            ],
            "confident": [
                "I like your style 💪",
                "Bold move, I like it 😏",
                "You got game 🔥",
                "Not impressed... just kidding 😄",
                "You're cool, I'll give you that 😏",
            ],
            "sweet": [
                "Awww, that's adorable 🥺💕",
                "You're so kind 🥰",
                "Making me smile over here 😊",
                "That's really sweet 💗",
                "You seem nice 🥺✨",
            ],
        }
        
        import random
        style_replies = fallbacks.get(self.settings["style"], fallbacks["playful"])
        return random.choice(style_replies)
    
    async def should_reply(self, user_id: int) -> bool:
        """Check if should reply to this user"""
        if not self.settings["auto_reply"]:
            return False
        if user_id in self.settings["blacklist"]:
            return False
        return True


# Initialize manager
flirt_manager = None

async def setup_auto_flirt(client):
    """Setup auto flirt plugin"""
    global flirt_manager
    flirt_manager = AutoFlirtManager(client)
    logger.info("Auto Flirt plugin initialized")


@events.register(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_private_message(event):
    """Handle incoming private messages"""
    if not flirt_manager or not flirt_manager.settings["auto_reply"]:
        return
    
    sender_id = event.sender_id
    message_text = event.text
    
    # Skip if message is empty or from self
    if not message_text or sender_id == event.client.get_me().id:
        return
    
    # Check if should reply
    if not await flirt_manager.should_reply(sender_id):
        return
    
    try:
        # Generate flirty reply
        flirty_reply = await flirt_manager.generate_flirty_reply(message_text)
        
        # Add delay if configured
        if flirt_manager.settings["response_delay"] > 0:
            await asyncio.sleep(flirt_manager.settings["response_delay"])
        
        # Send reply
        await event.respond(flirty_reply)
        logger.info(f"Auto-replied to {sender_id}: {flirty_reply}")
        
    except Exception as e:
        logger.error(f"Error in auto flirt: {e}")


# Commands for managing auto flirt

@sudo_only
async def cmd_flirt_toggle(event):
    """Toggle auto flirt ON/OFF"""
    flirt_manager.settings["auto_reply"] = not flirt_manager.settings["auto_reply"]
    status = "✅ ON" if flirt_manager.settings["auto_reply"] else "❌ OFF"
    await event.edit(f"Auto Flirt: {status}")


@sudo_only
async def cmd_flirt_style(event, style: str):
    """Change flirting style"""
    if style not in FLIRT_PROMPTS:
        await event.edit(f"❌ Invalid style! Use: {', '.join(FLIRT_PROMPTS.keys())}")
        return
    
    flirt_manager.settings["style"] = style
    await event.edit(f"✅ Flirt style changed to: **{style}**")


@sudo_only
async def cmd_flirt_blacklist(event, action: str, user_id: int = None):
    """Manage blacklist"""
    if action == "add" and user_id:
        flirt_manager.settings["blacklist"].append(user_id)
        await event.edit(f"✅ User {user_id} added to blacklist")
    elif action == "remove" and user_id:
        if user_id in flirt_manager.settings["blacklist"]:
            flirt_manager.settings["blacklist"].remove(user_id)
            await event.edit(f"✅ User {user_id} removed from blacklist")
    elif action == "list":
        blacklist = flirt_manager.settings["blacklist"]
        if blacklist:
            await event.edit(f"🚫 Blacklist: {', '.join(map(str, blacklist))}")
        else:
            await event.edit("✅ Blacklist is empty")


@sudo_only
async def cmd_flirt_delay(event, seconds: int):
    """Set response delay"""
    flirt_manager.settings["response_delay"] = seconds
    await event.edit(f"✅ Response delay set to {seconds} seconds")


@sudo_only
async def cmd_flirt_status(event):
    """Show auto flirt status"""
    status_text = f"""
🎭 **Auto Flirt Status**
━━━━━━━━━━━━━━━━━━━
✅ Status: {'ON' if flirt_manager.settings['auto_reply'] else 'OFF'}
💕 Style: {flirt_manager.settings['style']}
⏰ Delay: {flirt_manager.settings['response_delay']}s
🚫 Blacklist: {len(flirt_manager.settings['blacklist'])} users
"""
    await event.edit(status_text)


# Register commands
PLUGIN_COMMANDS = {
    "flirttoggle": cmd_flirt_toggle,
    "flirtstyle": cmd_flirt_style,
    "flirtblacklist": cmd_flirt_blacklist,
    "flirtdelay": cmd_flirt_delay,
    "flirtstatus": cmd_flirt_status,
}
