import discord
from os import getenv
from dotenv import load_dotenv
from time import time
from datetime import datetime

load_dotenv()

TOKEN = getenv('BOT_TOKEN')
LISTA_PERSONAS = [int(x) for x in getenv('ID_PERSONAS').split(',')]
CHANNEL_ID = int(getenv('CHANNEL_ID', 0))
DEBOUNCE_TIME = 0.5

ultima_actualizacion_estado = {}

offline_times = {}

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_presence_update(before, after):
    # añadir checkeo de debounce
    momento_actual = time()
    if after.id in ultima_actualizacion_estado:
        if momento_actual - ultima_actualizacion_estado[after.id] < DEBOUNCE_TIME:
            return

    ultima_actualizacion_estado[after.id] = momento_actual

    channel = client.get_channel(CHANNEL_ID)

    user = str(await client.fetch_user(after.id))
    if user == 'ldreamzl': user = 'martin'
    elif user == 'nafle': user = 'gabo'

    if after.id not in LISTA_PERSONAS:
        return

    if not CHANNEL_ID:
        print("No se ha configurado un canal para enviar mensajes")
        return

    if not channel:
        print(f"No se pudo encontrar el canal con ID {CHANNEL_ID}")
        return

    estados_online = [discord.Status.online, discord.Status.do_not_disturb, discord.Status.dnd]
    estados_offline = [discord.Status.idle, discord.Status.offline, discord.Status.invisible]

    # Detectar cuando se desconecta y manejar mensaje
    if (before.status in estados_online) and (after.status in estados_offline):
        if after.id not in offline_times:
            offline_times[after.id] = time()
            hora_actual = datetime.now().time()
            if hora_actual >= datetime.strptime("03:00", "%H:%M").time() and hora_actual <= datetime.strptime("10:00", "%H:%M").time():
                await channel.send(f"el {user} por fin, duerme mono culiao q te vai a enfermar")
            else:
                await channel.send(f"el {user} se fue a jugar con sus verdaderos amigos")


    # Detectar cuando se conecta y manejar mensaje
    elif (before.status in estados_offline) and (after.status in estados_online):
        try:
            tiempo_desconectado = time() - offline_times[after.id]
            tiempo_formateado = format_time(tiempo_desconectado, user)
            mensaje = 'se conecto' if before.status == discord.Status.offline else 'volvio'
            await channel.send(f"el {user} {mensaje} despues de {tiempo_formateado}")
            del offline_times[after.id]
        except Exception as e:
            print(f"Error al calcular tiempo desconectado: {e}")
            await channel.send(f"el {user} se ha conectado. no se desde cuando Dx")


def format_time(seconds, user):
    """Formatea el tiempo en segundos a un mensaje utilizable."""
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