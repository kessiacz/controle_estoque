import sqlite3

class Login:
    def __init__(self, controle_estoque):
        self.controle_estoque = controle_estoque
        self.criar_tabela_usuarios()

    def conectar(self):
        return sqlite3.connect(self.controle_estoque.nome_banco)

    def criar_tabela_usuarios(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        senha TEXT NOT NULL
                    )''')
        conn.commit()
        conn.close()

    def criar_usuario(self, username, senha):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (username, senha) VALUES (?, ?)', (username, senha))
        conn.commit()
        conn.close()

    def verificar_usuario(self, username, senha):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND senha = ?', (username, senha))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
