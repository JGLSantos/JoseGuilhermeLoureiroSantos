import psycopg2
from datetime import datetime


def project():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    clear()
    print("---------- Programa de Gest�o de PASTELTUGA V1.0 ----------")
    print("1 - Aceder a Back Office")
    print("2 - Aceder a Front Office")
    print("3 - Ver Clientes Registados")
    print("4 - Ver Empresas Registadas")
    print("0 - Terminar")
    print("")

    opcao = int(input("Escolha uma op��o: "))
    while (opcao != 0 and opcao != 1 and opcao != 2 and opcao != 3 and opcao != 4):
        opcao = int(input("Escolha uma op��o: "))

    if (opcao == 1):
        back_office()

    if (opcao == 2):
        front_office()

    if (opcao == 3):
        clear()
        cur.execute("SELECT ID, NOME, MORADA, CONTACTO FROM Clientes")
        for apresenta in cur:
            ID, NOME, MORADA, CONTACTO = apresenta
            print(ID, NOME, MORADA, CONTACTO)
        opcao2 = input("Retroceder: ")
        while (opcao2 != 'sim' and opcao2 != 'Sim'):
            opcao2 = input("Retroceder: ")
        return project()

    if (opcao == 4):
        clear()
        cur.execute("SELECT NOME, DESTINO FROM Empresas")
        for apresenta in cur:
            NOME, DESTINO = apresenta
            print(NOME, DESTINO)
        opcao2 = input("Retroceder: ")
        while (opcao2 != 'sim' and opcao2 != 'Sim'):
            opcao2 = input("Retroceder: ")
        cur.close()
        conn.close()
        return project()

    if (opcao == 0):
        cur.close()
        conn.close()
        return


def back_office():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    clear()
    print("---------- Back Office (Plataforma para Administradores) ----------")
    print("1 - Registar cliente")
    print("2 - Registar distribuidora")
    print("0 - Sair da aplica��o")
    print("")

    opcao = int(input("Escolha uma op��o: "))
    while (opcao != 0 and opcao != 1 and opcao != 2):
        opcao = int(input("Escolha uma op��o: "))

    if (opcao == 0):
        cur.close()
        return project()

    if (opcao == 1):
        clear()
        nome_cliente = input("Nome do cliente: ")
        add = input("Morada do cliente: ")
        tel = int(input("Contacto do cliente: "))
        id_cliente = int(input("N�mero de ID do cliente: "))
        while (id_cliente <= 0):
            id_cliente = int(input("N�mero de ID do cliente: "))
        cur.execute("INSERT INTO Clientes (ID, NOME, MORADA, CONTACTO) VALUES (%d, '%s', '%s', %d)" % (
            id_cliente, nome_cliente, add, tel))
        conn.commit()
        cur.close()
        conn.close()
        return back_office()

    if (opcao == 2):
        clear()
        nome_emp = input("Nome da empresa: ")
        destino = input("Escolha o destino da viagem: ")
        dist_viagem = int(input("Dist�ncia da viagem (em Km): "))
        dur_viagem = input("Dura��o da Viagem: ")
        id_emp = int(input("Numero de ID de empresa/destino: "))
        while (id_emp <= 0):
            id_emp = int(input("Numero de ID de empresa/destino: "))
        preco_dest = int(input("Pre�o Base de Transporte: "))
        preco_kg = int(input("Pre�o por Kg: "))
        cur.execute(
            "INSERT INTO Empresas (ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG) VALUES (%d, '%s', '%s', %d, '%s', %d, %d)" % (
                id_emp, nome_emp, destino, dist_viagem, dur_viagem, preco_dest, preco_kg))
        conn.commit()
        cur.close()
        conn.close()
        return back_office()


def front_office():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    clear()
    print("---------- Front Office (Plataforma para Funcion�rios) ----------")
    print("1 - Inserir encomenda")
    print("2 - Ver faturas")
    print("0 - Sair da aplica��o")
    print("")

    opcao = int(input("Escolha uma op��o: "))
    while (opcao != 0 and opcao != 1 and opcao != 2):
        opcao = int(input("Escolha uma op��o: "))

    if (opcao == 0):
        cur.close()
        conn.close()
        return project()

    if (opcao == 1):
        clear()

        cur.execute("SELECT ID, NOME, MORADA, CONTACTO FROM Clientes WHERE EMPRESA_ASSOCIADA IS NULL")
        for apresenta in cur:
            ID, NOME, MORADA, CONTACTO = apresenta
            print(ID, NOME, MORADA, CONTACTO)

        print("")
        enc_cliente = int(input("Escolha o ID do cliente: "))

        Kg = int(input("Quantida de past�is (em Kg): "))
        while (Kg <= 0 or Kg > 1500000):
            Kg = int(input("Quantida de past�is (em Kg): "))
        cur.execute("UPDATE Clientes SET PESO = %d WHERE ID = %d" % (Kg, enc_cliente))
        conn.commit()

        cur.execute("SELECT MORADA FROM Clientes WHERE ID = %d" % (enc_cliente))
        add = cur.fetchone()[0]

        cur.close()
        conn.close()

        return front_office_menu2(enc_cliente, add, Kg)

    if (opcao == 2):
        clear()
        cur.execute(
            "SELECT Clientes.DATA, Clientes.NOME, Clientes.MORADA, Clientes.CONTACTO, Empresas.NOME, Empresas.DISTANCIA, Clientes.PESO, Clientes.PRECO_TOTAL, EMPRESAS.DURACAO FROM Clientes, Empresas WHERE Clientes.EMPRESA_ASSOCIADA IS NOT NULL and Clientes.EMPRESA_ASSOCIADA = Empresas.ID")
        for apresenta in cur:
            print("----------FATURA DA ENCOMENDA---------")
            DATA, NOME, MORADA, CONTACTO, NAME, DISTANCIA, PESO, PRECO_TOTAL, DURACAO = apresenta
            print(DATA)
            print("Cliente: " + NOME)
            print("Morada: " + MORADA)
            print("Contacto: " + str(CONTACTO))
            print("Empresa de Distribuicao: " + NAME)
            print("Distancia da encomenda: " + str(DISTANCIA))
            print("Peso da encomenda: " + str(PESO))
            print("Custo Total: " + str(PRECO_TOTAL))
            print("Tempo de Entrega: " + DURACAO)
            print("-------------FIM DA FATURA------------")
            print("")
            print("")
        opcao3 = input("Retroceder: ")
        while (opcao3 != 'sim' and opcao3 != 'Sim'):
            opcao3 = input("Retroceder: ")
        cur.close()
        conn.close()
        return front_office()


