from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from web_scrape import get_results



#bot name: LinkedInJobBot, @get_this_job_bot

updater = Updater("BOT_TOKEN",
	use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
	"Hello. Type /search {job title}")
def _help(update: Update, context: CallbackContext):
	update.message.reply_text("Type /search {job title} to search for LinkedIn job postings\nFor example, /search data science intern\nYou can add a results parameter to change the number of results; Maximum is 10\n/search data science intern results 6")

def search(update: Update, context: CallbackContext):
	params = update.message.text.split()[1:]
	if 'results' in params:
		r_ind = params.index('results')
		num_results = r_ind + 1
		query = params[:r_ind]
		query = ' '.join(query)
	else:
		query = ' '.join(params)
		num_results = 5
	ret_val = get_results(query,num_results)

	update.message.reply_text(ret_val,parse_mode="HTML")
	print("Processed query: %s" % query)

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
