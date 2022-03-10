# from pydoc import cli
# from email.policy import default
import discord
from discord.commands import Option

import os
from dotenv import load_dotenv
from NHentai import NHentai
# from help import help

helpList={
    "info":"Enter id of a doujin to get brief information about it. \n eg. `nh!info 117013`",
    "cover":"Enter id of a doujin to get it's cover image. \n eg. `nh!cover 117013` ",
    "random":"Get information about a random doujin.",
    "search":"Seach the nhentai database using using a term followed by number of results you want. \n eg. `nh!search naruto 5` \n Note: Search queries with more than 10 doujins may take few extra seconds to process",
    "pop":"Get trending doujins in the current time."
}

slMessage="**Try using the all new Slash commands!**\n For more information, use `nh!help`.\n"
warning="⚠️ **Regular commands are being replaced in favour of slash commands.** \n From Friday, 1 April 2022 regular commands will no longer work and the bot will only respond to slash commands.\nTry typing / to see a list of available commands.\n\nIf you can't see the slash commands, try re-inviting the bot using the following link.\nhttps://discord.com/api/oauth2/authorize?client_id=925763248857419847&permissions=534723950656&scope=bot%20applications.commands"

load_dotenv()
client = discord.Bot()
nhentai = NHentai()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Game(name="nh!help")
    await client.change_presence(activity=activity)

async def handleNsfw(x):
    embed=discord.Embed(
        type='gifv',
        title='Please use a nsfw channel :)',
        #video='https://i.imgur.com/7HtvXdb.gif'        
    )
    embed.set_image(url='https://i.imgur.com/7HtvXdb.gif')
    await x.send(embed=embed)
async def handleSlashNsfw(ctx):
    embed=discord.Embed(
        type='gifv',
        title='Please use a nsfw channel :)',
        #video='https://i.imgur.com/7HtvXdb.gif'        
    )
    embed.set_image(url='https://i.imgur.com/7HtvXdb.gif')
    await ctx.respond(embed=embed)


#Slash cover
@client.slash_command(guild_ids=[843878576981147648], description="Get the cover of the entered doujin.")
async def cover(ctx:discord.ApplicationContext, id:Option(int,"Enter the doujin code")):
    if not (ctx.channel.is_nsfw()):
                await handleSlashNsfw(ctx)
                return
    code=id
    doujin=nhentai.get_doujin(id=code)
    if doujin!= None:
        embed=discord.Embed(
           title=doujin.title.english,
           type='image',   
           color=0xEC2854             
           )            
        embed.set_image(url=doujin.cover.src)
        # embed.set_author(name=ctx.author.display_name , url="", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("Invalid Code")

#Slash info
@client.slash_command(guild_ids=[843878576981147648], description="Get useful information about the desired doujin.")
async def info(ctx:discord.ApplicationContext, id:Option(int,"Enter the doujin code")):
    if not (ctx.channel.is_nsfw()):
        await handleSlashNsfw(ctx)
        return
    # try:
    #     code=ctx[1]
    # except IndexError:
    #     await ctx.respond('Please enter an id')
    #     return
    doujin=nhentai.get_doujin(id=id)
    if doujin!= None:
        embed=discord.Embed(
            title=doujin.title.english,
            type='rich',                
            url=doujin.url,
            color=0xEC2854
            )
        tags=''
        for i in range(5):
            tags+=doujin.tags[i].name
            if i != 4:
                tags+=", "
        embed.add_field(name="Tags", value=tags, inline=False)
        embed.add_field(name="Id", value=doujin.id, inline=True)
        embed.add_field(name="Artists", value=doujin.artists[0].name if len(doujin.artists)!=0 else "-", inline=True)
        embed.add_field(name="Total Pages", value=doujin.total_pages, inline=True)
        embed.add_field(name="Favourites", value=doujin.total_favorites, inline=True)
        embed.add_field(name="Languages", value=doujin.languages[0].name, inline=True)
        embed.add_field(name="Groups", value=doujin.groups[0].name if len(doujin.groups)!=0 else "-", inline=True)
        # embed.set_author(name=ctx.author.display_name , url="", icon_url=ctx.author.avatar)
        embed.set_image(url=doujin.cover.src)
        embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
        await ctx.respond(embed=embed)            
    else:
        await ctx.respond("Invalid Code")

