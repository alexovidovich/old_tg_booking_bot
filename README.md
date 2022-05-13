# old_tg_booking_bot
- You can test it here https://t.me/testKLOP_bot  \
- Type 'admin_string' to become an admin(it's necessary for func)\
- It was written 2+ years ago for a small business in Belarus (timezone)(it's russian lan version, but you could edit texts for any language), \
- Now i'm just showing my progress then. fixed google auth(old token), 1-4 mistakes(telegram UI has changed).
- Code is too bad, I didn't use functions to build things I manually wrote, a structure is absent. The code could've been 3-5 times smaller.
- To make your own bot with the same functionality, make a post request to http://alexovidovich.pythonanywhere.com/ \
- With google_id,token,admin_key params:

                                       ("google_id" is calendar id from google calendar, \
                                       "token" is telegram bot token (BotFather for creation),\
                                       "admin_key" is a string to become admin)
- token.json isn't here (security measures)
- it's simple for young developers to build, \
- there's no any database, only json files, there're no async, no websockets, no msg broker, no docker. 
