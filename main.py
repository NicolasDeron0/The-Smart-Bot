# test-bot(bot class)
# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
import random
import os
from discord.ext import commands
from bot_logic import gen_pass
import requests
from logic_poke import Pokemon
from model import get_class
from detect_objects import detect
from IND_Summary import summariztion
from ENG_summary import summarization
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
description = '''An example bot to showcase the discord.ext.commands extension
module.
You can use this bot to test out the commands and see how they work.
The commands are all prefixed with $ and can be used in any channel
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# command prefix 
bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})') # type: ignore
    print('-----------')

# calculator with 3 numbers
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def subtract(ctx, left: int, right: int):
    """Subtracts two numbers together."""
    await ctx.send(left - right)

@bot.command()
async def multiply(ctx, left: int, right: int):
    """Multiplies two numbers together."""
    await ctx.send(left * right)

@bot.command()
async def divide(ctx, left: int, right: int):
    """Divides two numbers together."""
    await ctx.send(left / right)

@bot.command()
async def exponentiate(ctx, left: int, right: int):
    """Exponents two numbers together."""
    await ctx.send(left ** right)

@bot.command()
async def modulo(ctx, left: int, right: int):
    """Remains of a division of two numbers together."""
    await ctx.send(left % right)

@bot.command()
async def gocrazy(ctx):
    await ctx.send("\U0001f601 \U0001f923 \U0001f609 \U0001f923 \U0001f61d")

@bot.command()
async def bruh(ctx):
    await ctx.send("\U0001f611")

# spamming word
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
        
# password generator        
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)
    if num == 1:
        await ctx.send('It is Heads!')
    if num == 2:
        await ctx.send('It is Tails!')

@bot.command()
async def whatsup(ctx):
    await ctx.send("I'm good!")

@bot.command()
async def flipflop(ctx, Flip: str = None):
    computer = random.choice(['Flip', 'Flop'])
    if Flip == computer:
        await ctx.send('Same! I picked ' + computer + '!')
    if Flip != computer:
        await ctx.send('Different... I picked ' + computer + '!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1,6)
    if nums == 1:
        await ctx.send('It is 1!')
    elif nums == 2:
        await ctx.send('It is 2!')
    elif nums == 3:
        await ctx.send('It is 3!')
    elif nums == 4:
        await ctx.send('It is 4!')
    elif nums == 5:
        await ctx.send('It is 5!')
    elif nums == 6:
        await ctx.send('It is 6!')

# overwriting kalimat.txt
@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        text = ""
        text += my_string
        t.write(text)
# append kalimat.txt
@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        text = "\n"
        text += my_string
        t.write(text)
# reading kalimat.txt
@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)

    # random local meme image
@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('meme'))
    with open(f'meme/{img_name}', 'rb') as f:
    # with open(f'meme/enemies-meme.jpg', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def animal(ctx):
    img_animal = random.choice(os.listdir('animal'))
    with open(f'animal/{img_animal}', 'rb') as f:
    # with open(f'meme/enemies-meme.jpg', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
    await ctx.send(file=picture)

# API to get random dog and duck image 
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('dog')
async def dog(ctx):
    '''Setiap kali permintaan dog (anjing) dipanggil, program memanggil fungsi get_dog_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    '''Setiap kali permintaan duck (bebek) dipanggil, program memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

# The '$go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    # if author not in Pokemon.pokemons.keys():
    pokemon = Pokemon(author)  # Creating a new Pokémon
    await ctx.send(await pokemon.info())  # Sending information about the Pokémon
    image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
    if image_url:
        embed = discord.Embed()  # Creating an embed message
        embed.set_image(url=image_url)  # Setting up the Pokémon's image
        await ctx.send(embed=embed)  # Sending an embedded message with an image
    else:
        await ctx.send("Failed to upload an image of the pokémon.")

@bot.command()
async def polution_tips(ctx):
    tips = [
        'Reduce, Reuse, Recycle! Dont forget!',
        'Dont litter! Throw your trash in the recycle bin!',
        'Dont use plastic! They are hard to recycle.',
        'Reduce the usage of cars, they create gas that is harmful to the atmosphere!',
        'Do plant more trees, they create oxygen, to give us air.'
    ]
    acak = random.choice(tips)
    await ctx.send(acak)

# Warning Pollution
@bot.command()
async def peringatan(ctx):
    await ctx.send(f'Berikut adalah link peringatan polusi sesuai lokasi Anda : https://www.meteoblue.com/en/weather/widget/setupday/atambua_indonesia_1651103 , Kamu bisa gatikan tempat lokal sesuai tempat lokalmu.')

@bot.command()
async def inspiration(ctx):
    inspire = [
        'santai',
        'gak usah marah-marah',
        'tenang, damai',
        'lakukan tugasmu',
        'dengerin bapak emak',
        'sadar diri'
    ]
    inspiracy = random.choice(inspire)
    await ctx.send(inspiracy)

#show local drive    
@bot.command()
async def local_drive(ctx):
    try:
      folder_path = "./files"  # Replace with the actual folder path
      files = os.listdir(folder_path)
      file_list = "\n".join(files)
      await ctx.send(f"Files in the files folder:\n{file_list}")
    except FileNotFoundError:
      await ctx.send("Folder not found.")

#show local file
@bot.command()
async def showfile(ctx, filename):
  """Sends a file as an attachment."""
  folder_path = "./files/"
  file_path = os.path.join(folder_path, filename)
  try:
    await ctx.send(file=discord.File(file_path))
  except FileNotFoundError:
    await ctx.send(f"File '{filename}' not found.")

# upload file to local computer
@bot.command()
async def simpan(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            # file_url = attachment.url  IF URL
            await attachment.save(f"./files/{file_name}")
            await ctx.send(f"Menyimpan {file_name}")
    else:
        await ctx.send("Anda lupa mengunggah :(")

# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}') # type: ignore
    # provide what you can help here

@bot.command()
async def klasifikasi(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            #file_url = attachment.url IF URL
            await attachment.save(f"./CV/{file_name}")
            await ctx.send(get_class(model_path="keras_model4.h5", labels_path="labels4.txt", image_path=f"./CV/{file_name}"))
    else:
        await ctx.send("Anda lupa mengunggah gambar :(")

@bot.command()
async def info(ctx):
    await ctx.send('''Berikut adalah beberapa perintah yang bisa kamu gunakan:
    $add <left> <right> : Menjumlahkan dua angka
    $subtract <left> <right> : Mengurangkan dua angka
    $multiply <left> <right> : Mengalikan dua angka
    $divide <left> <right> : Membagi dua angka
    $exponentiate <left> <right> : Memangkatkan dua angka
    $modulo <left> <right> : Menghitung sisa bagi dua angka
    $gocrazy : Mengirimkan emoji gila
    $bruh : Mengirimkan emoji bruh
    $repeat <times> <content> : Mengulangi pesan beberapa kali
    $pw : Menghasilkan kata sandi acak
    $coinflip : Menghasilkan koin
    $dice : Menghasilkan dadu
    $tulis <my_string> : Menulis kalimat ke dalam file
    $tambahkan <my_string> : Menambahkan kalimat ke dalam file
    $baca : Membaca kalimat dari file
    $meme : Mengirimkan gambar meme acak
    $animal : Mengirimkan gambar hewan acak
    $dog : Mengirimkan gambar anjing acak
    $duck : Mengirimkan gambar bebek acak
    $go : Memulai permainan Pokemon
    $peringatan : Mengirimkan link peringatan polusi
    $inspiration : Mengirimkan kalimat inspirasi
    $local_drive : Menampilkan file di folder lokal
    $showfile <filename> : Mengirimkan file dari folder lokal
    $simpan : Menyimpan file yang diunggah
    $joined <member> : Menampilkan kapan anggota bergabung
    $klasifikasi : Mengklasifikasikan gambar yang diunggah
    $help : Menampilkan daftar perintah yang tersedia
    $deteksi : Mendeteksi objek dalam gambar yang diunggah ( maximum panjangnya 2000 pixel)
    $analisis <kalimat> : Menganalisis kalimat dalam bahasa Indonesia
    $analysis <kalimat2> : Menganalisis kalimat dalam bahasa Inggris
    $sentiment_vander <kalimat4> : Menganalisis sentimen kalimat
    ''')

@bot.command()
async def deteksi(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            #file_url = attachment.url IF URL
            await attachment.save(f"./CV/{file_name}")
            await ctx.send(detect(input_image=f"./CV/{file_name}", output_image=f"./CV/{file_name}", model_path="yolov3.pt"))
            with open(f'CV/{file_name}', 'rb') as f:
                picture = discord.File(f)
            await ctx.send(file=picture) 
    else:
        await ctx.send("Anda lupa mengunggah gambar :(")

# teks analytics IND dev
@bot.command()
async def analisis(ctx, *, kalimat: str):
    await ctx.send(f"keyword: {summariztion(kalimat)}")

# teks analytics ENG dev
@bot.command()
async def analysis(ctx, *, kalimat2: str):
    await ctx.send(f"keyword: {summarization(kalimat2)}")

# sentiment dev.
@bot.command()
async def sentiment_vander(ctx, *, kalimat4: str):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(kalimat4)
    # Format the output for better readability
    formatted_scores = f"""
    Negative: {scores['neg']:.3f}
    Neutral: {scores['neu']:.3f}
    Positive: {scores['pos']:.3f}
    Compound: {scores['compound']:.3f}
    """
    await ctx.send(f"Score: {formatted_scores}")

# Run the bot with the token
# Sorry, token not availble
