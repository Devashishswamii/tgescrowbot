# Quick Fix for Koyeb Bot Conflict

## Problem
```
ERROR: Conflict: terminated by other getUpdates request; 
make sure that only one bot instance is running
```

## Cause
- Multiple bot instances trying to use polling (getUpdates)
- OR a webhook is set from previous deployment
- OR local instance still running

## IMMEDIATE SOLUTIONS

### Solution 1: Delete Webhook (Try This First!)
Run this command to clear any existing webhook:

```bash
curl "https://api.telegram.org/bot8470449689:AAEHH4KZJi2TCqcWOxpVO0MtHDcTukaEN0k/deleteWebhook?drop_pending_updates=true"
```

Then redeploy on Koyeb.

### Solution 2: Check if Local Bot is Running
- Stop ANY local instances of bot.py
- Check Task Manager / Activity Monitor for python processes
- Kill any bot.py processes

### Solution 3: Force Single Instance in Code
The bot.py already calls `deleteWebhook()` on startup, but Koyeb might be creating multiple containers.

**Check Koyeb Settings:**
1. Go to Koyeb dashboard
2. Make sure "Instances" is set to **1** (not auto-scaling)
3. Disable auto-scaling if enabled

### Solution 4: Add Startup Delay
If Koyeb restarts too fast, add a small delay before polling starts.

---

## Recommended: Stay with Polling for Now
Since your bot is already using polling and it works locally, just ensure:
1. ✅ Only ONE instance on Koyeb
2. ✅ Webhook is deleted
3. ✅ No local bots running

The error will stop once there's only ONE bot instance using getUpdates.
