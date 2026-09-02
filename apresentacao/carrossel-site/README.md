# Carrossel de apresentação — Studio G85

Carrossel de 15 slides (1080×1350px, 4:5) apresentando o site www.studiog85.com.
Todas as imagens são screenshots reais das páginas, capturadas em 1440×900 (desktop),
834×1112 (tablet) e 390×844 (mobile).

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `carrossel-studio-g85.html` | Prévia navegável (arraste ou use as setas). Abra no navegador. |
| `slides/slide_01.png` … `slide_15.png` | Slides prontos para publicar, 1080×1350px. |
| `_fonte/shot2.py` | Captura os screenshots do site servido em `localhost:8099`. |
| `_fonte/build.py` | Monta o HTML do carrossel com as imagens embutidas em base64. |
| `_fonte/export.py` | Exporta cada slide como PNG 1080×1350. |

## Ordem dos slides

1. Capa — hook e mockup da home
2. O projeto — números do build
3. Fontes & cores — Montserrat, Inter, Dancing Script + paleta
4. Home · abertura
5. Home · sobre e serviços
6. Home · processo, galeria e vídeos
7. Home · perfil e avaliações
8. Home · estrutura, dúvidas e contato
9. Página de vitrificação cerâmica
10. Página de PPF
11. Página de película Window Blue
12. Página de lavagem técnica
13. Páginas de apoio (privacidade e 404) + bastidores
14. Responsivo — desktop, tablet e celular
15. CTA

## Como regerar

```bash
python3 -m http.server 8099          # na raiz do repositório
python3 _fonte/shot2.py              # screenshots
python3 _fonte/build.py              # monta o HTML
python3 _fonte/export.py slides      # exporta os PNGs
```

Os scripts usam caminhos absolutos do ambiente onde foram gerados — ajuste as
constantes do topo de cada arquivo antes de rodar em outra máquina.

## Atenção

Esta pasta é material de divulgação, não faz parte do site publicado. Se ela for
para a branch `main`, o GitHub Pages passa a servir os PNGs em
`www.studiog85.com/apresentacao/`. Para evitar isso, mantenha a pasta só nesta
branch ou mova para fora do repositório antes do merge.
