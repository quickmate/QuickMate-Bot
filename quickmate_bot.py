# ---------------- QuickMate Final Fixed Code ----------------

from keep_alive import keep_alive

import logging
import requests
import datetime
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from deep_translator import GoogleTranslator

# ---------- CONFIG ----------
BOT_TOKEN = '8059468951:AAG2woZiKh05JK10tOtLac0tylsJFie5dMw'
WEATHER_API = '40222fb44bb4fffeafa1acae2a7bb798'

# ---------- LOGGING ----------
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ---------- DATA ----------
quotes = [
"💬 The best way to get started is to quit talking and begin doing.",
"💬 Don’t let yesterday take up too much of today.",
"💬 It’s not whether you get knocked down, it’s whether you get up.",
"💬 If you are working on something exciting, it will keep you motivated.",
"💬 Success is not in what you have, but who you are.",
"💬 The harder you work for something, the greater you’ll feel when you achieve it.",
"💬 Dream bigger. Do bigger.",
"💬 Don’t watch the clock; do what it does. Keep going.",
"💬 Great things never come from comfort zones.",
"💬 Push yourself, because no one else is going to do it for you.",
"💬 Success doesn’t just find you. You have to go out and get it.",
"💬 The key to success is to focus on goals, not obstacles.",
"💬 Believe you can and you’re halfway there.",
"💬 Your limitation—it’s only your imagination.",
"💬 Sometimes later becomes never. Do it now.",
"💬 Wake up with determination. Go to bed with satisfaction.",
"💬 Do something today that your future self will thank you for.",
"💬 Little things make big days.",
"💬 It’s going to be hard, but hard does not mean impossible.",
"💬 Don’t wait for opportunity. Create it.",
"💬 Be stronger than your excuses.",
"💬 You don’t have to be great to start, but you have to start to be great.",
"💬 The only limit to our realization of tomorrow is our doubts of today.",
"💬 The future depends on what you do today.",
"💬 It always seems impossible until it’s done.",
"💬 Start where you are. Use what you have. Do what you can.",
"💬 Believe in yourself and all that you are.",
"💬 Your only limit is you.",
"💬 Everything you’ve ever wanted is on the other side of fear.",
"💬 Difficult roads often lead to beautiful destinations.",
"💬 Don’t stop when you’re tired. Stop when you’re done.",
"💬 Success is what happens after you have survived all your mistakes.",
"💬 The secret of getting ahead is getting started.",
"💬 The best revenge is massive success.",
"💬 I never dream of success. I worked for it.",
"💬 Stay positive. Work hard. Make it happen.",
"💬 You are capable of amazing things.",
"💬 Don’t limit your challenges. Challenge your limits.",
"💬 Make each day your masterpiece.",
"💬 Focus on being productive instead of being busy.",
"💬 Don’t be afraid to give up the good to go for the great.",
"💬 If it doesn’t challenge you, it won’t change you.",
"💬 The only way to do great work is to love what you do.",
"💬 Work hard in silence, let your success be the noise.",
"💬 Don’t raise your voice, improve your argument.",
"💬 You don’t find the happy life. You make it.",
"💬 Life is short. Live it. Fear is natural. Face it. Memory is powerful. Use it.",
"💬 Happiness is not by chance, but by choice.",
"💬 Positive anything is better than negative nothing."
]
jokes = [
"😂 Why don’t scientists trust atoms? Because they make up everything!",
"😂 I told my wife she was drawing her eyebrows too high. She looked surprised.",
"😂 Why did the scarecrow win an award? Because he was outstanding in his field.",
"😂 Parallel lines have so much in common. It’s a shame they’ll never meet.",
"😂 I would tell you a joke about construction, but I’m still working on it.",
"😂 Why don’t programmers like nature? Too many bugs.",
"😂 I used to play piano by ear, but now I use my hands.",
"😂 Why did the math book look sad? Because it had too many problems.",
"😂 I told my computer I needed a break, and now it won’t stop sending me KitKat ads.",
"😂 How do cows stay up to date? They read the moos-paper.",
"😂 Why did the bicycle fall over? Because it was two-tired.",
"😂 I asked my dog what’s two minus two. He said nothing.",
"😂 I’m reading a book on anti-gravity. It’s impossible to put down!",
"😂 I told my friend 10 jokes to make him laugh. Sadly, no pun in ten did.",
"😂 I’m on a whiskey diet. I’ve lost three days already.",
"😂 Did you hear about the restaurant on the moon? Great food, no atmosphere.",
"😂 Why can’t you hear a pterodactyl go to the bathroom? Because the ‘P’ is silent.",
"😂 I’m afraid for the calendar. Its days are numbered.",
"😂 What’s orange and sounds like a parrot? A carrot!",
"😂 Why did the coffee file a police report? It got mugged.",
"😂 I ate a clock yesterday, it was very time consuming.",
"😂 Why don’t oysters donate to charity? Because they are shellfish.",
"😂 What do you call fake spaghetti? An impasta.",
"😂 What did the janitor say when he jumped out of the closet? Supplies!",
"😂 Why did the golfer bring two pairs of pants? In case he got a hole in one.",
"😂 Why don’t skeletons fight each other? They don’t have the guts.",
"😂 Why did the cookie go to the doctor? Because he was feeling crumby.",
"😂 What do you call cheese that isn’t yours? Nacho cheese.",
"😂 I only know 25 letters of the alphabet. I don’t know y.",
"😂 How does a penguin build its house? Igloos it together.",
"😂 What’s brown and sticky? A stick.",
"😂 Why do chicken coops only have two doors? Because if they had four, they’d be chicken sedans.",
"😂 Why did the man get hit by a bike every day? He was stuck in a vicious cycle.",
"😂 What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.",
"😂 Why do cows wear bells? Because their horns don’t work.",
"😂 What did one wall say to the other? I’ll meet you at the corner.",
"😂 Why did the tomato blush? Because it saw the salad dressing.",
"😂 What happens when frogs park illegally? They get toad.",
"😂 How do you organize a space party? You planet.",
"😂 What did the grape do when it got stepped on? Nothing, it just let out a little wine.",
"😂 Why did the student eat his homework? Because the teacher told him it was a piece of cake.",
"😂 Why don’t some couples go to the gym? Because some relationships don’t work out.",
"😂 What lights up a soccer stadium? A soccer match.",
"😂 What do you call an alligator in a vest? An investigator.",
"😂 Did you hear about the kidnapping at school? It’s fine, he woke up.",
"😂 Why did the barber win the race? He knew all the shortcuts.",
"😂 Want to hear a joke about paper? Never mind, it’s tearable.",
"😂 How does a scientist freshen her breath? With experi-mints."
]
facts = [
    {"q": "❓ Honey never spoils.", "a": "Archaeologists have eaten 3000-year-old honey and it was perfectly edible."},
    {"q": "❓ Bananas are berries but strawberries are not.", "a": "Botanically, bananas fit the berry classification, strawberries do not."},
    {"q": "❓ The Eiffel Tower can be taller in summer.", "a": "Due to heat expansion, it can grow by up to 15 cm."},
    {"q": "❓ Octopuses have three hearts.", "a": "Two pump blood to the gills, one to the body."},
    {"q": "❓ Sloths can hold their breath longer than dolphins.", "a": "Up to 40 minutes by slowing their heart rate."},
    {"q": "❓ A snail can sleep for three years.", "a": "This helps them survive long periods without food."},
    {"q": "❓ Wombat poop is cube-shaped.", "a": "To stop it rolling away and mark territory effectively."},
    {"q": "❓ Butterflies can taste with their feet.", "a": "They have taste sensors on their feet to find food."},
    {"q": "❓ Sea otters hold hands while sleeping.", "a": "To keep from drifting apart in water."},
    {"q": "❓ Tigers have striped skin.", "a": "Their skin stripes match their fur pattern."},
    {"q": "❓ Koalas have fingerprints.", "a": "They are almost identical to human fingerprints."},
    {"q": "❓ The unicorn is Scotland’s national animal.", "a": "It symbolises purity and innocence in Celtic mythology."},
    {"q": "❓ A group of crows is called a murder.", "a": "The term dates back to 15th century England."},
    {"q": "❓ Humans and giraffes have the same neck vertebrae count.", "a": "Both have seven, giraffe vertebrae are just longer."},
    {"q": "❓ Mosquitoes are the deadliest animals.", "a": "They spread diseases killing millions every year."},
    {"q": "❓ You can't hum holding your nose closed.", "a": "Humming requires air passage through your nose."},
    {"q": "❓ Peanuts are legumes.", "a": "They belong to the bean family, not nuts."},
    {"q": "❓ Ostrich’s eye is bigger than its brain.", "a": "Their eyes are about 5 cm across, bigger than their brain."},
    {"q": "❓ Blue whales are the largest animals ever.", "a": "They can weigh up to 200 tons and are longer than basketball courts."},
    {"q": "❓ Avocados are berries.", "a": "Botanically, they fit all the berry criteria."},
    {"q": "❓ The inventor of Pringles is buried in one.", "a": "Fred Baur had his ashes in a Pringles can."},
    {"q": "❓ Coca-Cola was the first soft drink in space.", "a": "Astronauts tested it aboard Space Shuttle Challenger in 1985."},
    {"q": "❓ Kangaroos can't walk backwards.", "a": "Their bulky tail and body make it impossible."},
    {"q": "❓ Humans are the only animals that blush.", "a": "Blushing is unique to human social behaviour."},
    {"q": "❓ Crocodiles can't stick their tongue out.", "a": "Their tongue is held in place by a membrane."},
    {"q": "❓ It is impossible to sneeze with your eyes open.", "a": "Your body reflexively shuts your eyes while sneezing."},
    {"q": "❓ Some lipsticks contain fish scales.", "a": "They add shimmer and shine to the product."},
    {"q": "❓ Rats laugh when tickled.", "a": "They emit high-frequency chirps humans can't hear."},
    {"q": "❓ Hot water freezes faster than cold water.", "a": "This is called the Mpemba effect."},
    {"q": "❓ Chewing gum boosts concentration.", "a": "Studies show it improves memory and attention."},
    {"q": "❓ London Bridge is in Arizona.", "a": "It was relocated from England to Lake Havasu City in 1968."},
    {"q": "❓ Tomatoes have more genes than humans.", "a": "They have around 31,760 genes, humans have ~25,000."},
    {"q": "❓ Pineapples take two years to grow.", "a": "They require 18-24 months from planting to harvest."},
    {"q": "❓ Butterflies were originally called flutterbys.", "a": "Over time the words flipped into 'butterfly'."},
    {"q": "❓ Hummingbirds can't walk.", "a": "They can only perch and fly, their legs are too weak for walking."},
    {"q": "❓ Elephants can't jump.", "a": "Their weight and leg structure prevent it completely."},
    {"q": "❓ The moon has moonquakes.", "a": "They are similar to earthquakes but less intense."},
    {"q": "❓ The smell of fresh-cut grass is distress signal.", "a": "It's a chemical plants release when damaged."},
    {"q": "❓ Bananas glow blue under UV light.", "a": "Due to degradation products of chlorophyll."},
    {"q": "❓ Flamingos are naturally white.", "a": "Their pink comes from carotenoid pigments in their food."},
    {"q": "❓ Cows have best friends.", "a": "They become stressed when separated from them."},
    {"q": "❓ Giraffes have no vocal cords.", "a": "They communicate through low-frequency sounds below human hearing."},
    {"q": "❓ Hippo sweat is pink.", "a": "It acts as natural sunscreen and antibiotic."},
    {"q": "❓ Reindeer eyes change colour with seasons.", "a": "From gold in summer to blue in winter for better vision."},
    {"q": "❓ Pigs can't look up into the sky.", "a": "Their neck muscles and spine make it impossible."},
    {"q": "❓ Dolphins have names for each other.", "a": "They develop signature whistles to identify individuals."},
    {"q": "❓ Earthquakes turn water into gold.", "a": "Minerals can precipitate during seismic activity forming veins."},
    {"q": "❓ Some turtles can breathe through their butts.", "a": "Called cloacal respiration, useful during hibernation."}
]
quizzes = [
    {"q": "❓ What is the capital of France?", "a": "Paris"},
    {"q": "❓ Who wrote 'Romeo and Juliet'?", "a": "William Shakespeare"},
    {"q": "❓ What is the largest planet?", "a": "Jupiter"},
    {"q": "❓ Who discovered gravity?", "a": "Isaac Newton"},
    {"q": "❓ What is H2O commonly known as?", "a": "Water"},
    {"q": "❓ Who painted the Mona Lisa?", "a": "Leonardo da Vinci"},
    {"q": "❓ What is the fastest land animal?", "a": "Cheetah"},
    {"q": "❓ Which country is called the Land of the Rising Sun?", "a": "Japan"},
    {"q": "❓ What is the boiling point of water?", "a": "100°C"},
    {"q": "❓ Who was the first man on the moon?", "a": "Neil Armstrong"},
    {"q": "❓ What is the longest river?", "a": "Nile"},
    {"q": "❓ Who invented the telephone?", "a": "Alexander Graham Bell"},
    {"q": "❓ What is the hardest natural substance?", "a": "Diamond"},
    {"q": "❓ Which gas do plants absorb?", "a": "Carbon Dioxide"},
    {"q": "❓ Who wrote 'Harry Potter'?", "a": "J.K. Rowling"},
    {"q": "❓ What is the tallest mountain?", "a": "Mount Everest"},
    {"q": "❓ What is the currency of Japan?", "a": "Yen"},
    {"q": "❓ How many continents are there?", "a": "Seven"},
    {"q": "❓ What is the main language spoken in Brazil?", "a": "Portuguese"},
    {"q": "❓ Which ocean is the largest?", "a": "Pacific Ocean"},
    {"q": "❓ What is the powerhouse of the cell?", "a": "Mitochondria"},
    {"q": "❓ Who discovered America?", "a": "Christopher Columbus"},
    {"q": "❓ What is the smallest prime number?", "a": "2"},
    {"q": "❓ Which animal is known as the King of the Jungle?", "a": "Lion"},
    {"q": "❓ What does ATM stand for?", "a": "Automated Teller Machine"},
    {"q": "❓ What is the square root of 64?", "a": "8"},
    {"q": "❓ Who invented the light bulb?", "a": "Thomas Edison"},
    {"q": "❓ What is the largest mammal?", "a": "Blue Whale"},
    {"q": "❓ Which planet is known as the Red Planet?", "a": "Mars"},
    {"q": "❓ Who was the first President of the USA?", "a": "George Washington"},
    {"q": "❓ What is the freezing point of water?", "a": "0°C"},
    {"q": "❓ Which organ purifies blood?", "a": "Kidney"},
    {"q": "❓ Who wrote 'The Odyssey'?", "a": "Homer"},
    {"q": "❓ What is the capital of Italy?", "a": "Rome"},
    {"q": "❓ How many teeth do adults have?", "a": "32"},
    {"q": "❓ What is the chemical symbol for gold?", "a": "Au"},
    {"q": "❓ Which planet has rings?", "a": "Saturn"},
    {"q": "❓ What is the largest island?", "a": "Greenland"},
    {"q": "❓ Who painted the Sistine Chapel ceiling?", "a": "Michelangelo"},
    {"q": "❓ What is 5 squared?", "a": "25"},
    {"q": "❓ What is the capital of China?", "a": "Beijing"},
    {"q": "❓ Which insect produces honey?", "a": "Bee"},
    {"q": "❓ Who was Albert Einstein?", "a": "Physicist"},
    {"q": "❓ What is the tallest building in the world?", "a": "Burj Khalifa"},
    {"q": "❓ Which country gifted the Statue of Liberty to the USA?", "a": "France"},
    {"q": "❓ What is the largest desert?", "a": "Sahara"},
    {"q": "❓ What is the symbol for sodium?", "a": "Na"},
    {"q": "❓ Which organ pumps blood?", "a": "Heart"},
    {"q": "❓ Who is known as the Father of Computers?", "a": "Charles Babbage"}
]

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📌 Pin Code Finder", callback_data='pincode')],
        [InlineKeyboardButton("🌐 Translator", callback_data='translator')],
        [InlineKeyboardButton("⁉️ GK Quizzes", callback_data='quiz')],
        [InlineKeyboardButton("😂 Jokes", callback_data='joke')],
        [InlineKeyboardButton("💬 Quotes", callback_data='quote')],
        [InlineKeyboardButton("🕑 Time/Date", callback_data='time')],
        [InlineKeyboardButton("💡 Facts", callback_data='fact')],
        [InlineKeyboardButton("⛈️ Weather Info", callback_data='weather')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hey! I’m QuickMate, Your Personal Multi-Utility Assistant.", reply_markup=reply_markup)
    context.user_data['state'] = None

# ---------- PINCODE ----------
async def pincode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Send Pin Code to find details.")
    context.user_data['state'] = 'pincode'

async def handle_pincode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pincode = update.message.text
    res = requests.get(f"https://api.postalpincode.in/pincode/{pincode}").json()
    if res[0]['Status'] == 'Success':
        data = res[0]['PostOffice'][0]
        await update.message.reply_text(f"✅ Post Office: {data['Name']}\n✅ District: {data['District']}\n✅ State: {data['State']}")
    else:
        await update.message.reply_text("❌ Invalid Pin Code.")

# ---------- TRANSLATOR ----------
async def translator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("📝 Please send me the text you want to translate to English.")
    context.user_data['state'] = 'translator'

async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        await update.message.reply_text(f"🔤 Translated:\n{translated_text}")
    except Exception as e:
        print(f"Translation error: {e}")
        await update.message.reply_text("❌ Translation server unavailable right now.")

# ---------- WEATHER ----------
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Send city name to get weather info.")
    context.user_data['state'] = 'weather'

async def handle_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"
    res = requests.get(url).json()
    if res.get('cod') != 200:
        await update.message.reply_text("❌ City not found.")
    else:
        rain = res['clouds']['all']
        await update.message.reply_text(
            f"🌤️ Weather in {city}:\nTemperature: {res['main']['temp']}°C\nHumidity: {res['main']['humidity']}%\nRain (Today): {rain}%"
        )

# ---------- TIME ----------
async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)
    await update.callback_query.message.reply_text(
        f"⏰ Time : {now.strftime('%I:%M %p')}\n📅 Date : {now.strftime('%d %B %Y')}"
    )

