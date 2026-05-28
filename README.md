<div align="center">

# 🎱 Lotofácil IA

**Gerador inteligente de jogos da Lotofácil com rede neural embarcada no navegador.**

[![TensorFlow.js](https://img.shields.io/badge/TensorFlow.js-4.22.0-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/js)
[![Keras](https://img.shields.io/badge/Keras-3.13.2-D00000?logo=keras&logoColor=white)](https://keras.io)
[![PWA](https://img.shields.io/badge/PWA-Offline%20Ready-5A0FC8?logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/Licença-MIT-green.svg)](LICENSE)

<img src="favicon.svg" width="80" alt="Lotofácil IA Logo"/>

---

*Aplicação web que utiliza uma rede neural treinada com histórico real de sorteios para sugerir combinações estatisticamente fundamentadas.*

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Como Funciona](#-como-funciona)
- [Arquitetura do Modelo](#-arquitetura-do-modelo)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)
- [Instalação e Uso](#-instalação-e-uso)
- [Funcionalidades](#-funcionalidades)
- [Stack Tecnológica](#-stack-tecnológica)
- [Utilitários](#-utilitários)

---

## 🎯 Sobre o Projeto

O **Lotofácil IA** é um PWA (Progressive Web App) que roda 100% no navegador — sem backend, sem API paga, sem dependências externas em tempo de execução. O modelo de deep learning é carregado localmente via TensorFlow.js e faz inferência diretamente no dispositivo do usuário.

A proposta é oferecer sugestões de jogos baseadas em padrões estatísticos extraídos do histórico oficial de sorteios da Caixa Econômica Federal.

> ⚠️ **Aviso:** Este projeto é experimental e educacional. Loterias são eventos aleatórios — nenhum modelo matemático garante acertos.

---

## 🧠 Como Funciona

```
┌─────────────────────────────────────────────────────┐
│  1. Entrada: 15 dezenas do último sorteio           │
│     (automático via API da Caixa ou manual)         │
├─────────────────────────────────────────────────────┤
│  2. Normalização: cada dezena → (x-1) / 24.0       │
│     Mapeia o intervalo [1,25] para [0,1]            │
├─────────────────────────────────────────────────────┤
│  3. Inferência: rede neural gera 25 probabilidades  │
│     Uma para cada dezena possível                   │
├─────────────────────────────────────────────────────┤
│  4. Seleção: top 15 probabilidades → jogo sugerido  │
│     Com ruído paramétrico (±4%) para variedade      │
└─────────────────────────────────────────────────────┘
```

---

## 🏗 Arquitetura do Modelo

Rede neural sequencial com 7 camadas densas, normalização em lote e regularização por dropout:

| Camada | Tipo | Neurônios | Ativação |
|--------|------|-----------|----------|
| 1 | Dense | 128 | tanh |
| 2 | Dense | 256 | ReLU |
| 3 | Dropout | — | rate=0.5 |
| 4 | Dense + BatchNorm | 128 | ReLU |
| 5 | Dense + BatchNorm | 64 | ReLU |
| 6 | Dense | 32 | LeakyReLU (α=0.1) |
| 7 | Dense + BatchNorm | 16 | tanh |
| Saída | Dense | 25 | sigmoid |

- **Entrada:** vetor de 15 valores normalizados (último sorteio)
- **Saída:** 25 probabilidades (uma por dezena)
- **Otimizador:** Adam (lr=0.000125)
- **Loss:** Binary Crossentropy

---

## 📁 Estrutura de Arquivos

```
lotofacil/
├── index.html              # Aplicação principal (HTML + CSS + JS)
├── model.json              # Topologia e configuração da rede neural
├── group1-shard1of1.bin    # Pesos treinados do modelo (binário)
├── favicon.svg             # Ícone da aplicação
├── vacina.py               # Utilitário de compatibilidade Keras 3 → TFJS
└── README.md               # Este arquivo
```

| Arquivo | Propósito |
|---------|-----------|
| `index.html` | Interface completa do PWA — grid interativo, tema claro/escuro, geração de jogos |
| `model.json` | Descrição da arquitetura + manifesto dos pesos para o TensorFlow.js |
| `group1-shard1of1.bin` | Arquivo binário com os ~320KB de pesos treinados |
| `vacina.py` | Script de pós-processamento que corrige incompatibilidades do Keras 3 |

---

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.x (para o servidor local) **ou** Node.js

### Executando

```bash
# Clone o repositório
git clone <url-do-repo>
cd lotofacil

# Inicie um servidor HTTP local (necessário para o fetch do modelo)
python -m http.server 8000

# Ou com Node.js:
npx serve .
```

Acesse **http://localhost:8000** no navegador.

> 💡 **Por que precisa de servidor?** O TensorFlow.js usa `fetch()` para carregar o modelo. Navegadores bloqueiam fetch em protocolo `file://` por segurança (CORS).

### Uso da Aplicação

1. As 15 dezenas do último sorteio são preenchidas automaticamente (se houver internet)
2. Caso contrário, selecione manualmente as 15 dezenas no grid
3. Escolha a quantidade de jogos desejada (1–10)
4. Clique em **Gerar Jogos**
5. Os jogos sugeridos aparecem abaixo com scroll suave

---

## ✨ Funcionalidades

- 🌙 **Tema escuro/claro** — alternância com persistência visual
- 📡 **Sincronização automática** — busca o último sorteio via API da Caixa
- 🔌 **Modo offline** — funciona sem internet após primeiro carregamento
- 🎲 **Múltiplos jogos** — gera até 10 combinações diferentes por vez
- 🧮 **Inferência local** — nenhum dado sai do dispositivo do usuário
- 📱 **Responsivo** — otimizado para mobile (max-width 500px)

---

## 🛠 Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| **TensorFlow.js 4.22.0** | Inferência do modelo no browser |
| **Keras 3.13.2** | Treinamento original do modelo |
| **HTML/CSS/JS** | Interface sem frameworks (vanilla) |
| **API Caixa** | Dados do último sorteio (via proxy AllOrigins) |

---

## 🔧 Utilitários

### `vacina.py` — Correção de Compatibilidade

O Keras 3 exporta modelos com uma estrutura de `DTypePolicy` que o TensorFlow.js não reconhece nativamente. Este script converte:

```python
# Antes (Keras 3):
"dtype": {"class_name": "DTypePolicy", "config": {"name": "float32"}}

# Depois (compatível com TFJS):
"dtype": "float32"
```

**Quando usar:** sempre que re-treinar e re-exportar o modelo com Keras 3.

```bash
python vacina.py
```

---

<div align="center">

Feito com 🧠 e ☕ — *Que a estatística esteja ao seu favor.*

</div>
