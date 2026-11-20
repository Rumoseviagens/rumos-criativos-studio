#!/usr/bin/env python3
"""
Publicador Automático de Lâminas — Meta Ads (Rumos e Viagens / Azul Viagens Barra)
Baixa todas as 10 lâminas da pasta LAMINAS DA RUMOS (ou lê de uma pasta local),
faz upload das imagens na conta de anúncios Meta (act_...), cria os AdCreatives
com copy otimizada para WhatsApp/Direct e publica os Anúncios no AdSet ativo.
"""
import os
import sys
import json
import urllib.request
import urllib.parse

GRAPH_API_VERSION = "v21.0"
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# ==============================================================================
# CONFIGURAÇÃO DA CONTA META ADS (Lê do ambiente ou de meta_config.json)
# ==============================================================================
CONFIG_FILE = os.environ.get("META_CONFIG_FILE", "meta_config.json")
config = {}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN") or config.get("access_token", "")
AD_ACCOUNT_ID = os.environ.get("META_AD_ACCOUNT_ID") or config.get("ad_account_id", "")  # ex: act_123456789
ADSET_ID = os.environ.get("META_ADSET_ID") or config.get("adset_id", "")
PAGE_ID = os.environ.get("META_PAGE_ID") or config.get("page_id", "")
INSTAGRAM_ACTOR_ID = os.environ.get("META_INSTAGRAM_ID") or config.get("instagram_actor_id", "")
WHATSAPP_URL = os.environ.get("META_WHATSAPP_URL") or config.get("whatsapp_url", "https://wa.me/5521999061999")
AD_STATUS = os.environ.get("META_AD_STATUS") or config.get("ad_status", "ACTIVE")

