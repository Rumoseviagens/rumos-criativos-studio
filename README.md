# 🎨 Rumos Creative Studio — Guia de Integração (`rumos_studio_frontend.js` / `chat.rumosrj.com`)

Este repositório contém o **Estúdio Interativo de Lâminas (Feed 4:5 `1080x1350` + TV Vitrine 16:9 `1920x1080`)** das agências **Azul Viagens Barra** e **Rumos e Viagens**, com todos os logos e ativos oficiais já embutidos em base64 (`index.html`).

## 📂 Arquivos no Repositório
- `index.html`: Aplicação completa auto-contida (HTML + Canvas + JS + Logos em Base64 + API `postMessage` e Query Params).
- `assets_b64.json`: Todos os logos exatos (`logo_azul_barra_exact`, `logo_azul_barra_exact_dark`, `logo_rumos_horiz_green`, `logo_rumos_horiz_gold`, etc.) e selos em base64.

## 🔌 Como integrar no `rumos_studio_frontend.js` (`openSlideGeneratorModal`)

Você pode:
1. Servir o `index.html` em uma rota estática da VPS (ex: `/estudio-criativos/index.html`) e abri-lo dentro do modal `openSlideGeneratorModal` via `<iframe id="rumosCreativeIframe" src="/estudio-criativos/index.html"></iframe>`, **OU** portar as funções de renderização (`renderLayout3`, `renderLayout1`, `renderLayoutTV`, `PALETTES`, `ASSETS`) diretamente para dentro do `openSlideGeneratorModal` no `rumos_studio_frontend.js`.

### Enviando os dados do orçamento automaticamente para o Estúdio via `postMessage`:
```javascript
const iframe = document.getElementById("rumosCreativeIframe");
iframe.onload = () => {
  iframe.contentWindow.postMessage({
    type: "RUMOS_LOAD_ORCAMENTO",
    payload: {
      agency: "azul", // "azul" (Azul Viagens Barra) ou "rumos" (Rumos e Viagens)
      layout: "3",    // "3" (Feed 4:5 Alta Conversão), "1" (Feed 4:5 Foto Ampla), "tv" (TV Vitrine 16:9 1920x1080)
      destino: "PRAIA DO FORTE, BAHIA",
      subtitulo: "RESORT ALL INCLUSIVE",
      hotel: "Iberostar Waves Bahia",
      estrelas: 5,
      dias: "5 dias / 4 noites",
      periodo: "23 a 27 de Agosto de 2026",
      parcelas: "10x",
      valorInt: "434",
      valorDec: ",15",
      valorVista: "4.341,50",
      pagamento: "Em até 21x no Cartão Azul Itaú",
      condicao: "Taxas inclusas • Preço por pessoa em apto duplo",
      inclusos: ["aereo", "hotel", "allinclusive", "traslado"],
      seloRedondo: "all_inclusive", // "voo_direto", "all_inclusive", "cafe_manha", "meia_pensao", "completo", "custom", "none"
      seloPromo: "oferta",          // "oferta", "ultimas", "ferias", "feriado", "black", "custom", "none"
      fotoPrincipal: "https://...", // opcional
      fotoRedonda: "https://..."    // opcional
    }
  }, "*");
};
```
