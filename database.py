import sqlite3
from datetime import datetime

class ControleEstoque:
    def __init__(self, nome_banco="estoque.db"):
        self.nome_banco = nome_banco

    def conectar(self):
        return sqlite3.connect(self.nome_banco)

    def criar_tabela(self):
        conn = sqlite3.connect(self.nome_banco)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                        id INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        fornecedor TEXT NOT NULL,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        senha TEXT NOT NULL
                    )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS historico_entrada (
                        id INTEGER PRIMARY KEY,
                        nome_item TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        fornecedor TEXT NOT NULL,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')  
        cursor.execute('''CREATE TABLE IF NOT EXISTS historico_saida (
                        id INTEGER PRIMARY KEY,
                        nome_item TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        fornecedor TEXT NOT NULL,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        conn.commit()
        conn.close()

    def adicionar_item(self, nome, quantidade, fornecedor):
        if not self.verificar_existencia_tabela("estoque"):
            self.criar_tabela()
        
        nome = nome.upper()
        fornecedor = fornecedor.upper()

        conn = self.conectar()
        cursor = conn.cursor()

        # Verificar se o item já existe no estoque
        cursor.execute('SELECT * FROM estoque WHERE nome = ?', (nome,))
        item_existente = cursor.fetchone()

        if item_existente:
            # Se o item já existe, adicionar a quantidade informada à quantidade atual
            nova_quantidade = int(item_existente[2]) + int(quantidade)
            cursor.execute('UPDATE estoque SET quantidade = ? WHERE id = ?', (nova_quantidade, item_existente[0]))
        else:
            # Se o item não existe, inserir um novo registro no estoque
            cursor.execute('INSERT INTO estoque (nome, quantidade, fornecedor) VALUES (?, ?, ?)', (nome, quantidade, fornecedor))
            cursor.execute('INSERT INTO historico_entrada (nome_item, quantidade, fornecedor) VALUES (?, ?, ?)', (nome, quantidade, fornecedor))

        conn.commit()
        conn.close()

    def saida_item(self, nome, quantidade, fornecedor):
        nome = nome.upper()
        fornecedor = fornecedor.upper()

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque WHERE nome = ?', (nome,))
        item_encontrado = cursor.fetchone()
        if item_encontrado:
            quantidade_disponivel = int(item_encontrado[2])
            if quantidade_disponivel >= int(quantidade):
                nova_quantidade = quantidade_disponivel - int(quantidade)
                cursor.execute('UPDATE estoque SET quantidade = ? WHERE id = ?', (nova_quantidade, item_encontrado[0]))
                conn.commit()
                # Registrar a saída no histórico
                self.registrar_saida(nome, quantidade, fornecedor)
                conn.close()
                return True
            else:
                conn.close()
                return False
        else:
            conn.close()
            return False

    def registrar_saida(self, nome, quantidade, fornecedor):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO historico_saida (nome_item, quantidade, fornecedor, data) VALUES (?, ?, ?, ?)', (nome, quantidade, fornecedor, datetime.now()))
        conn.commit()
        conn.close()

    def atualizar_quantidade(self, id, quantidade):
            conn = self.conectar()
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE estoque SET quantidade = ? WHERE id = ?', (quantidade, id))
                conn.commit()
                if cursor.rowcount > 0:
                    print("Atualização bem-sucedida.")
                    return True
                else:
                    print("Nenhum item encontrado para atualizar.")
                    return False
            except Exception as e:
                print("Erro ao atualizar quantidade:", e)
                return False
            finally:
                conn.close()

    def existe_item(self, id_item):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estoque WHERE id = ?", (id_item,))
        item = cursor.fetchone()
        conn.close()
        return item is not None

    def listar_itens(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque')
        itens = cursor.fetchall()
        conn.close()
        
        if not itens:
            return "Não há itens no estoque."
        else:
            return itens
        
    def verificar_existencia_tabela(self, nome_tabela):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nome_tabela,))
        tabela = cursor.fetchone()
        conn.close()
        return tabela is not None

    def listar_historico_entrada(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome_item, quantidade, fornecedor, strftime("%d/%m/%Y %H:%M:%S", data) AS data FROM historico_entrada')
        historico = cursor.fetchall()
        conn.close()
        return historico

    def listar_historico_saida(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome_item, quantidade, fornecedor, strftime("%d/%m/%Y %H:%M:%S", data) AS data FROM historico_saida')
        historico = cursor.fetchall()
        conn.close()
        return historico
