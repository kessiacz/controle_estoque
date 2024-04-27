import tkinter as tk
from tkinter import ttk
from tkinter.font import Font as tkfont
from database.database import ControleEstoque
from models.login import Login

class ControleEstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque")
        self.root.geometry("800x400")
        self.root.minsize(800, 400)
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(expand=True, fill='both')
        self.controle_estoque = ControleEstoque()
        self.login = Login(self.controle_estoque)
        self.criar_interface_login()

    def criar_interface_login(self):
        # Criar interface gráfica com tkinter para login
        self.frame_login = tk.Frame(self.frame_principal)  # frame_principal como pai
        self.frame_login.pack(expand=True)

        # Label com o nome do programa
        self.label_titulo = tk.Label(self.frame_login, text="CONTROLE DE ESTOQUE", font=("Helvetica", 16, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Centralizando o conteúdo verticalmente
        self.frame_login.grid_rowconfigure(1, weight=1)
        self.frame_login.grid_rowconfigure(3, weight=1)

        self.label_username = tk.Label(self.frame_login, text="USUÁRIO:", font=("Helvetica", 12))
        self.label_username.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.frame_login, font=("Helvetica", 12))
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)

        self.label_senha = tk.Label(self.frame_login, text="SENHA:", font=("Helvetica", 12))
        self.label_senha.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.senha_entry = tk.Entry(self.frame_login, show="*", font=("Helvetica", 12))
        self.senha_entry.grid(row=3, column=1, padx=5, pady=5)

        self.botao_login = tk.Button(self.frame_login, text="LOGIN", command=self.realizar_login, font=("Helvetica", 12))
        self.botao_login.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="we")

        self.botao_criar_conta = tk.Button(self.frame_login, text="CRIAR CONTA", command=self.criar_conta, font=("Helvetica", 12))
        self.botao_criar_conta.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        self.label_mensagem = tk.Label(self.frame_login, text="", font=("Helvetica", 12), fg="red")
        self.label_mensagem.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def criar_interface_menu(self):
        # Limpar a tela
        self.limpar_tela()

        # Criar interface gráfica com tkinter para o menu principal
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(padx=20, pady=20)

        botoes = [("ENTRADA DE ITEM", self.criar_interface_adicionar),
                  ("SAÍDA DE ITEM", self.criar_interface_saida),
                  ("ATUALIZAR QUANTIDADE", self.criar_interface_atualizar),
                  ("LISTAR ITENS", self.listar_itens),
                  ("HISTÓRICO DE ENTRADA", self.exibir_historico_entrada),
                  ("HISTÓRICO DE SAÍDA", self.exibir_historico_saida)]

        # Adicionar os botões verticalmente
        for i, (texto, comando) in enumerate(botoes):
            botao = tk.Button(self.frame_menu, text=texto, command=comando, font=("Helvetica", 12))
            botao.grid(row=i, column=0, padx=5, pady=5, sticky="we")

        # Centralizar o frame do menu verticalmente
        self.frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def criar_interface_adicionar(self):
        # Limpar a tela
        self.limpar_tela()

        # Criar novo frame para os widgets
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(padx=20, pady=20)

        # Adicionar título
        titulo = tk.Label(self.frame_menu, text="ENTRADA DE ITENS", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Adicionar campos de entrada para o nome do item, a quantidade e o fornecedor
        self.label_nome = tk.Label(self.frame_menu, text="NOME DO ITEM:", font=("Helvetica", 12))
        self.label_nome.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

        self.label_quantidade = tk.Label(self.frame_menu, text="QUANTIDADE:", font=("Helvetica", 12))
        self.label_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.quantidade_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.quantidade_entry.grid(row=2, column=1, padx=5, pady=5)

        self.label_fornecedor = tk.Label(self.frame_menu, text="FORNECEDOR:", font=("Helvetica", 12))
        self.label_fornecedor.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.fornecedor_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.fornecedor_entry.grid(row=3, column=1, padx=5, pady=5)

        # Adicionar botão para confirmar adição do item
        self.botao_confirmar = tk.Button(self.frame_menu, text="CONFIRMAR", command=self.confirmar_adicao, font=("Helvetica", 12))
        self.botao_confirmar.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Adicionar botão para voltar ao menu principal
        self.botao_voltar = tk.Button(self.frame_menu, text="VOLTAR", command=self.criar_interface_menu, font=("Helvetica", 12))
        self.botao_voltar.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Criar widget label_resultado
        self.label_resultado = tk.Label(self.frame_menu, text="", font=("Helvetica", 12))
        self.label_resultado.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Adicionar rastreador de evento para converter entrada em maiúsculas
        self.nome_entry.bind("<KeyRelease>", self.converter_maiusculas)
        self.fornecedor_entry.bind("<KeyRelease>", self.converter_maiusculas)

    def criar_interface_saida(self):
        # Limpar a tela
        self.limpar_tela()

        # Criar novo frame para os widgets
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(padx=20, pady=20)

        # Adicionar título
        titulo = tk.Label(self.frame_menu, text="SAÍDA DE ITENS", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Adicionar campos de entrada para o nome do item, a quantidade e o destinatário
        self.label_nome = tk.Label(self.frame_menu, text="NOME DO ITEM:", font=("Helvetica", 12))
        self.label_nome.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

        self.label_quantidade = tk.Label(self.frame_menu, text="QUANTIDADE:", font=("Helvetica", 12))
        self.label_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.quantidade_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.quantidade_entry.grid(row=2, column=1, padx=5, pady=5)

        self.label_destinatario = tk.Label(self.frame_menu, text="DESTINATÁRIO:", font=("Helvetica", 12))
        self.label_destinatario.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.destinatario_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.destinatario_entry.grid(row=3, column=1, padx=5, pady=5)

        # Adicionar botão para confirmar saída do item
        self.botao_confirmar = tk.Button(self.frame_menu, text="CONFIRMAR", command=self.confirmar_saida, font=("Helvetica", 12))
        self.botao_confirmar.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Adicionar botão para voltar ao menu principal
        self.botao_voltar = tk.Button(self.frame_menu, text="VOLTAR", command=self.criar_interface_menu, font=("Helvetica", 12))
        self.botao_voltar.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Criar widget
        self.label_resultado = tk.Label(self.frame_menu, text="", font=("Helvetica", 12))
        self.label_resultado.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Adicionar rastreador de evento para converter entrada em maiúsculas
        self.nome_entry.bind("<KeyRelease>", self.converter_maiusculas)
        self.destinatario_entry.bind("<KeyRelease>", self.converter_maiusculas)

    def confirmar_adicao(self):
        nome = self.nome_entry.get()
        quantidade = self.quantidade_entry.get()
        fornecedor = self.fornecedor_entry.get()
        if nome and quantidade and fornecedor:
            # Verificar se o item já existe no estoque
            itens = self.controle_estoque.listar_itens()
            for item in itens:
                if item[1] == nome:
                    # Se o item já existe no estoque, adicionar a quantidade informada à quantidade atual
                    nova_quantidade = int(item[2]) + int(quantidade)
                    self.controle_estoque.atualizar_quantidade(item[0], nova_quantidade)
                    self.mostrar_resultado("Quantidade do item atualizada com sucesso.")
                    return
            # Se o item não existe no estoque, adicioná-lo
            self.controle_estoque.adicionar_item(nome, quantidade, fornecedor)  # Atualize esta linha para passar o fornecedor
            self.mostrar_resultado("Item adicionado com sucesso.")
        else:
            self.mostrar_resultado("Por favor, insira um nome, uma quantidade e um fornecedor.")


    def limpar_tela(self):
        # Verificar se o frame do menu já existe
        if hasattr(self, 'frame_menu'):
            # Ocultar todos os widgets no frame do menu
            self.frame_menu.destroy()

    def realizar_login(self):
        username = self.username_entry.get()
        senha = self.senha_entry.get()
        usuario = self.login.verificar_usuario(username, senha)
        if usuario:
            self.frame_login.destroy()
            self.criar_interface_menu()
        else:
            self.label_mensagem.config(text="ERRO DE LOGIN: USUÁRIO OU SENHA INCORRETOS.")

    def criar_conta(self):
        username = self.username_entry.get()
        senha = self.senha_entry.get()
        if username and senha:
            self.login.criar_usuario(username, senha)
            self.label_mensagem.config(text="CONTA CRIADA: CONTA CRIADA COM SUCESSO.")
        else:
            self.label_mensagem.config(text="ERRO: POR FAVOR, INSIRA UM NOME DE USUÁRIO E UMA SENHA.")
                              
    def confirmar_saida(self):
        nome = self.nome_entry.get()
        quantidade = self.quantidade_entry.get()
        destinatario = self.destinatario_entry.get()
        if nome and quantidade and destinatario:
            if self.controle_estoque.saida_item(nome, quantidade, destinatario):
                self.mostrar_resultado("Saída registrada com sucesso.")
            else:
                self.mostrar_resultado("ERRO: QUANTIDADE INSUFICIENTE NO ESTOQUE OU ITEM NÃO ENCONTRADO.")
        else:
            self.mostrar_resultado("Por favor, preencha todos os campos.")

    def criar_interface_atualizar(self):
        # Limpar a tela
        self.limpar_tela()

        # Criar novo frame para os widgets
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(padx=20, pady=20)

        # Adicionar título
        titulo = tk.Label(self.frame_menu, text="ATUALIZAR ITENS", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Adicionar campos de entrada para o ID do item e a nova quantidade
        self.label_id = tk.Label(self.frame_menu, text="ID DO ITEM:", font=("Helvetica", 12))
        self.label_id.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)

        self.label_nova_quantidade = tk.Label(self.frame_menu, text="NOVA QUANTIDADE:", font=("Helvetica", 12))
        self.label_nova_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.nova_quantidade_entry = tk.Entry(self.frame_menu, font=("Helvetica", 12))
        self.nova_quantidade_entry.grid(row=2, column=1, padx=5, pady=5)

        # Adicionar botão para confirmar atualização da quantidade
        self.botao_confirmar = tk.Button(self.frame_menu, text="CONFIRMAR", command=self.confirmar_atualizacao, font=("Helvetica", 12))
        self.botao_confirmar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Adicionar botão para voltar ao menu principal
        self.botao_voltar = tk.Button(self.frame_menu, text="VOLTAR", command=self.criar_interface_menu, font=("Helvetica", 12))
        self.botao_voltar.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Criar widget label_resultado
        self.label_resultado = tk.Label(self.frame_menu, text="", font=("Helvetica", 12))
        self.label_resultado.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def confirmar_atualizacao(self):
        id_item = self.id_entry.get()
        nova_quantidade = self.nova_quantidade_entry.get()
        
        if id_item and nova_quantidade:
            if self.controle_estoque.atualizar_quantidade(id_item, nova_quantidade):
                self.mostrar_resultado("Quantidade atualizada com sucesso.")
            else:
                self.mostrar_resultado("ERRO: Falha ao atualizar a quantidade.")
        else:
            self.mostrar_resultado("Por favor, preencha todos os campos.")

    def mostrar_resultado(self, mensagem):
        self.label_resultado.config(text=mensagem)

    def exibir_historico_entrada(self):
        # Limpar a tela
        self.limpar_tela()

        # Criar novo frame para os widgets
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(padx=20, pady=20)

        # Adicionar título
        titulo = tk.Label(self.frame_menu, text="HISTÓRICO DE ENTRADA", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Criar frame para a tabela e barra de rolagem
        frame_tabela = tk.Frame(self.frame_menu)
        frame_tabela.grid(row=1, column=0, columnspan=2)

        # Criar estilo para a tabela
        estilo = ttk.Style()
        estilo.configure("mystyle.Treeview", background="#f0f0f0", fieldbackground="#f0f0f0", foreground="black", rowheight=25)

        # Criar tabela
        self.tree = ttk.Treeview(frame_tabela, style="mystyle.Treeview", columns=("ID", "Nome", "Quantidade", "Fornecedor"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Fornecedor", text="Fornecedor")

        # Exibir os itens na tabela
        registros = self.controle_estoque.listar_historico_entrada()
        for item in registros:
            self.tree.insert("", "end", values=item)

        # Ajustar a largura das colunas
        for i, coluna in enumerate(self.tree["columns"]):
            largura_coluna = max(tkfont().measure(coluna), max(tkfont().measure(str(item[i])) for item in registros)) + 95
            self.tree.column(coluna, width=largura_coluna)

        # Criar barra de rolagem vertical
        yscrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side="right", fill="y")

        # Mostrar a tabela
        self.tree.pack(side="left")

        # Adicionar botão para voltar ao menu principal
        self.botao_voltar = tk.Button(self.frame_menu, text="VOLTAR", command=self.criar_interface_menu, font=("Helvetica", 12))
        self.botao_voltar.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        self.frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def exibir_historico_saida(self):
        # Limpar a tela
        self.limpar_tela()

        # Criar novo frame para os widgets
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(padx=20, pady=20)

        # Adicionar título
        titulo = tk.Label(self.frame_menu, text="HISTÓRICO DE SAÍDA", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Criar frame para a tabela e barra de rolagem
        frame_tabela = tk.Frame(self.frame_menu)
        frame_tabela.grid(row=1, column=0, columnspan=2)

        # Criar estilo para a tabela
        estilo = ttk.Style()
        estilo.configure("mystyle.Treeview", background="#f0f0f0", fieldbackground="#f0f0f0", foreground="black", rowheight=25)

        # Criar tabela
        self.tree = ttk.Treeview(frame_tabela, style="mystyle.Treeview", columns=("ID", "Nome", "Quantidade", "Destino"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Destino", text="Destino")

        # Exibir os itens na tabela
        historico_saida = self.controle_estoque.listar_historico_saida()
        for item in historico_saida:
            self.tree.insert("", "end", values=item)

        # Ajustar a largura das colunas
        for i, coluna in enumerate(self.tree["columns"]):
            largura_coluna = max(tkfont().measure(coluna), max(tkfont().measure(str(item[i])) for item in historico_saida)) + 100
            self.tree.column(coluna, width=largura_coluna)

        # Criar barra de rolagem vertical
        yscrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side="right", fill="y")

        # Mostrar a tabela
        self.tree.pack(side="left")

        # Adicionar botão para voltar ao menu principal
        self.botao_voltar = tk.Button(self.frame_menu, text="VOLTAR", command=self.criar_interface_menu, font=("Helvetica", 12))
        self.botao_voltar.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        self.frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    def listar_itens(self):
        # Limpar a tela
        self.limpar_tela()

        # Criar novo frame para os widgets
        self.frame_menu = tk.Frame(self.root)
        self.frame_menu.pack(padx=20, pady=20)

        # Adicionar título
        titulo = tk.Label(self.frame_menu, text="LISTA DE ITENS", font=("Helvetica", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Verificar se a tabela "estoque" existe
        if not self.controle_estoque.verificar_existencia_tabela("estoque"):
            # Se a tabela não existir, exibir mensagem de que não há itens
            sem_itens_label = tk.Label(self.frame_menu, text="NÃO HÁ ITENS", font=("Helvetica", 12))
            sem_itens_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        else:
            # Se a tabela existir, verificar se há itens nela
            itens = self.controle_estoque.listar_itens()
            if not itens:
                # Se não houver itens, exibir mensagem de que não há itens
                sem_itens_label = tk.Label(self.frame_menu, text="NÃO HÁ ITENS", font=("Helvetica", 12))
                sem_itens_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            else:
                # Se houver itens, exibir a lista desses itens em uma tabela
                # Criar frame para a tabela e barra de rolagem
                frame_tabela = tk.Frame(self.frame_menu)
                frame_tabela.grid(row=1, column=0, columnspan=2)

                # Criar estilo para a tabela
                estilo = ttk.Style()
                estilo.configure("mystyle.Treeview", background="#f0f0f0", fieldbackground="#f0f0f0", foreground="black", rowheight=25)

                # Criar tabela
                self.tree = ttk.Treeview(frame_tabela, style="mystyle.Treeview", columns=("ID", "Nome", "Quantidade"), show="headings")
                self.tree.heading("ID", text="ID")
                self.tree.heading("Nome", text="Nome")
                self.tree.heading("Quantidade", text="Quantidade")

                # Exibir os itens na tabela
                for item in itens:
                    self.tree.insert("", "end", values=item)

                # Ajustar a largura das colunas
                for i, coluna in enumerate(self.tree["columns"]):
                    largura_coluna = max(tkfont().measure(coluna), max(tkfont().measure(str(item[i])) for item in itens)) + 150
                    self.tree.column(coluna, width=largura_coluna)

                # Criar barra de rolagem vertical
                yscrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
                self.tree.configure(yscrollcommand=yscrollbar.set)
                yscrollbar.pack(side="right", fill="y")

                # Mostrar a tabela
                self.tree.pack(side="left")

        # Adicionar botão para voltar ao menu principal
        self.botao_voltar = tk.Button(self.frame_menu, text="VOLTAR", command=self.criar_interface_menu, font=("Helvetica", 12))
        self.botao_voltar.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        self.frame_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    def converter_maiusculas(self, event):
        entry_widget = event.widget
        novo_texto = entry_widget.get().upper()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, novo_texto)