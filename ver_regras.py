import sqlite3

def listar_regras():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rules")
    regras = cursor.fetchall()
    
    print("--- Regras Atuais ---")
    if not regras:
        print("Nenhuma regra cadastrada.")
    for r in regras:
        print(f"ID: {r[0]} | Palavra-chave: {r[1]} | Categoria: {r[2]}")
    conn.close()

if __name__ == "__main__":
    listar_regras()