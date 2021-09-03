
# CanvasAutoSubscriber
CanvasAutoSubscriber is a Python program to automatically check the groups on Canvas and subscribe to open groups. This program is used by me to secure an place in the right lessons for my study Econometrics at Tilburg University.

At the moment of writing, the Dutch government limits the number of students during colleges to 75. As the study has 185 students, you have to subscribe to the lectures to get an seat. This program ensures that I will have a seat for my selected lectures (In my cases selected by ID and the right expected title of the group, the English ones as that is the better one qua timing.)

For this program I made use of the available [API of Canvas](https://canvas.instructure.com/doc/api/). To try this program yourself you have to change the token (log in to Canvas, go to your profile, settings and generate an access token). Replace the ID’s with the course ID’s of your own courses and change the if-statements to suit your preferences.

## Telegram bot
If the program signs you up, you want to get updated. The python script has an function build in to inform you about the new sign ups. To enable this you have to make an telgeram bot and get an token en your chat_id. It's based on [this StackOverflow anwser](https://stackoverflow.com/questions/29003305/sending-telegram-message-from-python).
