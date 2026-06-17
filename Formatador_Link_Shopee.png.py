
import tkinter as tk
from tkinter import messagebox
import re
import pyperclip
import urllib.parse
import webbrowser

EMOJIS_TEMATICOS = {
    "faqueiro": "🍴", "talheres": "🍴", "panela": "🍳", "frigideira": "🍳",
    "fritadeira": "🍟", "liquidificador": "🥤", "cafeteira": "☕",
    "tênis": "👟", "sapato": "👟", "sandália": "👡", "bota": "👢",
    "camiseta": "👕", "roupa": "👕", "calça": "👖", "vestido": "👗",
    "bolsa": "👜", "mochila": "🎒", "relógio": "⌚",
    "celular": "📱", "smartphone": "📱", "notebook": "💻", "fone": "🎧",
    "perfume": "🌸", "skincare": "✨", "creme": "🧴", "shampoo": "🧴",
    "suplemento": "💪", "proteína": "💪", "whey": "💪", "vitamina": "💊",
    "colágeno": "💊", "sofá": "🛋️", "cama": "🛏️", "travesseiro": "🛏️",
    "bicicleta": "🚴", "livro": "📚", "brinquedo": "🧸", "jogo": "🎮",
}

def detectar_emoji(nome: str) -> str:
    nome_lower = nome.lower()
    for chave, emoji in EMOJIS_TEMATICOS.items():
        if chave in nome_lower:
            return emoji
    return "🛍️"