# ---------- QUOTE ----------
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i = context.user_data.get('quote_index', 0)
    await update.callback_query.message.reply_text(quotes[i], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Next", callback_data='quote_next')]]))
    context.user_data['quote_index'] = (i + 1) % len(quotes)

# ---------- JOKE ----------
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i = context.user_data.get('joke_index', 0)
    await update.callback_query.message.reply_text(jokes[i], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Next", callback_data='joke_next')]]))
    context.user_data['joke_index'] = (i + 1) % len(jokes)

# ---------- QUIZ ----------
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    i = context.user_data.get('quiz_index', 0)
    if i >= len(quizzes):
        i = 0
    q = quizzes[i]

    keyboard = [
        [InlineKeyboardButton("Answer", callback_data=f"quiz_ans_{i}")],
        [InlineKeyboardButton("Next Quiz", callback_data="quiz_next")]
    ]

    await query.message.reply_text(q['q'], reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data['quiz_index'] = i + 1

async def quiz_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data.split("_")[-1])
    a = quizzes[index]['a']
    await query.message.reply_text(f"✅ Answer: {a}")

# ---------- FACT ----------
async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    i = context.user_data.get('fact_index', 0)
    if i >= len(facts):
        i = 0
    q = facts[i]

    keyboard = [
        [InlineKeyboardButton("Answer", callback_data=f"fact_ans_{i}")],
        [InlineKeyboardButton("Next Fact", callback_data="fact_next")]
    ]

    await query.message.reply_text(q['q'], reply_markup=InlineKeyboardMarkup(keyboard))
    context.user_data['fact_index'] = i + 1

async def fact_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data.split("_")[-1])
    a = facts[index]['a']
    await query.message.reply_text(f"💡 {a}")

# ---------- CALLBACK HANDLER ----------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'pincode':
        await pincode(update, context)
    elif data == 'translator':
        await translator(update, context)
    elif data == 'weather':
        await weather(update, context)
    elif data == 'time':
        await time(update, context)
    elif data == 'quote':
        await quote(update, context)
    elif data == 'quote_next':
        await quote(update, context)
    elif data == 'joke':
        await joke(update, context)
    elif data == 'joke_next':
        await joke(update, context)
    elif data == 'fact':
        await fact(update, context)
    elif data.startswith('fact_ans_'):
        await fact_ans(update, context)
    elif data == 'fact_next':
        await fact(update, context)
    elif data == 'quiz':
        await quiz(update, context)
    elif data.startswith('quiz_ans_'):
        await quiz_ans(update, context)
    elif data == 'quiz_next':
        await quiz(update, context)

# ---------- MESSAGE HANDLER ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get('state')
    if state == 'pincode':
        await handle_pincode(update, context)
    elif state == 'translator':
        await handle_translation(update, context)
    elif state == 'weather':
        await handle_weather(update, context)

# ---------- MAIN ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


keep_alive()


print("🤖 Bot is running...")
app.run_polling()
