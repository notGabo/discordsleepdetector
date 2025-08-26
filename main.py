import discord
from os import getenv
from dotenv import load_dotenv
from time import time

load_dotenv()

TOKEN = getenv('BOT_TOKEN')
LISTA_PERSONAS = [int(x) for x in getenv('ID_PERSONAS').split(',')]
CHANNEL_ID = int(getenv('CHANNEL_ID', 0))

offline_times = {}

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Monitoreando {len(LISTA_PERSONAS)} usuarios')

@client.event
async def on_presence_update(before, after):
    user = str(await client.fetch_user(after.id))
    if user == 'ldreamzl': user = 'martin'
    elif user == 'nafle': user = 'gabo'

    if after.id not in LISTA_PERSONAS:
        return

    if not CHANNEL_ID:
        print("No se ha configurado un canal para enviar mensajes.")
        return

    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print(f"No se pudo encontrar el canal con ID {CHANNEL_ID}")
        return
    # cuando un usuario se desconecta
    if (before.status != discord.Status.offline or before.status != discord.Status.idle) and (after.status == discord.Status.offline or after.status == discord.Status.idle):
        offline_times[after.id] = time()
        print(f"{user} se fue.")

    # cuando un usuario se conecta
    elif (before.status == discord.Status.offline or before.status == discord.Status.idle) and (after.status != discord.Status.offline or after.status != discord.Status.idle):
        if after.id in offline_times:
            tiempo_desconectado = time() - offline_times[after.id]

            tiempo_formateado = format_time(tiempo_desconectado, user)
            mensaje = 'se conecto' if before.status == discord.Status.offline else 'volvio'
            #await channel.send(f"<@{after.id}> {mensaje} despues de {tiempo_formateado}.")
            await channel.send(f"el {user} {mensaje} despues de {tiempo_formateado}.")

            # Eliminar del registro ya que está conectado ahora
            del offline_times[after.id]
        else:
            # Si no tenemos registro de desconexión
            await channel.send(f"{user} se ha conectado. no se desde cuando Dx")

def format_time(seconds, user):
    """Formatea el tiempo en segundos a un formato legible."""
    if seconds < 60:
        return f"{int(seconds)} segundos, omg se demoro poco"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutos, {'omg se demoro poco' if seconds <= 300 else f'{user} ctm demorate ma'}"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours} horas y {minutes} minutos, {'volvio de cosechar el trigo pa hacerse el pan' if hours <= 2 else 'por fin se desperto'}"
    else:
        days = int(seconds / 86400)
        hours = int((seconds % 86400) / 3600)
        return f"{days} días y {hours} horas, VOLVIO DE LA MUERTECTM"

client.run(TOKEN)