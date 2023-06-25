import base64 as b64
import sqlite3
from glob import glob
from re import sub
from sqlite3 import Error
from typing import List
from Model.Status_Resposta import StatusResposta
from Model.Usuario import Usuario
from Model.Post import Post
from Model.exceptions.UserExisteException import UserExisteException


# -- -----------------------------------------------------
# -- funções para o Model de dados
# -- -----------------------------------------------------

def create_bd():
    conn = sqlite3.connect("Control/CadastroUsuario.bd")
    print("Banco de dados criado com sucesso!")

    # Criação da tabela "Usuario"
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            user TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            seguidores TEXT NOT NULL
        )
    """)
    print("Tabela 'Usuario' criada com sucesso!")

    # Criação da tabela "post"
    conn.execute("""
        CREATE TABLE IF NOT EXISTS post (
            id_post INTEGER PRIMARY KEY AUTOINCREMENT,
            TAG_post TEXT NOT NULL,
            data_post TEXT NOT NULL,
            horario_post TEXT NOT NULL,
            conteudo_post TEXT NOT NULL,
            estrelas_post REAL NOT NULL,
            comentario_post TEXT NOT NULL,
            qnt_avaliacoes INTEGER NOT NULL,
            Usuario_user TEXT,
            FOREIGN KEY (Usuario_user) REFERENCES Usuario (user)
        )
    """)
    print("Tabela 'post' criada com sucesso!")

    conn.close()


class Banco:
    def __init__(self):
        self.qnt_imagens = self.atualiza_qnt()
        con = sqlite3.connect('Control/CadastroUsuario.bd', check_same_thread=False)
        self.vcon = con

    def ExecutaSQL(self, conexao, sql):
        try:
            c = conexao.cursor()
            c.execute(sql)
            conexao.commit()
            return c
        except sqlite3.Error as ex:
            print(ex)

    # -- -----------------------------------------------------
    # -- função para inserir um novo usuário
    # -- -----------------------------------------------------

    def inserirUsuario(self, usuario: Usuario):
        nome = usuario.get_nome()
        user = usuario.get_user()
        email = usuario.get_email()
        senha = usuario.get_senha()

        vsql = "SELECT * FROM Usuario WHERE user == '{}'".format(user)
        result = self.ExecutaSQL(self.vcon, vsql)
        if result.fetchone() is None:  # caso não encontre o nome de usuário (user), então insere
            vsql = "INSERT INTO Usuario(nome, user, email, senha, seguidores) " \
                   f"VALUES('{nome}', '{user}', '{email}', '{senha}', '{'[]'}')"
            self.ExecutaSQL(self.vcon, vsql)
            return
        raise UserExisteException(user)

    # -- -----------------------------------------------------
    # -- função para inserir um post
    # -- -----------------------------------------------------

    def inserirPost(self, user: str, post: Post, imagem):
        try:
            tag_post = post.tag
            horario_post = post.horario
            conteudo_post = post.conteudo
            estrelas_post = post.estrelas
            comentario_post = post.comentarios

            self.qnt_imagens = self.atualiza_qnt()

            path = f'Model/imagens/{self.qnt_imagens}.jpg'

            print("inserindo:"+path)

            decodeit = open(path, 'wb')
            decodeit.write(imagem)

            data_post = path

            vsql = "INSERT INTO " \
                   "post(TAG_post, data_post, horario_post, conteudo_post, comentario_post, estrelas_post, " \
                   "Usuario_user, qnt_avaliacoes) " \
                   f"VALUES('{tag_post}', '{data_post}', '{horario_post}', '{conteudo_post}', '{comentario_post}', " \
                   f"'{estrelas_post}', '{user}', '{0}')"

            self.ExecutaSQL(self.vcon, vsql)
            return StatusResposta.sucesso.value  # 1
        except Error as e:
            raise e
            # return StatusResposta.falha.value  # 0

    # -- -----------------------------------------------------
    # -- função para deletar um post
    # -- -----------------------------------------------------

    def deletarPost(self, idpost: int, user: str):
        try:
            vsql = "DELETE FROM post WHERE id_post == {} AND Usuario_user == '{}'".format(idpost, user)
            self.ExecutaSQL(self.vcon, vsql)
            return StatusResposta.sucesso.value  # 1
        except:
            return StatusResposta.falha.value  # 0

    # -- -----------------------------------------------------
    # -- função para buscar usuário pelo user e senha
    # -- -----------------------------------------------------

    def buscarUsuario(self, user: str, senha: str) -> Usuario:
        vsql = "SELECT * FROM Usuario WHERE user == '{}' AND senha == '{}'".format(user, senha)
        result = self.ExecutaSQL(self.vcon, vsql)
        row = result.fetchone()
        if row is None:
            return None
        else:
            usuario = Usuario(nome=row[1], user=row[0], email=row[2], senha=row[3])

            usuario.inserir_seguidores(row[4][1:-1].split(','))

            return usuario

    # -- -----------------------------------------------------
    # -- função para buscar usuários pelo user (nome de usuário)
    # -- -----------------------------------------------------

    def buscarUsuarioBancoUser(self, user: str) -> Usuario:
        vsql = "SELECT * FROM Usuario WHERE user == '{}'".format(user)
        result = self.ExecutaSQL(self.vcon, vsql).fetchone()

        if result is None:
            return None

        usuario = Usuario(nome=result[1], user=result[0], email=result[2], senha=result[3])

        usuario.inserir_seguidores(result[4][1:-1].split(','))

        return usuario

    # -- -----------------------------------------------------
    # -- função para atualizar o Model (seja atualizar o nome, senha ou user)
    # -- -----------------------------------------------------

    def inserir_seguidores(self, user:Usuario, seguidor):
        user.inserir_seguidores([seguidor])

        self.atualizaBanco(user)

    # -- -----------------------------------------------------
    # -- função para atualizar o Post
    # -- -----------------------------------------------------


    def atualizaBancoPost(self, post: Post):
        dt = post.get_data()
        vsql = f"UPDATE post SET estrelas_post = '{post.get_estrelas()}', qnt_avaliacoes = '{post.get_qnt()}' " \
               f"WHERE data_post = '{dt}'"
        self.ExecutaSQL(self.vcon, vsql)


    # -- -----------------------------------------------------
    # -- função para atualizar o Model (seja atualizar o nome, senha, user ou seguidores)
    # -- -----------------------------------------------------


    def atualizaBanco(self, user: Usuario):
        nome = user.nome
        senha = user.senha
        usuario = user.user
        seguidores = str(user.get_sou_seguidor()).replace("\'", '').replace(" ","")
        print(str(user.get_sou_seguidor()).replace("\'",'').replace(" ",""))
        vsql = f"""UPDATE Usuario 
                    SET user = '{usuario}', 
                    nome = '{nome}', 
                    senha = '{senha}', 
                    seguidores = '{seguidores}'
                    WHERE user = '{usuario}'"""
        self.ExecutaSQL(self.vcon, vsql)

    # -- -----------------------------------------------------
    # -- função para listar todos os usuários
    # -- -----------------------------------------------------

    def listarUsuarios(self) -> List[Usuario]:
        vsql = "SELECT * FROM Usuario"
        usuarios = []
        result = self.ExecutaSQL(self.vcon, vsql)
        for row in result:
            usuarios.append(Usuario(nome=row[1], user=row[0], email=row[2], senha=row[3]))
        return usuarios

    # -- -----------------------------------------------------
    # -- função para buscar posts de um usuário
    # -- -----------------------------------------------------

    def buscarPost(self, user: str) -> List[Post]:
        posts = []
        vsql = "SELECT * FROM post WHERE Usuario_user == '{}'".format(user)
        result = self.ExecutaSQL(self.vcon, vsql)
        for row in result:
            print("buscando:"+row[2])
            post = Post(tag_post=row[1], data_post=row[2], horario_post=row[3], conteudo_post=row[4], comentarios_post=row[6])
            post.set_estrela(row[5], row[7])
            posts.append(post)
        return posts

    # -- -----------------------------------------------------
    # -- função para buscar posts de um usuário
    # -- -----------------------------------------------------

    def buscarAutor(self, data_post: str) -> List[Post]:
        posts = []
        vsql = "SELECT * FROM post WHERE data_post == '{}'".format(data_post)
        result = self.ExecutaSQL(self.vcon, vsql)
        for row in result:
            print("buscando:"+row[2])
            post = Post(tag_post=row[1], data_post=row[2], horario_post=row[3], conteudo_post=row[4], comentarios_post=row[6])
            post.set_estrela(row[5], row[7])
            posts.append(post)
            return row[8]

    def atualiza_qnt(self):
        lista = [-1]
        lista.extend([int(sub(r'[^0-9]', '', x.split('/')[-1])) for x in glob('Model/imagens/*')])
        return max(lista) + 1


# Continuação do código (testes)

"""if __name__ == "__main__":
    CriarBanco("CadastroUsuario.bd")

    # Conectar ao Model de dados
    vcon = ConexaoBanco()

    # Criar uma instância de usuário e inserir no Model de dados
    usuario1 = Usuario(nome='João', user='joao123', email='joao@example.com', senha='senha123')
    resultado_insercao = inserirUsuario(usuario1)
    print("Resultado da inserção do usuário:", resultado_insercao)


    # Criar uma instância de post e inserir no Model de dados
    post1 = Post(id=1, tag_post='tag1', data_post='2023-01-01', horario_post='12:00:00', conteudo_post='Receita de bolo', estrelas_post=4.5, comentarios_post='ótimo post')
    resultado_insercao_post = inserirPost(user='joao123', post=post1)
    print("Resultado da inserção do post:", resultado_insercao_post)

    # Buscar um usuário pelo nome de usuário e senha
    usuario_encontrado = buscarUsuario('joao123', 'senha123')
    if usuario_encontrado:
        print("Usuário encontrado:", usuario_encontrado.nome)
    else:
        print("Usuário não encontrado.")

    # Atualizar o nome de um usuário
    usuario_encontrado.nome = 'João Silva'
    atualizaBanco(usuario_encontrado)
    print("Usuário atualizado:", usuario_encontrado.nome)


    #Listar todos os usuários
    usuarios = listarUsuarios()
    print("Lista de usuários:")
    for u in usuarios:
        print(u.nome)


    # Buscar posts de um usuário
    posts = buscarPost('joao123')
    print("Posts do usuário:")
    for p in posts:
        print("ID",p.id,"Data",p.data,"Horario",p.horario,"Tag",p.tag,"Conteudo",p.conteudo,"comentarios",p.comentarios,"Estrelas",p.estrelas)

    # Deletar um post
    resultado_delecao = deletarPost(1, 'joao123')
    print("Resultado da deleção do post:", resultado_delecao)"""
