import discord
import os
from dotenv import load_dotenv
from NHentai import NHentai
from help import help




load_dotenv()
client = discord.Client()
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

pre='nh!'
@client.event
async def on_message(message):

    if message.content.startswith(pre):
        txt=message.content
        command=txt.split(pre)[1].split()
        if command[0]=='ping':
            await message.channel.send(client.latency)


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
                embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
                embed.set_image(url=doujin.cover.src)
                embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                await message.channel.send(embed=embed)            
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
                embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
                embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                await message.channel.send(embed=embed)

            else:
                try:
                    for i in range(int(num)):
                        name=nhentai.search(query=query, sort=None, page=1).doujins[i].title.english
                        url=nhentai.search(query=query, sort=None, page=1).doujins[i].url
                        embed.add_field(name=name, value=url, inline=False)
                    embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
                    embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                    await message.channel.send(embed=embed)

                except:
                    await message.channel.send("An error occured, please try another query.")

            await wait.delete()


        
        elif(command[0]=='help'):
            embed=discord.Embed(
                title='Bot Commands',
                color=0xEC2854,
                description='Please use these commands in a nsfw channel.'
            )
            embed.add_field(name='info', value=help['info'], inline=False)
            embed.add_field(name='cover', value=help['cover'], inline=False)
            embed.add_field(name='random', value=help['random'], inline=False)
            embed.add_field(name='pop', value=help['pop'], inline=False)
            embed.add_field(name='search', value=help['search'], inline=False)
            embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
            
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
                embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
                embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Invalid Code")
            

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
            embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
            embed.set_image(url=doujin.cover.src)
            embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")
            await message.channel.send(embed=embed)
            
            
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
            
            embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
            embed.set_thumbnail(url="https://i.imgur.com/IGLxm6C.png")

            await message.channel.send(embed=embed)   

        elif (command[0]=='guild'):
            await message.channel.send("I'm in " + str(len(client.guilds)) + " servers!")     



client.run(os.getenv('TOKEN'))