def parsear_e_gerar_prompt(texto_original: str):
    match_nome  = re.search(r"(?:Dê uma olhada em|olhada em)\s+(.+?)\s+por\s+R\$", texto_original, re.IGNORECASE)
    match_preco = re.search(r"por\s+R\$\s*([\d.,]+)", texto_original, re.IGNORECASE)
    match_link  = re.search(r"(https?://\S+)", texto_original)

    if not match_nome or not match_preco or not match_link:
        return None, "❌ Não foi possível identificar o produto, preço ou link no texto."

    nome_produto = match_nome.group(1).strip()
    preco        = match_preco.group(1).strip()
    link         = re.sub(r"[\)\]\(>]+$", "", match_link.group(1).strip())
    emoji        = detectar_emoji(nome_produto)
    descricao    = f"{nome_produto}, perfeito para o seu dia a dia com qualidade e praticidade"

    prompt = (
        f"*{nome_produto.upper()} {emoji}✨*\n"
        f"> {descricao}\n"
        f"\n"
        f"Por *R${preco}* 😍💥\n"
        f"Compre aqui ✅👇\n"
        f"{link}\n"
        f"\n"
        f"*Essa oferta pode acabar a qualquer momento 🏃🏻\u200d♀️🏃🏻\u200d♀️*"
    )
    return prompt, None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Ofertas WhatsApp 🛍️")
        self.geometry("700x650")
        self.resizable(True, True)
        self.configure(bg="#1e1e2e")
        self._build_ui()

    def _build_ui(self):
        FONT_LABEL = ("Segoe UI", 10)
        FONT_TEXT  = ("Consolas", 10)
        BG         = "#1e1e2e"
        CARD       = "#2a2a3d"
        ACCENT     = "#7c3aed"
        ACCENT_D   = "#5b21b6"
        FG         = "#e2e8f0"
        GREEN      = "#22c55e"
        GREEN_D    = "#16a34a"
        WHATS      = "#25D366"
        WHATS_D    = "#128C7E"

        # Header
        header = tk.Frame(self, bg=ACCENT, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🛍️  Gerador de Ofertas WhatsApp",
                 font=("Segoe UI", 15, "bold"), bg=ACCENT, fg="white").pack()

        body = tk.Frame(self, bg=BG, padx=20, pady=15)
        body.pack(fill="both", expand=True)

        # Entrada
        tk.Label(body, text="Cole o texto da Shopee / Mercado Livre abaixo:",
                 font=FONT_LABEL, bg=BG, fg=FG).pack(anchor="w", pady=(0, 4))

        self.txt_entrada = tk.Text(body, height=6, font=FONT_TEXT,
                                   bg=CARD, fg=FG, insertbackground=FG,
                                   relief="flat", bd=0, padx=10, pady=8, wrap="word")
        self.txt_entrada.pack(fill="x", pady=(0, 4))

        PLACEHOLDER = "Ex: Dê uma olhada em Faqueiro Tramontina 24 Peças por R$55,06. Compre na Shopee agora! https://s.shopee.com.br/xxx"
        self.txt_entrada.insert("1.0", PLACEHOLDER)
        self.txt_entrada.config(fg="#888")

        def on_focus_in(e):
            if self.txt_entrada.get("1.0", "end-1c") == PLACEHOLDER:
                self.txt_entrada.delete("1.0", "end")
                self.txt_entrada.config(fg=FG)

        def on_focus_out(e):
            if not self.txt_entrada.get("1.0", "end-1c").strip():
                self.txt_entrada.insert("1.0", PLACEHOLDER)
                self.txt_entrada.config(fg="#888")

        self.txt_entrada.bind("<FocusIn>", on_focus_in)
        self.txt_entrada.bind("<FocusOut>", on_focus_out)

        # Botões superiores
        btn_row1 = tk.Frame(body, bg=BG)
        btn_row1.pack(fill="x", pady=8)

        tk.Button(btn_row1, text="⚡  Gerar Prompt",
                  font=("Segoe UI", 11, "bold"),
                  bg=ACCENT, fg="white", activebackground=ACCENT_D,
                  activeforeground="white", relief="flat",
                  padx=20, pady=8, cursor="hand2",
                  command=self.gerar).pack(side="left")

        tk.Button(btn_row1, text="🗑️  Limpar",
                  font=("Segoe UI", 10),
                  bg=CARD, fg=FG, activebackground="#3a3a55",
                  activeforeground=FG, relief="flat",
                  padx=16, pady=8, cursor="hand2",
                  command=self.limpar).pack(side="left", padx=(8, 0))

        # Saída
        tk.Label(body, text="Resultado formatado:", font=FONT_LABEL, bg=BG, fg=FG)            .pack(anchor="w", pady=(10, 4))

        self.txt_saida = tk.Text(body, height=12, font=FONT_TEXT,
                                 bg=CARD, fg="#a3e635", insertbackground=FG,
                                 relief="flat", bd=0, padx=10, pady=8,
                                 wrap="word", state="disabled")
        self.txt_saida.pack(fill="both", expand=True)

        # ── Botões de ação ──────────────────────────────────────────
        btn_row2 = tk.Frame(body, bg=BG)
        btn_row2.pack(fill="x", pady=(10, 0))

        # Copiar para área de transferência
        self.btn_copiar = tk.Button(btn_row2,
                                    text="📋  Copiar Texto",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=GREEN, fg="white",
                                    activebackground=GREEN_D, activeforeground="white",
                                    relief="flat", padx=16, pady=10,
                                    cursor="hand2", state="disabled",
                                    command=self.copiar)
        self.btn_copiar.pack(side="left", expand=True, fill="x", padx=(0, 6))

        # Abrir WhatsApp Web com mensagem
        self.btn_whats = tk.Button(btn_row2,
                                   text="💬  Enviar pelo WhatsApp Web",
                                   font=("Segoe UI", 10, "bold"),
                                   bg=WHATS, fg="white",
                                   activebackground=WHATS_D, activeforeground="white",
                                   relief="flat", padx=16, pady=10,
                                   cursor="hand2", state="disabled",
                                   command=self.abrir_whatsapp)
        self.btn_whats.pack(side="left", expand=True, fill="x")

        # Status
        self.status_var = tk.StringVar(value="Aguardando texto...")
        tk.Label(self, textvariable=self.status_var,
                 font=("Segoe UI", 9), bg="#111120", fg="#94a3b8",
                 anchor="w", padx=12).pack(fill="x", side="bottom")

    def gerar(self):
        texto = self.txt_entrada.get("1.0", "end-1c").strip()
        if not texto or texto.startswith("Ex:"):
            messagebox.showwarning("Atenção", "Cole o texto da Shopee no campo de entrada.")
            return

        prompt, erro = parsear_e_gerar_prompt(texto)

        self.txt_saida.config(state="normal")
        self.txt_saida.delete("1.0", "end")

        if erro:
            self.txt_saida.insert("1.0", erro)
            self.btn_copiar.config(state="disabled")
            self.btn_whats.config(state="disabled")
            self.status_var.set("❌ Erro ao processar o texto.")
        else:
            self.txt_saida.insert("1.0", prompt)
            self.btn_copiar.config(state="normal")
            self.btn_whats.config(state="normal")
            self.status_var.set("✅ Prompt gerado com sucesso!")

        self.txt_saida.config(state="disabled")

    def copiar(self):
        conteudo = self.txt_saida.get("1.0", "end-1c")
        try:
            pyperclip.copy(conteudo)
        except Exception:
            self.clipboard_clear()
            self.clipboard_append(conteudo)
        self.status_var.set("📋 Texto copiado para a área de transferência!")

    def abrir_whatsapp(self):
        conteudo = self.txt_saida.get("1.0", "end-1c")
        try:
            pyperclip.copy(conteudo)
        except Exception:
            self.clipboard_clear()
            self.clipboard_append(conteudo)

        texto_encoded = urllib.parse.quote(conteudo)
        url = f"https://web.whatsapp.com/send?text={texto_encoded}"
        webbrowser.open(url)
        self.status_var.set("💬 WhatsApp Web aberto! Texto também copiado para segurança.")

    def limpar(self):
        self.txt_entrada.delete("1.0", "end")
        self.txt_saida.config(state="normal")
        self.txt_saida.delete("1.0", "end")
        self.txt_saida.config(state="disabled")
        self.btn_copiar.config(state="disabled")
        self.btn_whats.config(state="disabled")
        self.status_var.set("🗑️ Campos limpos.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
