import discord
import os
from dotenv import load_dotenv
from NHentai import NHentai
from help import help




load_dotenv()
client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

nhentai = NHentai()

pre='nh!'
@client.event
async def on_message(message):


    if message.content.startswith(pre):
        txt=message.content
        if(txt==pre+'ping'):
            await message.channel.send('pong!')
        command=txt.split(pre)[1].split()

        if (command[0]=='info'):
            code=command[1]
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
        
        elif command[0]=='search':
            wait = await message.channel.send('Please wait...')

            query=command[1]
            num=command[2]
            embed=discord.Embed(
                title=query,
                color=0xEC2854
            )
            results=nhentai.search(query=query, sort=None, page=1).total_results
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
                color=0xEC2854
            )
            embed.add_field(name='info', value=help['info'], inline=False)
            embed.add_field(name='cover', value=help['cover'], inline=False)
            embed.add_field(name='random', value=help['random'], inline=False)
            embed.add_field(name='pop', value=help['pop'], inline=False)
            embed.add_field(name='search', value=help['search'], inline=False)
            embed.set_author(name=message.author.display_name , url="", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
            
        elif command[0]=='cover':
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



client.run(os.getenv('TOKEN'))