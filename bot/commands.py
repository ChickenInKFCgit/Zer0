import os
import discord

def deplacer_chemin_courant():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


async def restart(bot):
    # 1. On ferme proprement la connexion Discord
    await bot.close()
    
    from pathlib import Path
    import subprocess
    
    
    # 2. On calcule la racine absolue du projet
    racine_projet = Path(__file__).resolve().parent.parent
    
    python_env = str(racine_projet / ".env" / "Scripts" / "python.exe")
    script_bot = str(racine_projet / "bot" / "bot.py")
    
    # On relance le bot en forçant sont répertoire de travail
    subprocess.Popen([python_env, script_bot], cwd=str(racine_projet))
    
    # 4. On tue INSTANTANÉMENT le processus actuel pour laisser la place au nouveau
    os._exit(0)

async def envoyer_message_en_morceaux(message:str, interaction: discord.Interaction): 
    """
    Découpe un message bien trop long en petits messages afin de permettre l'envoi.
    """ 
    taille_max = 1900 

    for morceau in [message[i:i + taille_max] for i in range(0, len(message), taille_max)]:
        await interaction.followup.send(morceau)

async def services_introuvables(L_services_non_trouves:list)->str:
    if len(L_services_non_trouves) > 0:
        texte="Services qui n'ont pas pu être lancés : "
    else :
        texte="✅ Aucun service  introuvable."
    
    for service in L_services_non_trouves:
        texte +=f"\n- {service}"
    return texte

async def services_obtain(L_services_non_trouves:list)->str:
    if len(L_services_non_trouves) > 0:
        texte="Obtention des services non-trouvés :"
    else :
        texte="✅ Aucun service non trouvé, obtention des services annulée."
    deplacer_chemin_courant()
    for service in L_services_non_trouves:
        texte +=f"\n- {service} : " 
        texte+=bot_git.clone_service(service)
    return texte

async def services_update(L_services:list, L_services_non_trouves:list)->str:
    if len(L_services) > 0:
        texte="Actualisation des services :"
    else:
        texte="❌ Aucun service, impossible d'en actualiser."
    deplacer_chemin_courant()
    for service in L_services:
        texte +=f"\n- {service} : " 
        if service not in L_services_non_trouves:
            texte+=bot_git.pull_service(service)
        else:
            texte+=f"Impossible de pull, service {service} introuvable"
    return texte

async def services_trouvables(L_services:list, L_services_non_trouves:list)->str:
    if len(L_services) > 0:
        texte="Actualisation des services :"
    else:
        texte="❌ Aucun service."
    
    deplacer_chemin_courant()
    for service in L_services: 
        if service not in L_services_non_trouves:
            texte+= f"\n- {service} est chargé 🥹"
    return texte

async def services_force(L_services:list, L_services_non_trouves:list):
    await services_obtain(L_services_non_trouves)
    await services_update(L_services,L_services_non_trouves)
    await restart()


# Init Git
deplacer_chemin_courant()
import bot_git as bot_git