"""
Définit toutes les commandes du bot via la fonction load_commands.
"""

# Import des librairies et modules
import discord 
from discord.ext import commands


import bot_console_dialog



def load_commands(bot:commands.bot.Bot):
    """
    Prend en paramètre un bot discord de discord.ext et lui définit les évènements et commandes rédigées pour Zer0 bot.
    Cette définition des commandes va être validée par l'event on_ready.
    """
 
    #___EVENTS
    @bot.event
    async def on_ready():
        """Lorsque le bot est prêt, syncronise les commandes commentées avec le bot."""
        nb_commandes_syncro = len(await bot.tree.sync())
        bot_console_dialog.confirm(f"{nb_commandes_syncro} commandes ont été chargées avec succès.")

    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        # Récupérer l'erreur d'origine si l'erreur est encapsulée
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original
    
        # Message d'erreur personnalisé à envoyer à l'utilisateur
        message_erreur = f"⚠️ **Une erreur est survenue lors de l'exécution :**\n`{type(error).__name__}: {error}`"
    
        try:
            # Si le bot a déjà commencé à répondre (defer), on utilise followup
            if interaction.response.is_done():
                await interaction.followup.send(message_erreur, ephemeral=True)
            else:
                await interaction.response.send_message(message_erreur, ephemeral=True)
        except Exception as e:
            print(f"Impossible d'envoyer le message d'erreur sur Discord : {e}")
        

    #___COMMANDES
    @bot.tree.command(name="restart", description="Redémarre le bot.")
    async def restart(interaction: discord.Interaction):
        """
        Permet de rédémarrer le bot.
        """  
        await interaction.response.send_message("Okay le goat, je redémarre pour toi <3", ephemeral=True)

        await commands.restart(bot)
        

    @bot.tree.command(name="services_introuvables", description="Indique tous les services qui n'ont pas pu être lancés.")
    async def services_introuvables(interaction: discord.Interaction):
        # laisse le temps au bot de réfléchir
        await interaction.response.defer(thinking=True) 
        
        await interaction.followup.send( commands.services_introuvables() )

    @bot.tree.command(name="services_obtain", description="Charge chacun des services introuvables depuis github.")
    async def services_obtain(interaction: discord.Interaction):
        # laisse le temps au bot de réfléchir
        await interaction.response.defer(thinking=True) 

        await interaction.followup.send( commands.services_obtain(L_services_non_trouves) )
    
    @bot.tree.command(name="services_update", description="Met à jour chacun des services à la version disponible sur github.")
    async def services_update(interaction: discord.Interaction):
        # laisse le temps au bot de réfléchir
        await interaction.response.defer(thinking=True) 

        await interaction.followup.send( commands.services_update(L_services, L_services_non_trouves))

    @bot.tree.command(name="services_force", description="/service_obtain → /service_update → /restart")
    async def services_force(interaction: discord.Interaction):
        # laisse le temps au bot de réfléchir
        await interaction.response.defer(thinking=True)

        await interaction.followup.send( "Obtention, actualisation des services et redémarrage.")

    @bot.tree.command(name="annoying_text", description="Permet de randomiser les lettres du texte fourni.")
    async def annoying_text(interaction: discord.Interaction, texte_a_randomiser:str):
        # laisse le temps au bot de réfléchir
        await interaction.response.defer(thinking=True) 

        if SERVICE_AT not in L_services_non_trouves:
            resultat = codertexte(texte_a_randomiser)
        else:
            resultat = SERVICE_INTROUVABLE
        await interaction.followup.send(resultat)

    @bot.tree.command(name="chest_hunt_simulator_idle_slayer", description="Permet de randomiser les lettres du texte fourni.")
    async def chest_hunt_simulator_idle_slayer(interaction: discord.Interaction, nombre_generations:int, nombre_simulations:int):
        # laisse le temps au bot de réfléchir
        await interaction.response.defer(thinking=True) 
        
        if SERVICE_CHSIS not in L_services_non_trouves:
            resultat = simuler(nombre_generations,nombre_simulations)
        else:
            resultat = SERVICE_INTROUVABLE
        await interaction.followup.send(resultat)

        
        await commands.envoyer_message_en_morceaux(resultat,interaction)
    
    

#constantes messsages d'erreur
SERVICE_INTROUVABLE = "❌ Le service est introuvable, essayez /services_obtain et de relancer le bot."

#constantes de noms services
SERVICE_AT = "annoying_text"
SERVICE_CHSIS = "chest_hunt_simulator_idle_slayer"

# Commandes
import commands

# Import des services, et si un service est introuvable, il est flag comme non trouvé.
L_services = [SERVICE_AT,SERVICE_CHSIS]
L_services_non_trouves = []
try:    from services.annoying_text.annoyingtext import codertexte
except ModuleNotFoundError: L_services_non_trouves.append(SERVICE_AT)

try:    from services.chest_hunt_simulator_idle_slayer.simu import simuler
except ModuleNotFoundError: L_services_non_trouves.append(SERVICE_CHSIS)
