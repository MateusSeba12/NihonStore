"""
Nihon Store - Sistema de Gestão e Compra de Mangás
Desenvolvido com foco nos requisitos da Engenharia de Software Moderna (Valente, 2020)
"""

import json
import os

# ==============================================================================
# ESTRUTURA 6: Estruturas (Registros / Dicionários / Tuplas)
# ESTRUTURA 4: Matrizes / Listas
# ==============================================================================
# As entidades são representadas por Dicionários (Registros) armazenados em Listas.
banco_dados = {
    "clientes": [
        {"id": 1, "nome": "Akira Toriyama", "cpf": "111.222.333-44"}
    ],
    "mangas": [
        {"id": 101, "titulo": "One Piece", "volume": 1, "preco": 34.90, "estoque": 15, "categoria": "Shonen"},
        {"id": 102, "titulo": "Naruto", "volume": 1, "preco": 29.90, "estoque": 8, "categoria": "Shonen"},
        {"id": 103, "titulo": "Berserk", "volume": 1, "preco": 59.90, "estoque": 5, "categoria": "Seinen"}
    ],
    "vendas": []
}

ARQUIVO_DADOS = "nihon_store_db.json"

# ==============================================================================
# ESTRUTURA 3: Subprogramas (Funções)
# ESTRUTURA 7: Arquivos (Persistência em Disco)
# ==============================================================================
def salvar_dados():
    """Salva a estrutura de dados atual em um arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as file:
        json.dump(banco_dados, file, indent=4, ensure_ascii=False)
    print("\n[INFO] Dados salvos no arquivo com sucesso!")

def carregar_dados():
    """Carrega os dados salvos do arquivo para a memória."""
    global banco_dados
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as file:
            banco_dados = json.load(file)
        print("[INFO] Dados carregados do arquivo local.")

# ==============================================================================
# SUBPROGRAMAS DE GESTÃO (CRUD e Regras de Negócio)
# ==============================================================================
def cadastrar_manga():
    """Cadastra um novo mangá no acervo da Nihon Store."""
    print("\n--- CADASTRO DE MANGÁ - NIHON STORE ---")
    
    # ESTRUTURA 5: Cadeia de caracteres / String
    titulo = str(input("Título do Mangá: ")).strip()
    volume = int(input("Volume: "))
    preco = float(input("Preço R$: "))
    estoque = int(input("Quantidade em Estoque: "))
    categoria = str(input("Categoria (Shonen/Seinen/Shojo): ")).strip()

    novo_id = 101 if not banco_dados["mangas"] else banco_dados["mangas"][-1]["id"] + 1

    # Registro (Dicionário)
    manga = {
        "id": novo_id,
        "titulo": titulo,
        "volume": volume,
        "preco": preco,
        "estoque": estoque,
        "categoria": categoria
    }
    
    banco_dados["mangas"].append(manga)
    salvar_dados()
    print(f"Mangá '{titulo} Vol. {volume}' cadastrado com sucesso! ID: {novo_id}")

def listar_mangas():
    """Exibe os mangás cadastrados no catálogo da Nihon Store."""
    print("\n---------------- CATÁLOGO NIHON STORE ----------------")
    print(f"{'ID':<5} | {'Título':<20} | {'Vol.':<5} | {'Preço (R$)':<10} | {'Estoque':<8} | {'Categoria':<10}")
    print("-" * 70)
    
    # ESTRUTURA 2: Repetição (for)
    for m in banco_dados["mangas"]:
        print(f"{m['id']:<5} | {m['titulo']:<20} | {m['volume']:<5} | R$ {m['preco']:<7.2f} | {m['estoque']:<8} | {m['categoria']:<10}")

def cadastrar_cliente():
    """Cadastra um cliente no sistema."""
    print("\n--- CADASTRO DE CLIENTE - NIHON STORE ---")
    nome = str(input("Nome do Cliente: ")).strip()
    cpf = str(input("CPF: ")).strip()

    novo_id = 1 if not banco_dados["clientes"] else banco_dados["clientes"][-1]["id"] + 1
    cliente = {"id": novo_id, "nome": nome, "cpf": cpf}
    
    banco_dados["clientes"].append(cliente)
    salvar_dados()
    print(f"Cliente '{nome}' cadastrado com sucesso! ID: {novo_id}")

def realizar_venda():
    """Realiza a compra/venda de mangás atualizando o estoque."""
    print("\n--- REALIZAR VENDA DE MANGÁ ---")
    listar_mangas()
    
    id_manga = int(input("\nInforme o ID do Mangá: "))
    
    # Busca do mangá na lista
    manga_encontrado = None
    for m in banco_dados["mangas"]:
        if m["id"] == id_manga:
            manga_encontrado = m
            break

    # ESTRUTURA 1: Condicional (if/else)
    if manga_encontrado is None:
        print("[ERRO] Mangá não encontrado no catálogo da Nihon Store!")
        return

    qtd = int(input(f"Quantidade desejada de '{manga_encontrado['titulo']}': "))

    if qtd <= 0:
        print("[ERRO] A quantidade deve ser maior que zero!")
    elif qtd > manga_encontrado["estoque"]:
        print(f"[ERRO] Estoque insuficiente! Estoque atual: {manga_encontrado['estoque']}")
    else:
        # Cálculo de valor com desconto para compras de 3 ou mais unidades
        val_total = manga_encontrado["preco"] * qtd
        if qtd >= 3:
            val_total *= 0.90 # 10% de desconto
            print("[DESCONTO NIHON STORE] 10% de desconto aplicado por comprar 3 ou mais volumes!")

        # Atualização do Estoque
        manga_encontrado["estoque"] -= qtd

        # Registro da Venda
        venda = {
            "id_manga": id_manga,
            "titulo": manga_encontrado["titulo"],
            "qtd": qtd,
            "valor_total": val_total
        }
        banco_dados["vendas"].append(venda)
        salvar_dados()
        print(f"\n[SUCESSO] Venda realizada! Total a pagar: R$ {val_total:.2f}")

def gerar_relatorio():
    """Gera um relatório sintético do caixa e vendas da Nihon Store."""
    print("\n================ RELATÓRIO DE VENDAS NIHON STORE ================")
    faturamento_total = 0.0
    total_itens = 0

    # ESTRUTURA 2: Repetição (for)
    for v in banco_dados["vendas"]:
        faturamento_total += v["valor_total"]
        total_itens += v["qtd"]

    print(f"Total de vendas realizadas: {len(banco_dados['vendas'])}")
    print(f"Total de mangás vendidos:  {total_itens} unidades")
    print(f"Faturamento Total:         R$ {faturamento_total:.2f}")
    print("==================================================================")

# ==============================================================================
# MENU PRINCIPAL (ESTRUTURA DE CONTROLE GERAL)
# ==============================================================================
def menu_principal():
    carregar_dados()
    
    # ESTRUTURA 2: Repetição (while)
    opcao = ""
    while opcao != "0":
        print("\n" + "="*40)
        print("          SYSTEM NIHON STORE v1.0         ")
        print("="*40)
        print("1. Listar Catálogo de Mangás")
        print("2. Cadastrar Novo Mangá")
        print("3. Cadastrar Cliente")
        print("4. Realizar Venda")
        print("5. Gerar Relatório Financeiro")
        print("0. Sair do Sistema")
        
        opcao = input("Opção desejada: ").strip()

        # ESTRUTURA 1: Condicionais Encadeadas (if / elif / else)
        if opcao == "1":
            listar_mangas()
        elif opcao == "2":
            cadastrar_manga()
        elif opcao == "3":
            cadastrar_cliente()
        elif opcao == "4":
            realizar_venda()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "0":
            print("\nEncerrando o Nihon Store. Arigatou gozaimasu!")
        else:
            print("\n[ERRO] Opção inválida! Tente novamente.")

# Execução do Programa
if __name__ == "__main__":
    menu_principal()
