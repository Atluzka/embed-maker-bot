import discord, json
from discord import app_commands

bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
config = json.load(open('./bin/config.json'))

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=config["guild-id"]))
    print("Logged in as {0.user}".format(bot))

@tree.command(name = "embed", description = "Build an embed.", guild=discord.Object(id=config["guild-id"]))
async def generate(interaction: discord.Interaction):
    if not interaction.user.id in config['admins']:
        return await interaction.response.send_message(content='You do not have permission to use this command.', ephemeral=True) 
    
    await interaction.response.send_message(content="Choose a building style. ('advanced', 'simple' or 'cancel' to cancel building)")
    
    def check(msg):
        return msg.author.id == interaction.user.id and msg.channel == interaction.channel

    answer = await bot.wait_for('message', check=check)
    channel = interaction.channel
    userid = interaction.user.id
    if answer.content.lower() == 'simple':
        # simple building method

        await answer.delete()
        await interaction.edit_original_response(content='Simple building method chosen.')
        
        msg = await channel.send(f"<@{userid}>, what should be the title of your embed?")
        embed_title = await bot.wait_for('message', check=check)
        embed = discord.Embed(title=str(embed_title.content).replace('\\n', '\n'),description=str('Placeholder example').replace('\\n', '\n'),color=int(config['default-embed-color']))
        await interaction.edit_original_response(content='Preview:', embed=embed)
        
        await msg.delete()
        msg = await channel.send(f"<@{userid}>, what should be the description of your embed?")
        embed_description = await bot.wait_for('message', check=check)
        embed = discord.Embed(title=str(embed_title.content).replace('\\n', '\n'),description=str(embed_description.content).replace('\\n', '\n'),color=int(config['default-embed-color']))
        await interaction.edit_original_response(content='Preview:', embed=embed)

        await msg.delete()
        msg = await channel.send(f"<@{userid}>, what color should the embed be? (decimal value)")
        embed_color = await bot.wait_for('message', check=check)
        embed = discord.Embed(title=str(embed_title.content).replace('\\n', '\n'),description=str(embed_description.content).replace('\\n', '\n'),color=int(embed_color.content))
        await interaction.edit_original_response(content='Preview:', embed=embed)

        await msg.delete()
        msg = await channel.send(f"<@{userid}>, what channel should i send the embed to? (channel_id or tag)")
        embed_channel = await bot.wait_for('message', check=check)

        try:
            await msg.delete()
            embed = discord.Embed(title=str(embed_title.content).replace('\\n', '\n'),description=str(embed_description.content).replace('\\n', '\n'),color=int(embed_color.content))

            embed_channel_id = embed_channel.content
            for char in '<#>':
                embed_channel_id = embed_channel_id.replace(char, '')

            await embed_title.delete(); await embed_description.delete(); await embed_color.delete(); await embed_channel.delete()
            await interaction.delete_original_response()
            channel = discord.utils.get(interaction.guild.channels, id=int(embed_channel_id))
            await channel.send(embed=embed)
        except Exception as e:
            await msg.delete()
            await embed_title.delete(); await embed_description.delete(); await embed_color.delete(); await embed_channel.delete()
            return await interaction.edit_original_response(content=f'```rust\nThere was an error with building an embed\n\n{e}```')

        return
    elif answer.content.lower() == 'advanced':
        # advanced building method
        try:  
            await answer.delete()
            await interaction.edit_original_response(content='Advanced building method chosen.')
            
            # embed init
            embed = discord.Embed(title=str('Example').replace('\\n', '\n'),description=str('Preview embed').replace('\\n', '\n'),color=int(config['default-embed-color']))
            
            # content for the embed build
            msg = await channel.send(f"<@{userid}>, what should be the content of your embed? ('none' for no content)")
            embed_content = await bot.wait_for('message', check=check)
            embed_content_msg = embed_content.content if not embed_content.content.lower() == 'none' else ''
            await embed_content.delete()
            await interaction.edit_original_response(content=str(embed_content_msg).replace('\\n', '\n'), embed=embed)
            
            # title of the embed
            await msg.delete()
            msg = await channel.send(f"<@{userid}>, what should be the title of your embed? ('none' for no title)")
            embed_title = await bot.wait_for('message', check=check)
            embed_title_msg = embed_title.content if not embed_title.content.lower() == 'none' else ''
            await embed_title.delete()
            embed.title=str(embed_title_msg).replace('\\n', '\n')
            if not embed_title.content.lower() == 'none':
                await interaction.edit_original_response(embed=embed)

            # description of the embed
            await msg.delete()
            msg = await channel.send(f"<@{userid}>, what should be the description of your embed? ('none' for no description)")
            embed_description = await bot.wait_for('message', check=check)
            embed_description_msg = embed_description.content if not embed_description.content.lower() == 'none' else ''
            await embed_description.delete()
            embed.description=str(embed_description_msg).replace('\\n', '\n')
            if not embed_description.content.lower() == 'none':
                await interaction.edit_original_response(embed=embed)
            
            # thumbnail url
            await msg.delete()
            msg = await channel.send(f"<@{userid}>, what should be the thumbnail of your embed? ('none' for no thumbnail)")
            embed_thumbnail = await bot.wait_for('message', check=check)
            embed_thumbnail_msg = embed_thumbnail.content if not embed_thumbnail.content == 'none' else ''
            await embed_thumbnail.delete()
            if not embed_thumbnail.content.lower() == 'none': 
                embed.set_thumbnail(url=str(embed_thumbnail_msg))
                await interaction.edit_original_response(embed=embed)
            
            # image url
            await msg.delete()
            msg = await channel.send(f"<@{userid}>, what should be the image of your embed? ('none' for no image)")
            embed_image = await bot.wait_for('message', check=check)
            embed_image_msg = embed_image.content if not embed_image.content.lower() == 'none' else ''
            await embed_image.delete()
            if not embed_thumbnail.content.lower() == 'none': 
                embed.set_image(url=str(embed_image_msg))
                await interaction.edit_original_response(embed=embed)
            
            # fields
            await msg.delete()
            msg = await channel.send(f"<@{userid}>, how many fields would you like your embed to have? ('0' for no fields, maximum is 25)")
            field_amount = await bot.wait_for('message', check=check)
            if int(field_amount.content) >= 1:
                await msg.delete()
                for i in range(int(field_amount.content)):
                    await msg.delete()
                    msg = await channel.send(f"<@{userid}>, what should be the name of your number {i+1} field?")
                    field_name = await bot.wait_for('message', check=check)
                    await msg.delete()
                    msg = await channel.send(f"<@{userid}>, what should be the description of your {i+1}th field?")
                    field_value = await bot.wait_for('message', check=check)
                    await msg.delete()
                    msg = await channel.send(f"<@{userid}>, should your {i+1}th field be inline? (true/false)")
                    field_inline = await bot.wait_for('message', check=check)
                    field_inline_msg = True if field_inline.content.lower() == 'true' else False
                    embed.add_field(name=str(field_name.content),value=str(field_value.content),inline=field_inline_msg)
                    await field_name.delete(); await field_value.delete(); await field_inline.delete()
                await field_amount.delete()
                await interaction.edit_original_response(embed=embed)
            else:
                await msg.delete()
                await field_amount.delete()
            
            # footer
            msg = await channel.send(f"<@{userid}>, what should be the footer of your embed? ('none' for no footer)")
            embed_footer = await bot.wait_for('message', check=check)

            await msg.delete()
            msg = await channel.send(f"<@{userid}>, what should be the icon_url of your footer? ('none' for no footer_icon)")
            embed_footer_icon = await bot.wait_for('message', check=check)

            embed_footer_msg = embed_footer.content if not embed_footer.content.lower() == 'none' else ''
            embed_footer_icon_msg = embed_footer_icon.content if not embed_footer_icon.content.lower() == 'none' else ''
            await embed_footer.delete(); await embed_footer_icon.delete()
            if not embed_thumbnail.content.lower() == 'none': 
                embed.set_footer(text=str(embed_footer_msg), icon_url=str(embed_footer_icon_msg))
                await interaction.edit_original_response(embed=embed)
            
            # embed color
            await msg.delete()
            msg = await channel.send(f"<@{userid}>, what color should the embed be in decimals? ('none' for default color)")
            embed_color = await bot.wait_for('message', check=check)
            embed_color_msg = embed_color.content if not embed_color.content.lower() == 'none' else int(config['default-embed-color'])
            if not embed_color.content.lower() == 'none':
                embed.color=int(embed_color_msg)
                await interaction.edit_original_response(embed=embed)
            
            # channel to send it to
            await msg.delete()
            msg = await channel.send(f"<@{userid}>, what channel should i send the embed to? ('none' for current channel)")
            embed_channel = await bot.wait_for('message', check=check)
            embed_chan = embed_channel.content
            for char in '<#>':
                    embed_chan = (embed_chan).replace(char, '')
            embed_channel_id = str(interaction.channel.id) if embed_channel.content.lower() == 'none' else embed_chan
            await msg.delete()
        except Exception as e:
            await interaction.edit_original_response(content=f'```rust\nThere was an error, please run /embed again to build.\n\n{e}```', embed=None)
        try:
            await interaction.delete_original_response()
            channel = discord.utils.get(interaction.guild.channels, id=int(embed_channel_id))
            await channel.send(embed=embed)
        except Exception as e:
            await interaction.edit_original_response(content=f"```rust\nThere was an error while trying to send the embed\nERROR:\n{e}```")
    elif answer.content == 'cancel':
        return await interaction.edit_original_response(content=f'Building has been canceled.')
    else:
        return await interaction.edit_original_response(content=f'Invalid response.')
    
bot.run(config['token'])