#Slash search
@client.slash_command(guild_ids=[843878576981147648],description="Search using a tag.")
async def search(
    ctx:discord.ApplicationContext, 
    query:Option(str,"Enter the query"),
    num:Option(int, "Enter number of results you want.", default=10)
    ):
    if not (ctx.channel.is_nsfw()):
        await handleSlashNsfw(ctx)
        return

    query=query
    num=num
    await ctx.defer()
    results=nhentai.search(query=query, sort=None, page=1).total_results
    # try:
    # except:
    #     await ctx.respond('Please enter the correct format. \nUse `nh!help` for further information')
    #     return
        
    # wait = await ctx.respond('Please wait...')
    embed=discord.Embed(
        title=query,
        color=0xEC2854
    )
    #print (results)
    if results==0:
        await ctx.respond('Sorry we could not find something for the entered query.')

    elif int(num)>20:
        await ctx.respond("Please keep the count below 20 :)")
    
    elif results<int(num):
        for i in range(results):
            name=nhentai.search(query=query, sort=None, page=1).doujins[i].title.english
            url=nhentai.search(query=query, sort=None, page=1).doujins[i].url
            embed.add_field(name=name, value=url, inline=False)
        # embed.set_author(name=ctx.author.display_name , url="", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
        await ctx.respond(embed=embed)

    else:
        try:
            for i in range(int(num)):
                name=nhentai.search(query=query, sort=None, page=1).doujins[i].title.english
                url=nhentai.search(query=query, sort=None, page=1).doujins[i].url
                embed.add_field(name=name, value=url, inline=False)
            # embed.set_author(name=ctx.author.display_name , url="", icon_url=ctx.author.avatar)
            embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
            await ctx.respond(embed=embed)

        except:
            await ctx.respond("An error occured, please try another query.")

    # await wait.delete()

#slash help
@client.slash_command(guild_ids=[843878576981147648],description="Get a list of useful commands.")
async def help(ctx:discord.ApplicationContext):
    embed=discord.Embed(
                title='Bot Commands',
                color=0xEC2854,
                description='Please use these commands in a nsfw channel.'
            )
    embed.add_field(name='info', value=helpList['info'], inline=False)
    embed.add_field(name='cover', value=helpList['cover'], inline=False)
    embed.add_field(name='random', value=helpList['random'], inline=False)
    embed.add_field(name='pop', value=helpList['pop'], inline=False)
    embed.add_field(name='search', value=helpList['search'], inline=False)
    # embed.set_author(name=ctx.author.display_name , url="", icon_url=ctx.author.avatar)
    await ctx.respond(embed=embed)

#Slash Random
@client.slash_command(guild_ids=[843878576981147648], description="Get information about a random doujin.")
async def random(ctx:discord.ApplicationContext):
    if not (ctx.channel.is_nsfw()):
        await handleSlashNsfw(ctx)
        return            
    doujin=nhentai.get_random()
    embed=discord.Embed(
        title=doujin.title.english,
        type='rich',                
        url=doujin.url,
        color=0xEC2854
        )
    tags=''
    for i in range(5):  
        tags+=doujin.tags[i].name
        if i != 4:
            tags+=", "
    embed.add_field(name="Tags", value=tags, inline=False)
    embed.add_field(name="Id", value=doujin.id, inline=True)
    embed.add_field(name="Artists", value=doujin.artists[0].name if len(doujin.artists)!=0 else "-", inline=True)
    embed.add_field(name="Total Pages", value=doujin.total_pages, inline=True)
    embed.add_field(name="Favourites", value=doujin.total_favorites, inline=True)
    embed.add_field(name="Languages", value=doujin.languages[0].name, inline=True)
    embed.add_field(name="Groups", value=doujin.groups[0].name if len(doujin.groups)!=0 else "-", inline=True)
    # embed.set_author(name=ctx.author.display_name , url="", icon_url=ctx.author.avatar)
    embed.set_image(url=doujin.cover.src)
    embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
    await ctx.respond(embed=embed)

#Slash Popular
@client.slash_command(guild_ids=[843878576981147648],description="Get a list of trending doujins.")
async def popular(ctx:discord.ApplicationContext):
    if not (ctx.channel.is_nsfw()):
        await handleSlashNsfw(ctx)
        return         
    await ctx.defer()
    doujin=nhentai.get_popular_now()
    embed=discord.Embed(
        title="Popular Now", 
        type='rich',
        color=0xEC2854
    )
    
    for x in doujin.doujins:
        embed.add_field(name=x.title.english, value=x.url, inline=False)
        
    # embed.set_author(name=ctx.author.display_name , url="", icon_url=ctx.author.avatar)
    embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
    await ctx.respond(embed=embed)  
   


