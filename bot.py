import os
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Carrega as variáveis do arquivo .env
load_dotenv()

# Atribui o Token do BotAPI
TOKEN = os.environ.get("BOT_TOKEN")

# Cria uma lista com algumas curiosidades sobre a FURIA
curiosidades = [
    "A FURIA foi fundada em 2017 e já jogou vários Majors de CS:GO, entre eles, o lendário Major do Rio no qual a FURIA fez história conquistando a semifinal em cima da NAVI de S1mple.",
    "O estilo agressivo de jogo da FURIA ficou conhecido como 'Furia style'.",
    "A FURIA tem uma das torcidas mais engajadas do mundo no cenário de esports.",
    "Em 2020, a FURIA entrou para o top 5 mundial no ranking da HLTV."
]

# Cria uma lista com os jogadores da FURIA e suas funções
jogadores = [
    ("FalleN", "IGL"),
    ("KSCERATO", "Rifler / Lurcker"),
    ("yuurih", "Rifler"),
    ("YEKINDAR", "Rifler / Entry fragger"),
    ("molodoy", "AWPer")
]

# Cria uma lista dos próximos jogos simulados
proximos_jogos = [
    ("FURIA vs G2", "🏆 IEM Dallas 2025 — 15/05/2025 às 16h"),
    ("FURIA vs FaZe", "🏆 BLAST Premier — 20/05/2025 às 18h"),
    ("FURIA vs Vitality", "🏆 ESL Pro League — 25/05/2025 às 14h")
]
    
# Função do comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Envia o logo da FURIA
    await update.message.reply_photo(
        photo="https://dribbble.com/shots/23136059-Furia-Redesign",
    )

    # Texto principal com as instruções
    texto = (
        "Salve FURIOSO!\n"
        "Eu sou o bot oficial da torcida! 🔥 Aqui você pode acompanhar o time de CS com estilo!\n\n"
        "📋 Escolha uma opção abaixo 👇" 
    )
    
    # Cria os botões
    keyboard = [
        [InlineKeyboardButton("📅 Próximos Jogos", callback_data="jogos")],
        [InlineKeyboardButton("📰 Notícias", callback_data="noticias")],
        [InlineKeyboardButton("🧍 Elenco", callback_data="elenco")],
        [InlineKeyboardButton("🧠 Curiosidade", callback_data="curiosidade")],
        [InlineKeyboardButton("🆘 Ajuda", callback_data="ajuda")],
        [InlineKeyboardButton("🎯 Sobre", callback_data="sobre")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(texto, reply_markup=reply_markup)

# Função para exibir os próximos jogos
def buscar_jogos():
    jogos_texto = "\n\n".join([f"• {partida}\n{detalhes}" for partida, detalhes in proximos_jogos])
    return jogos_texto

# Função para buscar noticias
def buscar_noticias_furia():
    url = "https://draft5.gg/equipe/330-FURIA"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"❌ Erro ao acessar Draft5: status {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # Pega todas as divs que têm a notícia
        noticias_divs = soup.find_all("div", class_="Card__CardContainer-sc-122kzjp-0")

        noticias = []
        for div in noticias_divs:
            link_tag = div.find("a")
            if link_tag:
                href = link_tag.get("href")
                if href and href.startswith("/noticia/"):
                    titulo = link_tag.get_text(strip=True)
                    link = "https://draft5.gg" + link_tag.get("href")
                    noticias.append(f"📰 [{titulo}]({link})")
                
            if len(noticias) == 5: 
                break

        return "\n\n".join(noticias) if noticias else "Nenhuma notícia da FURIA encontrada."
    
    except Exception as e:
        return f"❌ Erro inesperado: {str(e)}"
    
# Função do comando /ajuda
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_ajuda = (
        "🆘 *AJUDA FURIOSA!*\n\n"
        "Eu sou o bot oficial da torcida da FURIA! Aqui estão meus comandos:\n\n"
        "• /start — Inicia o bot e exibe o menu principal.\n"
        "• /ajuda — Mostra esta mensagem de ajuda.\n"
        "• /sobre — Mostra informações sobre a criação do Bot.\n\n"
        "📋 Também é possível usar os botões abaixo da mensagem principal para:\n"
        "- Ver os *Próximos Jogos*\n"
        "- Ler uma *Curiosidade* sobre a FURIA\n"
        "- Ver o *Elenco Atual*\n"
        "- Ler as *Últimas Notícias*\n\n"
        "*Vamos juntos torcer pela FURIA! 🔥*\n"
    )

    # Verifique se o update tem uma mensagem de callback_query
    if update.callback_query:
        await update.callback_query.message.reply_text(texto_ajuda, parse_mode="Markdown")
    else:
        # Caso seja um comando direto como /ajuda
        await update.message.reply_text(
            texto_ajuda, 
            parse_mode="Markdown"
        )

# Função para o /sobre
async def sobre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_sobre = (
        "💻 Desenvolvido por João Felipe Fernandes Pimentel\npara demonstração técnica.\n"
        "Bot focado em torcedores da FURIA! 🔥"
    )

    # Verifique se o update tem uma mensagem de callback_query
    if update.callback_query:
        await update.callback_query.message.reply_text(texto_sobre)
    else:
        # Caso seja um comando direto como /sobre
        await update.message.reply_text(texto_sobre)

# Função para lidar com os botões   
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    fato = random.choice(curiosidades)

    if data == "jogos":
        jogos = buscar_jogos()
        await query.edit_message_text(f"📅 Próximos jogos da FURIA:\n\n{jogos}")
    elif data == "noticias":
        noticias = buscar_noticias_furia()
        await query.edit_message_text(
            f"*📰 Últimas notícias sobre a FURIA:*\n\n{noticias}",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    elif data == "elenco":
        elenco_texto = "🧍 *Elenco Atual da FURIA:*\n"
        elenco_texto += "\n".join([f"• *{nome}* — {funcao}" for nome, funcao in jogadores])
        await query.edit_message_text(elenco_texto, parse_mode="Markdown")
    elif data == "curiosidade":
        await query.edit_message_text(f"🧠 Curiosidade FURIA:\n{fato}")
    elif data == "ajuda":
        await ajuda(update, context)
    elif data == "sobre":
        await sobre(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ajuda", ajuda))
app.add_handler(CommandHandler("sobre", sobre))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot rodando...")
app.run_polling()