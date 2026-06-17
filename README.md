# 🛍️ Gerador de Ofertas WhatsApp

Ferramenta desktop para transformar textos de compartilhamento da Shopee em prompts formatados prontos para enviar no WhatsApp — com um clique abre direto no **WhatsApp Web** com a mensagem já preenchida.

![Preview da aplicação](comparador_figurinhas.png)

---

## ✨ Funcionalidades

- Cola o texto copiado direto da Shopee e gera o prompt automaticamente
- Detecta emoji temático com base no nome do produto
- Gera descrição curta e natural automaticamente
- Formata título em MAIÚSCULO com padrão negrito WhatsApp (`* *`)
- **📋 Copiar Texto** — copia o resultado para a área de transferência
- **💬 Enviar pelo WhatsApp Web** — abre o WhatsApp Web no navegador com a mensagem já preenchida
- Interface escura moderna com barra de status em tempo real

---

## 🖥️ Pré-requisitos

- Python 3.8 ou superior
- pip

---

## 📦 Instalação

**1. Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/gerador-ofertas-whatsapp.git
cd gerador-ofertas-whatsapp
```

**2. Instale a dependência:**

```bash
pip install pyperclip
```

> `tkinter` e `webbrowser` já vêm incluídos na instalação padrão do Python.

---

## ▶️ Como executar

```bash
python gerador_ofertas_whatsapp_gui.py
```

---

## 📖 Como usar

1. Abra o produto na Shopee e toque em **Compartilhar**
2. Copie o texto gerado pela Shopee
3. Cole no campo de entrada da janela
4. Clique em **⚡ Gerar Prompt**
5. Escolha uma das opções:

| Botão | Ação |
|---|---|
| 📋 **Copiar Texto** | Copia para a área de transferência |
| 💬 **Enviar pelo WhatsApp Web** | Abre o navegador com a mensagem já preenchida |

---

## 📋 Formato de entrada esperado