def front_office_menu2(enc_cliente, add, Kg):
    now = datetime.now()

    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    clear()
    print("Organizar Empresas por: ")
    print("1 - Dura��o da Viagem")
    print("2 - Dist�ncia da Viagem")
    print("3 - Pre�o Para o Destino")
    print("4 - Pre�o Base por Kg")
    print("")
    print("5 - Escolher uma empresa para a entrega")

    opcao2 = int(input("Escolha uma op��o: "))
    while (opcao2 != 1 and opcao2 != 2 and opcao2 != 3 and opcao2 != 4 and opcao2 != 5):
        opcao2 = int(input("Escolha uma op��o: "))

    if (opcao2 == 1):
        clear()
        cur.execute(
            "SELECT ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG FROM Empresas WHERE DESTINO = '%s' ORDER BY DURACAO" % (
                add))
        for apresenta in cur:
            ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG = apresenta
            print(ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG)
        opcao3 = input("Retroceder: ")
        while (opcao3 != 'sim' and opcao3 != 'Sim'):
            opcao3 = input("Retroceder: ")
        conn.close()
        cur.close()
        return front_office_menu2(enc_cliente, add, Kg)

    if (opcao2 == 2):
        clear()
        cur.execute(
            "SELECT ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG FROM Empresas WHERE DESTINO = '%s' ORDER BY DISTANCIA" % (
                add))
        for apresenta in cur:
            ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG = apresenta
            print(ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG)
        opcao3 = input("Retroceder: ")
        while (opcao3 != 'sim' and opcao3 != 'Sim'):
            opcao3 = input("Retroceder: ")
        conn.close()
        cur.close()
        return front_office_menu2(enc_cliente, add, Kg)

    if (opcao2 == 3):
        clear()
        cur.execute(
            "SELECT ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG FROM Empresas WHERE DESTINO = '%s' ORDER BY PRECO_DESTINO" % (
                add))
        for apresenta in cur:
            ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG = apresenta
            print(ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG)
        opcao3 = input("Retroceder: ")
        while (opcao3 != 'sim' and opcao3 != 'Sim'):
            opcao3 = input("Retroceder: ")
        conn.close()
        cur.close()
        return front_office_menu2(enc_cliente, add, Kg)

    if (opcao2 == 4):
        clear()
        cur.execute(
            "SELECT ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG FROM Empresas WHERE DESTINO = '%s' ORDER BY PRECO_KG" % (
                add))
        for apresenta in cur:
            ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG = apresenta
            print(ID, NOME, DESTINO, DISTANCIA, DURACAO, PRECO_DESTINO, PRECO_KG)
        opcao3 = input("Retroceder: ")
        while (opcao3 != 'sim' and opcao3 != 'Sim'):
            opcao3 = input("Retroceder: ")
        conn.close()
        cur.close()
        return front_office_menu2(enc_cliente, add, Kg)

    if (opcao2 == 5):
        clear()
        emp_asso = int(input("Seleccione uma empresa para realizar a encomenda: "))
        data = str(now.day) + str('/') + str(now.month) + str('/') + str(now.year) + str(' - ') + str(now.hour) + str(
            'h:') + str(now.minute) + str('min')
        cur.execute("SELECT PRECO_DESTINO FROM Empresas WHERE ID = %d" % (emp_asso))
        preco_dest = cur.fetchone()[0]
        preco_kg = cur.execute("SELECT PRECO_KG FROM Empresas WHERE ID = %d" % (emp_asso))
        preco_kg = cur.fetchone()[0]
        preco_total = preco_dest + preco_kg * Kg
        cur.execute("UPDATE Clientes SET EMPRESA_ASSOCIADA = '%s', DATA = '%s', PRECO_TOTAL = %d WHERE ID = %d" % (
            emp_asso, data, preco_total, enc_cliente))
        conn.commit()
        conn.close()
        cur.close()
        return front_office()


def clear():
    print("\n" * 20)
