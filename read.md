"expiry": "2024-04-30T17:38:03.603418Z"

That's the expiration of the oauth2 token, used
to log and use the google drive api.

I would say it only lasts 24 hours.

Once it expires, the code won't work
until a new one is created.

To create one, delete the current token.json.
And run the program again, a chrome window will
pop up requiring permision on drogon's account.