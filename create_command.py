"""
Simple /create command handler for escrow group creation
"""
import logging
import uuid
from telegram import Update
from telegram.ext import ContextTypes
import telegram_group_manager
import database

logger = logging.getLogger(__name__)

async def create_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /create command - creates an escrow group
    Simple command - no arguments needed
    """
    user_id = update.effective_user.id
    
    # Generate short deal ID (5 chars for matching reference)
    deal_id = str(uuid.uuid4())[:5]
    
    await update.message.reply_text(
        "<b>Creating escrow group... Please wait.</b>",
        parse_mode='HTML'
    )
    
    try:
        # Create group using admin session from database
        result = await telegram_group_manager.create_escrow_group(
            deal_id=deal_id,
            bot_username=context.bot.username
        )
        
        if not result['success']:
            error_msg = result.get('error', 'Unknown error')
            await update.message.reply_text(
                f"<b>❌ Error creating group:</b> {error_msg}\n\n"
                f"Please try again or contact support.",
                parse_mode='HTML'
            )
            return
        
        # Store in database
        group_id = result['group_id']
        invite_link = result['invite_link']
        
        # Store deal (use 0 for seller if not specified)
        try:
            database.create_deal(deal_id, user_id, 0, group_id)
        except:
            pass  # Database might not have function yet
        
        # Send formatted success message matching reference bot
        success_message = telegram_group_manager.format_group_created_message(
            deal_id=deal_id,
            invite_link=invite_link
        )
        
        await update.message.reply_text(
            success_message,
            parse_mode='HTML',
            disable_web_page_preview=False
        )
        
        # Log success
        logger.info(f"✅ Escrow group #{deal_id} created successfully by user {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Error in /create command: {e}")
        import traceback
        traceback.print_exc()
        await update.message.reply_text(
            f"<b>❌ Error creating group:</b> {str(e)}\n\n"
            f"Please try again or contact support.",
            parse_mode='HTML'
        )
