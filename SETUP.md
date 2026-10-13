# Perfil GitHub da Onyx Labs — guia de manutenção

Adaptado do template "Animated GitHub Profile" (retrato ASCII + painel neofetch +
gráfico de contribuições). Na versão da Onyx Labs, o retrato virou a **gema
hexagonal da marca em ASCII** e o gráfico soma as contribuições da **equipe**.

## Como funciona

O GitHub remove `<script>` dos READMEs, mas **executa animações SMIL/CSS dentro
de SVGs** carregados como `<img>`. Toda a animação mora em SVGs do próprio
repositório, então nada quebra por limite de requisições de serviços externos.

| Arquivo | O que é | Gerado por |
| --- | --- | --- |
| `logo-ascii.svg` | Gema + "ONYX LABS" em ASCII, que se digita como num terminal | `make_logo_source.py` → `make_ascii_svg.py` |
| `info-card.svg` | Painel estilo neofetch (quem somos, serviços, stack) | `make_info_card.py` |
| `contrib-heatmap.svg` | Gráfico de contribuições da equipe (preto → branco) | `fetch_contributions.py` → `render_heatmap_svg.py` |
| `data/contributions.json` | Dados brutos + sequências | `fetch_contributions.py` |
| `.github/workflows/update-profile-art.yml` | Atualiza o gráfico todo dia, sem token | GitHub Actions |

## Publicar (primeira vez)

1. Entre no GitHub com a conta **OnyxLabsNG**.
2. Crie um repositório **público** chamado exatamente **`OnyxLabsNG`**, sem README
   (o GitHub mostra o aviso "special repository").
3. Nesta pasta:
   ```bash
   git init -b main
   git add .
   git commit -m "feat: perfil animado da Onyx Labs"
   git remote add origin https://github.com/OnyxLabsNG/OnyxLabsNG.git
   git push -u origin main
   ```
4. **Settings → Actions → General → Workflow permissions → Read and write
   permissions** → Save.
5. **Actions → "Atualizar arte do perfil" → Run workflow** (uma vez). Depois disso
   ele roda sozinho todo dia.

## Editar depois

```bash
pip install -r requirements-local.txt -r scripts/requirements.txt

# painel (quem somos / serviços / stack): edite ROWS e HOST no topo do script
python scripts/make_info_card.py

# logo ASCII com o logo oficial (PNG prata sobre preto)
python scripts/make_logo_source.py caminho/logo.png
python scripts/make_ascii_svg.py

# prévia sem animação (mostra o quadro final)
STATIC=1 python scripts/make_ascii_svg.py source-logo.png preview.svg

# gráfico manual (o workflow já faz isso todo dia)
GH_PROFILE_USERS="OnyxLabsNG,Stucaluc" python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

No Windows (PowerShell), troque `STATIC=1 python ...` por
`$env:STATIC=1; python ...` e `GH_PROFILE_USERS=...` por
`$env:GH_PROFILE_USERS="OnyxLabsNG,Stucaluc"; python ...`.

## Ajustes rápidos

| Quero… | Onde |
| --- | --- |
| Adicionar os sócios ao gráfico | `GH_PROFILE_USERS` no workflow (separados por vírgula) |
| Mudar textos do painel | `ROWS` em `scripts/make_info_card.py` |
| Facetas mais/menos marcadas | `FACET_BRIGHTNESS`, `EDGE`, `GRADIENT` em `make_logo_source.py` |
| Digitar mais rápido/devagar | `ROW_DUR`, `STAGGER` em `make_ascii_svg.py` |
| Cores do gráfico | `PALETTE` em `render_heatmap_svg.py` |
| Painel ficou mais alto | aumente `H` e recalcule as larguras no `README.md` |

**Recalcular larguras** (mesma altura lado a lado, total 860 px):
`w_logo = 860 × (H/480) ÷ (875/840 + H/480)` e `w_painel = 860 − w_logo`.
Com `H = 432`: 399 e 461.

## Observações

- O gráfico usa a página pública de contribuições de cada conta. Contribuições
  em repositórios **privados** só entram se a pessoa ativar *"Include private
  contributions on my profile"* nas configurações do perfil.
- Os commits do workflow são feitos pelo bot do GitHub Actions e **não** contam
  como contribuição da conta.
- Se o GitHub mudar o HTML da página de contribuições, o `fetch_contributions.py`
  falha com "no calendar cells found". O README continua mostrando o último
  gráfico gerado.
