import logging
from typing import Optional
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from telegram.constants import ParseMode
from config.settings import settings
from database.models import SessionLocal, Vacancy, Application

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.application = None

    async def start(self):
        """Запуск бота"""
        self.application = Application.builder().token(self.bot_token).build()

        # Регистрация обработчиков
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("search", self.search_command))
        self.application.add_handler(CommandHandler("applications", self.applications_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

        logger.info("Telegram bot started")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def stop(self):
        """Остановка бота"""
        if self.application:
            await self.application.stop()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
🤖 *HH Auto Apply Bot*

Доступные команды:
/start - Показать это сообщение
/stats - Статистика откликов
/search - Запустить поиск вакансий сейчас
/applications - Последние 10 откликов
        """
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Статистика откликов"""
        db = SessionLocal()
        try:
            total_vacancies = db.query(Vacancy).count()
            total_applications = db.query(Application).count()
            today_applications = db.query(Application).filter(
                Application.applied_at >= datetime.now().date()
            ).count()

            stats_text = f"""
📊 *Статистика откликов*

Всего вакансий в базе: *{total_vacancies}*
Всего отправлено откликов: *{total_applications}*
Откликов сегодня: *{today_applications}*
            """

            await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
        finally:
            db.close()

    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Запуск поиска вакансий"""
        await update.message.reply_text("🔍 Запускаю поиск вакансий...")
        # Здесь будет интеграция с основным процессом поиска

    async def applications_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать последние отклики"""
        db = SessionLocal()
        try:
            applications = db.query(Application).order_by(
                Application.applied_at.desc()
            ).limit(10).all()

            if not applications:
                await update.message.reply_text("Откликов еще нет.")
                return

            text = "📨 *Последние 10 откликов:*\n\n"
            for app in applications:
                vacancy = db.query(Vacancy).filter(Vacancy.hh_id == app.hh_vacancy_id).first()
                company = vacancy.employer if vacancy else "Неизвестно"
                position = vacancy.name if vacancy else "Вакансия"

                status_emoji = {
                    "sent": "📤",
                    "viewed": "👁️",
                    "rejected": "❌",
                    "invited": "✅"
                }.get(app.status, "📝")

                text += f"{status_emoji} *{position}*\n"
                text += f"🏢 {company}\n"
                text += f"📅 {app.applied_at.strftime('%d.%m.%Y')}\n"
                text += f"Статус: {app.status}\n"
                if app.response_text:
                    text += f"Ответ: {app.response_text[:50]}...\n"
                text += "\n"

            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        finally:
            db.close()

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий кнопок"""
        query = update.callback_query
        await query.answer()

        # Обработка различных callback_data
        await query.edit_message_text(text=f"Выбрано: {query.data}")

    async def send_notification(self, message: str, parse_mode: Optional[str] = None):
        """Отправка уведомления в телеграм"""
        try:
            if not self.application:
                # Если бот не запущен, отправляем через прямое API
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                    data = {
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": parse_mode
                    }
                    async with session.post(url, json=data) as response:
                        if response.status != 200:
                            logger.error(f"Failed to send Telegram notification: {await response.text()}")
            else:
                await self.application.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode=parse_mode
                )

            logger.info(f"Telegram notification sent: {message[:50]}...")
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")

    async def notify_new_vacancy(self, vacancy: dict):
        """Уведомление о новой вакансии"""
        salary_text = ""
        if vacancy.get("salary_from") or vacancy.get("salary_to"):
            salary = f"{vacancy.get('salary_from', '')} - {vacancy.get('salary_to', '')} {vacancy.get('salary_currency', '')}"
            salary_text = f"\n💰 *Зарплата:* {salary}"

        message = f"""
🎯 *Новая вакансия найдена!*

*Должность:* {vacancy.get('name', '')}
*Компания:* {vacancy.get('employer', '')}
*Город:* {vacancy.get('area', '')}
{salary_text}
*Опыт:* {vacancy.get('experience', 'Не указан')}

[Ссылка на вакансию]({vacancy.get('url', '')})
        """

        # Создаем кнопки для быстрых действий
        keyboard = [
            [
                InlineKeyboardButton("📤 Откликнуться", callback_data=f"apply_{vacancy.get('hh_id')}"),
                InlineKeyboardButton("👎 Пропустить", callback_data=f"skip_{vacancy.get('hh_id')}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            if self.application:
                await self.application.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
        except Exception as e:
            logger.error(f"Error sending vacancy notification: {e}")
            await self.send_notification(f"Найдена новая вакансия: {vacancy.get('name', '')}")

    async def notify_application_sent(self, vacancy: dict, success: bool, error: Optional[str] = None):
        """Уведомление об отправке отклика"""
        if success:
            message = f"""
✅ *Отклик отправлен!*

*Вакансия:* {vacancy.get('name', '')}
*Компания:* {vacancy.get('employer', '')}
*Время:* {datetime.now().strftime('%H:%M %d.%m.%Y')}

[Ссылка на вакансию]({vacancy.get('url', '')})
            """
        else:
            message = f"""
❌ *Ошибка при отправке отклика*

*Вакансия:* {vacancy.get('name', '')}
*Ошибка:* {error or 'Неизвестная ошибка'}

[Ссылка на вакансию]({vacancy.get('url', '')})
            """

        await self.send_notification(message, parse_mode=ParseMode.MARKDOWN)

    async def notify_response_received(self, application: Application, response_text: str):
        """Уведомление о получении ответа"""
        db = SessionLocal()
        try:
            vacancy = db.query(Vacancy).filter(Vacancy.hh_id == application.hh_vacancy_id).first()

            message = f"""
📩 *Получен ответ на отклик!*

*Вакансия:* {vacancy.name if vacancy else 'Неизвестно'}
*Компания:* {vacancy.employer if vacancy else 'Неизвестно'}
*Время отклика:* {application.applied_at.strftime('%d.%m.%Y')}

*Ответ работодателя:*
{response_text[:500]}{'...' if len(response_text) > 500 else ''}
            """

            await self.send_notification(message, parse_mode=ParseMode.MARKDOWN)
        finally:
            db.close()


# Синглтон для доступа к нотификатору
telegram_notifier = TelegramNotifier()