pre='nh!'
@client.event
async def on_message(message):

    if message.content.startswith(pre):
        txt=message.content
        command=txt.split(pre)[1].split()
        if command[0]=='ping':
            await message.channel.send(client.latency)

        #info command
        if (command[0]=='info'):
            if not (message.channel.is_nsfw()):
                await handleNsfw(message.channel)
                return
            try:
                code=command[1]
            except IndexError:
                await message.channel.send('Please enter an id')
                return
            doujin=nhentai.get_doujin(id=code)
            if doujin!= None:
                embed=discord.Embed(
                    title=doujin.title.english,
                    type='rich',                
                    url=doujin.url,
                    color=0xEC2854
                    )
                tags=''
                for i in range(5):
                    tags+=doujin.tags[i].name
                    if i != 4:
                        tags+=", "
                embed.add_field(name="Tags", value=tags, inline=False)
                embed.add_field(name="Id", value=doujin.id, inline=True)
                embed.add_field(name="Artists", value=doujin.artists[0].name if len(doujin.artists)!=0 else "-", inline=True)
                embed.add_field(name="Total Pages", value=doujin.total_pages, inline=True)
                embed.add_field(name="Favourites", value=doujin.total_favorites, inline=True)
                embed.add_field(name="Languages", value=doujin.languages[0].name, inline=True)
                embed.add_field(name="Groups", value=doujin.groups[0].name if len(doujin.groups)!=0 else "-", inline=True)
                embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar)
                embed.set_image(url=doujin.cover.src)
                embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                await message.channel.send(slMessage,embed=embed)            
            else:
                await message.channel.send("Invalid Code")
        
        #Search function
        elif command[0]=='search':
            if not (message.channel.is_nsfw()):
                await handleNsfw(message.channel)
                return

            try:
                query=command[1]
                num=command[2]
                results=nhentai.search(query=query, sort=None, page=1).total_results
            except:
                await message.channel.send('Please enter the correct format. \nUse `nh!help` for further information')
                return
                
            wait = await message.channel.send('Please wait...')
            embed=discord.Embed(
                title=query,
                color=0xEC2854
            )
            #print (results)
            if results==0:
                await message.channel.send('Sorry we could not find something for the entered query.')

            elif int(num)>20:
                await message.channel.send("Please keep the count below 20 :)")
            
            elif results<int(num):
                for i in range(results):
                    name=nhentai.search(query=query, sort=None, page=1).doujins[i].title.english
                    url=nhentai.search(query=query, sort=None, page=1).doujins[i].url
                    embed.add_field(name=name, value=url, inline=False)
                embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar)
                embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                await message.channel.send(embed=embed)

            else:
                try:
                    for i in range(int(num)):
                        name=nhentai.search(query=query, sort=None, page=1).doujins[i].title.english
                        url=nhentai.search(query=query, sort=None, page=1).doujins[i].url
                        embed.add_field(name=name, value=url, inline=False)
                    embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar)
                    embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                    await message.channel.send(slMessage,embed=embed)

                except:
                    await message.channel.send("An error occured, please try another query.")

            await wait.delete()


        #help function
        elif(command[0]=='help'):
            embed=discord.Embed(
                title='Bot Commands',
                color=0xEC2854,
                description='Please use these commands in a nsfw channel.'
            )
            embed.add_field(name='info', value=helpList['info'], inline=False)
            embed.add_field(name='cover', value=helpList['cover'], inline=False)
            embed.add_field(name='random', value=helpList['random'], inline=False)
            embed.add_field(name='pop', value=helpList['pop'], inline=False)
            embed.add_field(name='search', value=helpList['search'], inline=False)
            embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar)
            await message.channel.send(warning,embed=embed)
        
        #cover function   
        elif command[0]=='cover':
            if not (message.channel.is_nsfw()):
                await handleNsfw(message.channel)
                return
            code=command[1]
            doujin=nhentai.get_doujin(id=code)
            if doujin!= None:
                embed=discord.Embed(
                   title=doujin.title.english,
                   type='image',   
                   color=0xEC2854             
                   )            
                embed.set_image(url=doujin.cover.src)
                embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar)
                embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                await message.channel.send(slMessage,embed=embed)
            else:
                await message.channel.send("Invalid Code")
            
        #random function
        elif command[0]=='random':
            if not (message.channel.is_nsfw()):
                await handleNsfw(message.channel)
                return            
            doujin=nhentai.get_random()
            embed=discord.Embed(
                title=doujin.title.english,
                type='rich',                
                url=doujin.url,
                color=0xEC2854
                )
            tags=''
            for i in range(5):  
                tags+=doujin.tags[i].name
                if i != 4:
                    tags+=", "
            embed.add_field(name="Tags", value=tags, inline=False)
            embed.add_field(name="Id", value=doujin.id, inline=True)
            embed.add_field(name="Artists", value=doujin.artists[0].name if len(doujin.artists)!=0 else "-", inline=True)
            embed.add_field(name="Total Pages", value=doujin.total_pages, inline=True)
            embed.add_field(name="Favourites", value=doujin.total_favorites, inline=True)
            embed.add_field(name="Languages", value=doujin.languages[0].name, inline=True)
            embed.add_field(name="Groups", value=doujin.groups[0].name if len(doujin.groups)!=0 else "-", inline=True)
            embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar)
            embed.set_image(url=doujin.cover.src)
            embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
            await message.channel.send(slMessage,embed=embed)
            
         #popular function   
        elif command[0]=='pop':   
            if not (message.channel.is_nsfw()):
                await handleNsfw(message.channel)
                return         
            doujin=nhentai.get_popular_now()
            embed=discord.Embed(
                title="Popular Now", 
                type='rich',
                color=0xEC2854
            )
            
            for x in doujin.doujins:
                embed.add_field(name=x.title.english, value=x.url, inline=False)
            
            embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar)
            embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")

            await message.channel.send(slMessage,embed=embed)   

        elif (command[0]=='guild'):
            await message.channel.send("I'm in " + str(len(client.guilds)) + " servers!")     



client.run(os.getenv('TOKEN'))

