# 💕 Auto Chat Flirting Plugin

AI-powered automatic flirty responses to private messages!

## Commands

### Toggle Auto Flirt
```
.flirttoggle
```
Turn auto flirting ON/OFF

### Change Flirting Style
```
.flirtstyle <style>
```
Available styles:
- `playful` - Cheeky and fun 😏
- `romantic` - Sweet and romantic 🌹
- `confident` - Bold and confident 💪
- `sweet` - Cute and wholesome 🥰

**Example:**
```
.flirtstyle playful
```

### Manage Blacklist
```
.flirtblacklist add <user_id>     # Add user to blacklist
.flirtblacklist remove <user_id>  # Remove user
.flirtblacklist list              # View blacklist
```

**Example:**
```
.flirtblacklist add 1234567890
.flirtblacklist list
```

### Set Response Delay
```
.flirtdelay <seconds>
```
Add delay before responding (to look natural)

**Example:**
```
.flirtdelay 2    # Wait 2 seconds before replying
```

### Check Status
```
.flirtstatus
```
View current auto flirt settings

---

## Features

✨ **AI-Powered Replies** - Uses ChatGPT to generate contextual flirty responses
🎭 **Multiple Styles** - Playful, Romantic, Confident, Sweet
🚫 **Blacklist** - Ignore specific users
⏰ **Response Delay** - Make replies look natural
📊 **Status Tracking** - Monitor settings easily

---

## Configuration

Edit `plugins/auto_flirt.py`:

```python
FLIRT_SETTINGS = {
    "enabled": True,           # Master on/off
    "style": "playful",        # Default style
    "auto_reply": True,        # Auto reply enabled
    "blacklist": [],           # Blocked users
    "response_delay": 0,       # Delay in seconds
}
```

---

## How It Works

1. **Message Arrives** - Bot receives private message
2. **AI Processing** - ChatGPT analyzes message context
3. **Reply Generation** - Creates flirty response based on style
4. **Send Reply** - Responds with auto-generated message

---

## Requirements

- OpenAI API key (in `.env`)
- `openai` library (already in requirements.txt)

---

**Enjoy! 💕✨**
