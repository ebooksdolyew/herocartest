# Studio G85 — site institucional

Site estático (HTML + CSS + JS, sem build) do **Studio G85 — Estética e Proteção
Automotiva**, Fortaleza/CE.

Domínio de produção: **https://www.studiog85.com/**

---

## Estrutura

```
index.html                      Home (uma página, com seções âncora)
404.html                        Página de erro
politica-de-privacidade.html    LGPD + cookies
servicos/
  vitrificacao-ceramica.html    Página de serviço com SEO próprio
  ppf-paint-protection-film.html
  pelicula-window-blue.html
  lavagem-tecnica.html
assets/
  css/site.css                  Folha compartilhada (páginas internas, banner, formulário)
  js/g85.js                     Medição, consentimento, formulário de lead, lazy load
  galeria/                      Imagens WebP + favicon + imagem de compartilhamento
  videos/                       WebM (leve) + MP4 (compatível) de cada vídeo
robots.txt  sitemap.xml  CNAME  _redirects
```

Cada página tem `<title>`, meta description, canonical, Open Graph, Twitter Card
e dados estruturados JSON-LD próprios.

---

## 1. Ativar GA4 e Meta Pixel  ⚠️ pendente

Enquanto os IDs forem os valores de exemplo, **nada é carregado**: nenhum script
de terceiro é baixado e nenhum cookie de rastreamento é gravado. Para ativar,
abra `assets/js/g85.js` e troque as duas linhas do topo:

```js
var CFG = {
  ga4:   'G-XXXXXXXXXX',      // ID de medição do GA4
  pixel: '000000000000000',   // ID do Meta Pixel
```

- **GA4** → analytics.google.com › Admin › Fluxos de dados › ID de medição (`G-…`)
- **Meta Pixel** → business.facebook.com › Gerenciador de Eventos › ID do pixel

### Eventos já instrumentados

| Evento              | Quando dispara                                        | Meta          |
|---------------------|-------------------------------------------------------|---------------|
| `clique_whatsapp`   | qualquer link `wa.me` (com o parâmetro `origem`, que diz de qual seção partiu) | `Lead`   |
| `clique_telefone`   | links `tel:`                                          | —             |
| `clique_instagram`  | link do Instagram                                     | —             |
| `clique_rota`       | link do Google Maps                                   | —             |
| `form_iniciado`     | primeiro caractere digitado no formulário             | —             |
| `gerar_lead`        | envio válido do formulário                            | `Lead`        |
| `rolagem`           | 25 / 50 / 75 / 100 % da página                        | —             |

Todos entram também no `dataLayer`, então funcionam via GTM sem alteração de código.
No GA4, marque `gerar_lead` e `clique_whatsapp` como **conversões**.

---

## 2. Consentimento (LGPD)

O banner aparece na primeira visita, em todas as páginas. Ele usa **Consent Mode v2**:
tudo negado por padrão; GA4 e Pixel só são baixados após o clique em "Aceitar".
A escolha fica no `localStorage` do visitante e pode ser revista pelo botão
"Revisar minha escolha de cookies" na política de privacidade.

---

## 3. Formulário de orçamento

Está na home (`#orcamento`) e no final de cada página de serviço. Sem backend:
valida os campos, dispara `gerar_lead` e abre o WhatsApp com a mensagem já montada
(nome, telefone, veículo, serviço e observação). Nas páginas de serviço, o campo
"serviço de interesse" já vem pré-selecionado.

Para migrar para captura em servidor depois (e-mail ou banco), o ponto de troca é
a função `ligarFormulario()` em `assets/js/g85.js`.

---

## 4. Deploy

### GitHub Pages
1. Settings › Pages › Source: **Deploy from a branch**, branch `main`, pasta `/ (root)`.
2. Custom domain: `www.studiog85.com` (o arquivo `CNAME` na raiz já tem esse valor).
3. Marque **Enforce HTTPS** depois que o certificado for emitido.

### DNS no registrador do domínio
| Tipo  | Nome | Valor |
|-------|------|-------|
| CNAME | `www` | `<usuario>.github.io` |
| A     | `@`   | `185.199.108.153` |
| A     | `@`   | `185.199.109.153` |
| A     | `@`   | `185.199.110.153` |
| A     | `@`   | `185.199.111.153` |

Os registros A no apex fazem `studiog85.com` redirecionar para `www.studiog85.com`,
que é o host canônico usado em todas as tags `canonical` e no sitemap.

### Netlify / Cloudflare Pages
Publique a raiz do repositório. O arquivo `_redirects` já cobre o host canônico,
as URLs curtas (`/ppf`, `/vitrificacao`, `/pelicula`, `/lavagem`…) e o fallback 404.
No GitHub Pages esses redirects não são lidos — lá o apex → www é resolvido pelo DNS.

---

## 5. Depois de publicar

- [ ] Google Search Console: adicionar a propriedade e enviar `https://www.studiog85.com/sitemap.xml`
- [ ] Teste de Resultados Aprimorados do Google (schema de LocalBusiness, Review e FAQ)
- [ ] Facebook Sharing Debugger e validador de cards do X (imagem de compartilhamento)
- [ ] PageSpeed Insights em mobile
- [ ] Google Business Profile apontando para o site
- [ ] Confirmar o **número de WhatsApp** (ver abaixo)

### ⚠️ Número de WhatsApp

Os links do site usam `wa.me/558598484104` — isso são **8 dígitos** depois do DDD 85.
Celular no Ceará tem 9 dígitos e começa com 9, então o número correto provavelmente é
`5585998484104` (85 99848-4104). Confirme com o Studio e, se for o caso, troque em
todos os arquivos de uma vez:

```bash
grep -rl '558598484104' . --include='*.html' --include='*.js' \
  | xargs sed -i 's/558598484104/5585998484104/g'
sed -i 's/(85) 9848-4104/(85) 99848-4104/g' index.html politica-de-privacidade.html
```
