<h1 align="center">
	  EMBED MAKER BOT
</h1>

A simple bot to make making embeds easier. When the bot is running you use the command `/embed` which will ask for advanced or simple method, after choosing the method
you can start with making the embed. At the end it will ask which channel it should send it to. 

`advanced method` - You can change the content, title, description, thumbnail, image, custom amount of fields (change field descriptions, inline), footer and color.

`simple` - You can change the title, description and color. This is if you want to create an embed quickly.

There is also the config. Make sure you add your id to the admins list otherwise you can't use the bot.

Example, how to add multiple admins:
```json
{
    "token": "PUT YOUR BOT TOKEN HERE",
    "guild-id": "PUT THE ID OF YOUR SERVER HERE",

    "admins": [
        123456789,
        1223523526789,
        12352352352359,
        1234234523589
    ],

    "default-embed-color": 16777215
}

```

default-embed-color is for the preview, you dont have to worry about that.

A picture of the bot being used (simple method): 

![image](https://github.com/Atluzka/embed-maker-bot/assets/52002842/57f075cb-c712-4cce-85e8-e35f563447ad)
