from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from web_scrape import get_results
from datetime import datetime



#bot name: GetThisJobBot, @get_this_job_bot

updater = Updater("BOT_TOKEN",
	use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
	"Hello. Type /search {job title} without curly braces\nFor instance, /search frontend intern\nType /help for more info.")
def _help(update: Update, context: CallbackContext):
	update.message.reply_text("Type /search {job title} to search for LinkedIn job postings\nFor example, /search data science intern\nYou can add a results parameter to change the number of results; Maximum is 10\n/search data science intern results 6\nYou can try searching again if I don't return results")

def search(update: Update, context: CallbackContext):
	params = update.message.text.split()[1:]
	if 'results' in params:
		r_ind = params.index('results')
		num_results = int(params[r_ind + 1])
		query = params[:r_ind]
		query = ' '.join(query)
	else:
		query = ' '.join(params)
		num_results = 5
	print("Received query:",query)
	ret_val = get_results(query,num_results)

	if '{' in query or '}' in query:
		update.message.reply_text("Preferably leave out the curly braces.\nFor instance, /search freshman internship")
	update.message.reply_text(ret_val,parse_mode="HTML")
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Processed query: %s" % query, current_time)
	print()

def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
	"Sorry I don't understand you. You said '%s'" % update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('search', search))
updater.dispatcher.add_handler(CommandHandler('help', _help))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
updater.dispatcher.add_handler(MessageHandler(
	# Filters out unknown commands
	Filters.command, unknown_text))

updater.start_polling()