# ==============================================================================
# CATÁLOGO DAS 10 LÂMINAS DA PASTA "LAMINAS DA RUMOS" (1080x1350 - 4:5)
# ==============================================================================
LAMINAS = [
    {
        "drive_id": "1cRzcqZYQMaHWyRy488RSyKBel_J0qVx4",
        "filename": "rumos_s_o_miguel_dos_milagres_Feed_1080x1350.png",
        "name": "AD 01 - São Miguel dos Milagres (Naim Milagres) - 4:5",
        "headline": "São Miguel dos Milagres: 10x R$ 366,82 sem juros!",
        "description": "Embarque RJ • Loja Shopping Downtown Barra",
        "message": (
            "🌴 Uma semana no paraíso de São Miguel dos Milagres saindo do Rio de Janeiro!\n\n"
            "✈️ Aéreo Ida e Volta\n"
            "🏨 6 dias / 5 noites no Naim Milagres (4★)\n"
            "☕ Café da Manhã incluso\n"
            "🚐 Traslado Ida e Volta\n"
            "📅 Período: 13 a 18 de Setembro de 2027\n\n"
            "💰 A partir de 10x de R$ 366,82 sem juros (ou R$ 3.668,24 à vista)\n\n"
            "📍 Atendimento oficial na nossa loja no Shopping Downtown Barra (RJ) ou clique para falar no WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "13iedZT4Z6coEhmZrW9mpXi4BBv4qjbE5",
        "filename": "rumos_salvador_Feed_1080x1350.png",
        "name": "AD 02 - Salvador All Inclusive (Iberostar Waves) - 4:5",
        "headline": "Iberostar Bahia 5★ All Inclusive: 10x R$ 486,60!",
        "description": "Embarque RJ • Loja Shopping Downtown Barra",
        "message": (
            "🍹 O melhor Resort 5 Estrelas All Inclusive da Bahia esperando por você!\n\n"
            "✈️ Aéreo Ida e Volta saindo do RJ\n"
            "🏨 5 dias / 4 noites no Iberostar Waves Bahia (5★)\n"
            "🍹 100% All Inclusive (refeições, petiscos e bebidas)\n"
            "🚐 Traslado Ida e Volta\n"
            "📅 Período: 18 a 22 de Maio de 2027\n\n"
            "💰 A partir de 10x de R$ 486,60 sem juros (ou R$ 4.866,03 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Clique para chamar nossos especialistas no WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1iTbaxHtZZWZRkcqdL1JgBNtY0Hj8xvYh",
        "filename": "rumos_cura_ao_Feed_1080x1350.png",
        "name": "AD 03 - Curaçao Carnaval 2027 - 4:5",
        "headline": "Carnaval 2027 no Caribe (Curaçao): 10x R$ 956,67!",
        "description": "Embarque RJ • Loja Shopping Downtown Barra",
        "message": (
            "🏝️ Viva o Carnaval 2027 no mar azul-turquesa de Curaçao!\n\n"
            "✈️ Aéreo Ida e Volta saindo do RJ\n"
            "🏨 8 dias / 7 noites no Delynne Boutique Hotel\n"
            "🚐 Traslado Ida e Volta + 🛡️ Seguro Viagem\n"
            "📅 Período de Carnaval: 07 a 14 de Fevereiro de 2027\n\n"
            "💰 A partir de 10x de R$ 956,67 sem juros (ou R$ 9.566,66 à vista)\n\n"
            "📍 Loja oficial no Shopping Downtown Barra (RJ) • Clique e reserve pelo WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1HHQ5ppluEvt737l5xKAH2TnecmvtpAxB",
        "filename": "rumos_porto_de_galinhas_Feed_1080x1350.png",
        "name": "AD 04 - Porto de Galinhas (Porto Alto Resort) - 4:5",
        "headline": "Porto de Galinhas (Porto Alto Resort): 10x R$ 381,05!",
        "description": "Voo Direto RJ • Loja Shopping Downtown Barra",
        "message": (
            "🐠 Porto de Galinhas em Resort 4★ com Voo Direto saindo do Rio!\n\n"
            "✈️ Aéreo Ida e Volta (Voo Direto)\n"
            "🏨 6 dias / 5 noites no Porto Alto Resort GAV (4★)\n"
            "☕ Café da Manhã + 🚐 Traslado + 🎟️ Passeio Incluso\n"
            "📅 Período: 25 a 30 de Março de 2027\n\n"
            "💰 A partir de 10x de R$ 381,05 sem juros (ou R$ 3.810,51 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Chame agora no WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1MnHk5QJ-DFBu77BC6F7PnKbUHK56L6Am",
        "filename": "rumos_gramado_rio_grande_do_sul_Feed_1080x1350.png",
        "name": "AD 05 - Gramado Páscoa 2027 - 4:5",
        "headline": "Páscoa em Gramado (6 Dias): 10x R$ 214,99 sem juros!",
        "description": "Voo Direto RJ • Loja Shopping Downtown Barra",
        "message": (
            "🍫🐰 Páscoa mágica na Serra Gaúcha com Voo Direto saindo do Rio de Janeiro!\n\n"
            "✈️ Aéreo Ida e Volta + 🏨 6 dias / 5 noites no Hotel Vista do Vale\n"
            "☕ Café da Manhã + 🚐 Traslado + 🎟️ Passeio Incluso\n"
            "📅 Período: 25 a 30 de Março de 2027\n\n"
            "💰 A partir de 10x de R$ 214,99 sem juros (ou R$ 2.149,92 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Clique e garanta pelo WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1RdMMHqo8uLIm5ceB_dz_ckF8aVJk6PLq",
        "filename": "rumos_madri_espanha_Feed_1080x1350.png",
        "name": "AD 06 - Madri Espanha - 4:5",
        "headline": "Madri, Espanha (7 Dias c/ Bagagem): 10x R$ 866,76!",
        "description": "Embarque RJ • Loja Shopping Downtown Barra",
        "message": (
            "🇪🇸 Realize sua viagem para Madri com 10% OFF em Voo + Hotel!\n\n"
            "✈️ Aéreo Ida e Volta saindo do RJ + 🧳 Bagagem Inclusa\n"
            "🏨 7 dias / 6 noites no B&B Hotel Madrid Vallecas La Gavia\n"
            "☕ Café da Manhã + 🛡️ Seguro Viagem\n"
            "📅 Período: 19 a 25 de Fevereiro de 2027\n\n"
            "💰 A partir de 10x de R$ 866,76 sem juros (ou R$ 8.667,61 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Fale com nossos especialistas no WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1x2OhBBTcquuDKUA9-u36qZ_PAWi15jUC",
        "filename": "rumos_macei__Feed_1080x1350.png",
        "name": "AD 07 - Maceió 8 Dias (Acqua Inn) - 4:5",
        "headline": "Maceió 8 Dias Completo: 10x R$ 369,83 sem juros!",
        "description": "Embarque RJ • Loja Shopping Downtown Barra",
        "message": (
            "🌴 8 Dias em Maceió com Passeios e Traslado inclusos!\n\n"
            "✈️ Aéreo Ida e Volta saindo do RJ\n"
            "🏨 8 dias / 7 noites no Acqua Inn + ☕ Café da Manhã\n"
            "🚐 Traslado Ida e Volta + 🎟️ City Tour + Praia do Francês + 1 Passeio à escolha\n"
            "📅 Período: 09 a 16 de Maio de 2027\n\n"
            "💰 A partir de 10x de R$ 369,83 sem juros (ou R$ 3.698,28 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Chame no WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1lXk_2uxlezPSABlKWXlqP9G_7CNAngtN",
        "filename": "rumos_orlando_Feed_1080x1350.png",
        "name": "AD 08 - Orlando 10 Dias c/ Ingressos - 4:5",
        "headline": "Orlando 10 Dias + Disney e Universal: 10x R$ 1.198!",
        "description": "Embarque RJ • Loja Shopping Downtown Barra",
        "message": (
            "🏰✨ Viva o seu Magic Moment em Orlando com Ingressos Disney e Universal inclusos!\n\n"
            "✈️ Aéreo Ida e Volta saindo do RJ + 🧳 Bagagem Inclusa\n"
            "🏨 10 dias / 9 noites no Magic Moment Resort & Kids Club (4★)\n"
            "☕ Café da Manhã + 🛡️ Seguro Viagem\n"
            "🎟️ 1 dia Disney + 1 dia Universal inclusos!\n"
            "📅 Período: 06 a 15 de Abril de 2027\n\n"
            "💰 A partir de 10x de R$ 1.198,03 sem juros (ou R$ 11.980,34 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Fale no WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1kd_nxS5AEid39JAQtYYZJtw2WbX66Gbz",
        "filename": "rumos_lima_cusco_vale_sagr_e_machu_picchu_Feed_1080x1350.png",
        "name": "AD 09 - Peru Clássico e Machu Picchu - 4:5",
        "headline": "Lima, Cusco e Machu Picchu (7 Dias): 10x R$ 1.078!",
        "description": "Embarque RJ • Loja Shopping Downtown Barra",
        "message": (
            "🦙🏔️ Expedição Peru Clássico: Lima, Cusco, Vale Sagrado e Machu Picchu!\n\n"
            "✈️ Aéreo Ida e Volta saindo do RJ\n"
            "🏨 7 dias / 6 noites em Hotéis selecionados no roteiro\n"
            "☕ Café da Manhã + 🚐 Traslados + 🎟️ Passeios + 🛡️ Seguro Viagem\n"
            "📅 Período: 12 a 18 de Março de 2027\n\n"
            "💰 A partir de 10x de R$ 1.078,56 sem juros (ou R$ 10.785,59 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Chame no WhatsApp (21) 99906-1999!"
        )
    },
    {
        "drive_id": "1NbTWI0SAfpgfXoqa-szyQ3pfkn4lbKBP",
        "filename": "rumos_porto_de_galinhas_Feed_1080x1350 (1).png",
        "name": "AD 10 - Porto de Galinhas (Tabaobi Smart) - 4:5",
        "headline": "Porto de Galinhas (6 Dias): 10x R$ 218,86 sem juros!",
        "description": "Voo Direto • Loja Shopping Downtown Barra",
        "message": (
            "☀️ 6 Dias em Porto de Galinhas com Voo, Hospedagem e Traslado!\n\n"
            "✈️ Aéreo Ida e Volta + 🏨 Tabaobi Smart Hotel\n"
            "☕ Café da Manhã + 🚐 Traslado Ida e Volta\n"
            "📅 Período: 13 a 18 de Maio de 2027\n\n"
            "💰 A partir de 10x de R$ 218,86 sem juros (ou R$ 2.188,60 à vista)\n\n"
            "📍 Loja no Shopping Downtown Barra (RJ) • Reserve pelo WhatsApp (21) 99906-1999!"
        )
    }
]

def upload_image_to_meta(image_path, account_id, token):
    import base64
    with open(image_path, "rb") as f:
        b64_bytes = base64.b64encode(f.read()).decode("ascii")
    url = f"{GRAPH_BASE_URL}/{account_id}/adimages"
    data = urllib.parse.urlencode({
        "access_token": token,
        "bytes": b64_bytes,
        "name": os.path.basename(image_path)
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        images = res.get("images", {})
        for _, info in images.items():
            return info["hash"]
    raise RuntimeError(f"Falha ao obter image_hash: {res}")

def create_ad_creative(item, image_hash, account_id, page_id, ig_id, token):
    url = f"{GRAPH_BASE_URL}/{account_id}/adcreatives"
    link_data = {
        "image_hash": image_hash,
        "link": WHATSAPP_URL,
        "message": item["message"],
        "name": item["headline"],
        "description": item["description"],
        "call_to_action": {
            "type": "WHATSAPP_MESSAGE",
            "value": {"link": WHATSAPP_URL}
        }
    }
    object_story_spec = {
        "page_id": page_id,
        "link_data": link_data
    }
    if ig_id:
        object_story_spec["instagram_actor_id"] = ig_id

    payload = {
        "access_token": token,
        "name": f"Creative - {item['name']}",
        "object_story_spec": json.dumps(object_story_spec)
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["id"]

def create_ad(item, creative_id, adset_id, account_id, status, token):
    url = f"{GRAPH_BASE_URL}/{account_id}/ads"
    payload = {
        "access_token": token,
        "name": item["name"],
        "adset_id": adset_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": status
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["id"]

def main():
    if not ACCESS_TOKEN or not AD_ACCOUNT_ID or not ADSET_ID or not PAGE_ID:
        print("⚠️ Configure META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_ADSET_ID e META_PAGE_ID (ou meta_config.json).")
        sys.exit(1)

    acct = AD_ACCOUNT_ID if AD_ACCOUNT_ID.startswith("act_") else f"act_{AD_ACCOUNT_ID}"
    img_dir = os.environ.get("LAMINAS_DIR", "/tmp/laminas_rumos")

    print(f"🚀 Iniciando publicação das 10 lâminas na conta {acct} (AdSet: {ADSET_ID})...")
    for idx, item in enumerate(LAMINAS, 1):
        local_path = os.path.join(img_dir, item["filename"])
        if not os.path.exists(local_path):
            print(f"[{idx}/10] Baixando {item['filename']} do Google Drive ({item['drive_id']})...")
            os.system(f'gdrive readonly download {item["drive_id"]} --out "{local_path}"')

        print(f"[{idx}/10] Subindo imagem: {item['name']}...")
        img_hash = upload_image_to_meta(local_path, acct, ACCESS_TOKEN)
        print(f"   ✔ image_hash: {img_hash}")

        creative_id = create_ad_creative(item, img_hash, acct, PAGE_ID, INSTAGRAM_ACTOR_ID, ACCESS_TOKEN)
        print(f"   ✔ creative_id: {creative_id}")

        ad_id = create_ad(item, creative_id, ADSET_ID, acct, AD_STATUS, ACCESS_TOKEN)
        print(f"   🎉 Anúncio publicado com sucesso! ad_id: {ad_id}")

if __name__ == "__main__":
    main()
