from abc import ABC, abstractmethod
import sqlite3 as sql
import funcoes


class BancoDados(ABC):
    def __init__(self):
        """Realiza a conexão com o banco de dados."""
        self.conexao = sql.connect("bancodados.db")
        self.cursor = self.conexao.cursor()

    @abstractmethod
    def registrar(self):
        """Registra uma linha no banco de dados."""
        pass

    @abstractmethod
    def atualizar(self):
        """Atualiza uma linha no banco de dados."""
        pass

    @abstractmethod
    def deletar(self):
        """Deleta uma linha no banco de dados."""
        pass

    def __del__(self):
        """Finaliza a conexão com o banco de dados."""
        self.cursor.close()
        self.conexao.close()

    class ValorNuloErro(Exception):
        """Erro indicando uma entrada de valor nulo."""
        pass

    class ValorInvalidoErro(Exception):
        """Erro indicando uma entrada de valor inválido."""
        pass

    class CancelarErro(Exception):
        """Erro indicando uma ação de menu interrompida."""
        pass


class Aeronaves(BancoDados):
    def __init__(self):
        super().__init__()

    def registrar(self):
        """Registra uma aeronave no banco de dados."""
        self.cursor.execute(
            "INSERT INTO Aeronaves(MODELO_AERONAVE, ASSENTOS_DISPONIVEIS, LIMITE_BAGAGEM)"
            "VALUES(?, ?, ?)", (self.__modelo(), self.__assentos(), self.__limite())
        )
        self.conexao.commit()

    def atualizar(self):
        """Atualiza uma aeronave do banco de dados."""
        codigo = self.__listar()
        coluna = self.__colunas()
        self.cursor.execute(
            f"UPDATE Aeronaves SET {coluna[0]}=? WHERE COD_AERONAVE=?", (coluna[1](), codigo)
        )
        self.conexao.commit()

    def deletar(self):
        """Deleta uma aeronave do banco de dados."""
        codigo = self.__listar()
        while True:
            confirmacao = input(
                f"Você está prester a deleter a aeronave Código-{codigo}, "
                f"têm certeza desta ação? [ S / N ]"
            )
            if confirmacao.lower() == "s":
                break
            elif confirmacao.lower() == "n":
                raise self.CancelarErro
            else:
                print("\nEscolha inválida.\n")
        self.cursor.execute(
            f"DELETE FROM Aeronaves WHERE COD_AERONAVE={codigo}"
        )
        self.conexao.commit()

    def __modelo(self):
        """Entrada do modelo da aeronave."""
        modelo_aeronave = input("Modelo da Aeronave: ")
        if modelo_aeronave == "":
            raise self.ValorNuloErro("O modelo da aeronave não foi preenchido.")
        return modelo_aeronave

    def __assentos(self):
        """Entrada dos assentos disponíveis."""
        try:
            assentos_disponiveis = int(input("Assentos Disponíveis: "))
            if assentos_disponiveis <= 0:
                raise self.ValorInvalidoErro("O número de assentos disponíveis deve ser um número positivo.")
            return assentos_disponiveis
        except ValueError:
            raise ValueError("O número de assentos disponíveis deve ser um número inteiro.")

    def __limite(self):
        """Entrada do limite de bagagem."""
        try:
            limite_bagagem = float(input("Limite de Bagagem: "))
            if limite_bagagem <= 0:
                raise self.ValorInvalidoErro("O limite de bagagem deve ser um número positivo.")
            return limite_bagagem
        except ValueError:
            raise ValueError("O limite de bagagem deve ser um número real.")

    def __colunas(self):
        """Seleção de colunas e as suas respetivas entradas."""
        colunas = {
            1: ["MODELO_AERONAVE", self.__modelo],
            2: ["ASSENTOS_DISPONIVEIS", self.__assentos],
            3: ["LIMITE_BAGAGEM", self.__limite]
        }
        while True:
            print(
                "Escolha qual coluna modificar:\n"
                "[1] - Modelo da Aeronave\n"
                "[2] - Assentos Disponíveis\n"
                "[3] - Limite de Bagagem\n"
                "[4] - Retornar / Sair"
            )
            try:
                escolha = int(input(">> "))
                if escolha == 4:
                    raise self.CancelarErro
                else:
                    return colunas.get(escolha)
            except ValueError:
                print("\nEscolha inválida.\n")

    def __listar(self):
        """Lista e escolhe um ID da tabela de aeronaves"""
        self.cursor.execute(
            "SELECT * FROM Aeronaves"
        )
        lista_ids = []
        while True:
            for linha in self.cursor.fetchall():
                print(*linha, sep=" - ")
            escolha = input("Escolha um ID de aeronave ou pressione ENTER para cancelar: ")
            if escolha == "":
                raise self.CancelarErro
            try:
                escolha = int(escolha)
                if escolha not in lista_ids:
                    print("\nID inexistente...")
                    funcoes.continuar()
                    continue
                return escolha
            except ValueError:
                raise self.ValorInvalidoErro("\nID deve ser um número inteiro positivo...")


class Aeroportos(BancoDados):
    def __init__(self):
        super().__init__()

    def registrar(self):
        """Registra um aeroporto no banco de dados."""
        self.cursor.execute(
            "INSERT INTO Aeroportos(NOME_AEROPORTO, SIGLA_AEROPORTO, CIDADE, ESTADO, PAIS, CONTINENTE)"
            "VALUES(?, ?, ?, ?, ?, ?)", (
                self.__nome(), self.__sigla(), self.__cidade(), self.__estado(), self.__pais(), self.__continente()
            )
        )
        self.conexao.commit()

    def atualizar(self):
        """Atualiza um aeroporto do banco de dados."""
        codigo = self.__listar()
        coluna = self.__colunas()
        self.cursor.execute(
            f"UPDATE Aeroportos SET {coluna[0]}=? WHERE COD_AEROPORTO=?", (coluna[1](), codigo)
        )
        self.conexao.commit()

    def deletar(self):
        """Deleta um aeroporto do banco de dados."""
        codigo = self.__listar()
        while True:
            confirmacao = input(
                f"Você está prester a deleter o aeroporto Código-{codigo}, "
                f"têm certeza desta ação? [ S / N ]"
            )
            if confirmacao.lower() == "s":
                break
            elif confirmacao.lower() == "n":
                raise self.CancelarErro
            else:
                print("\nEscolha inválida.\n")
        self.cursor.execute(
            f"DELETE FROM Aeroportos WHERE COD_AEROPORTO={codigo}"
        )
        self.conexao.commit()

    def __nome(self):
        """Entrada do nome do aeroporto."""
        nome_aeroporto = input("Nome do Aeroporto: ")
        if nome_aeroporto == "":
            raise self.ValorNuloErro("O nome do aeroporto não foi preenchido.")
        return nome_aeroporto

    def __sigla(self):
        """Entrada da sigla do aeroporto."""
        sigla_aeroporto = input("Sigla do Aeroporto: ")
        if sigla_aeroporto == "":
            raise self.ValorNuloErro("A sigla do aeroporto não foi preenchida.")
        return sigla_aeroporto

    def __cidade(self):
        """Entrada da cidade do aeroporto."""
        cidade = input("Cidade: ")
        if cidade == "":
            raise self.ValorNuloErro("Cidade não foi preenchida.")
        return cidade

    def __estado(self):
        """Entrada do estado do aeroporto."""
        estado = input("Estado: ")
        if estado == "":
            raise self.ValorNuloErro("Estado não foi preenchido.")
        return estado

    def __pais(self):
        """Entrada do país do aeroporto."""
        pais = input("País: ")
        if pais == "":
            raise self.ValorNuloErro("País não foi preenchido.")
        return pais

    def __continente(self):
        """Entrada da cidade do aeroporto."""
        continente = input("Continente: ")
        if continente == "":
            raise self.ValorNuloErro("Continente não foi preenchido.")
        return continente

    def __colunas(self):
        """Seleção de colunas e as suas respetivas entradas."""
        colunas = {
            1: ["NOME_AEROPORTO", self.__nome],
            2: ["SIGLA_AEROPORTO", self.__sigla],
            3: ["CIDADE", self.__cidade],
            4: ["ESTADO", self.__estado],
            5: ["PAIS", self.__pais],
            6: ["CONTINENTE", self.__continente]
        }
        while True:
            print(
                "Escolha qual coluna modificar:\n"
                "[1] - Nome do Aeroporto\n"
                "[2] - Sigla do Aeroporto\n"
                "[3] - Cidade\n"
                "[4] - Estado\n"
                "[5] - País\n"
                "[6] - Continente\n"
                "[7] - Retornar / Sair"
            )
            try:
                escolha = int(input(">> "))
                if escolha == 4:
                    raise self.CancelarErro
                else:
                    return colunas.get(escolha)
            except ValueError:
                print("\nEscolha inválida.\n")

    def __listar(self):
        """Lista e escolhe um ID da tabela de aeroportos"""
        self.cursor.execute(
            "SELECT * FROM Aeroportos"
        )
        lista_ids = []
        while True:
            for linha in self.cursor.fetchall():
                print(*linha, sep=" - ")
            escolha = input("Escolha um ID de aeroporto ou pressione ENTER para cancelar: ")
            if escolha == "":
                raise self.CancelarErro
            try:
                escolha = int(escolha)
                if escolha not in lista_ids:
                    print("\nID inexistente...")
                    funcoes.continuar()
                    continue
                return escolha
            except ValueError:
                raise self.ValorInvalidoErro("\nID deve ser um número inteiro positivo...")


class Empresas(BancoDados):
    def __init__(self):
        super().__init__()

    def registrar(self):
        """Registra uma empresa no banco de dados."""
        self.cursor.execute(
            "INSERT INTO Empresas(NOME_EMPRESA, NACIONALIDADE_DA_EMPRESA, SIGLA_DA_EMPRESA)"
            "VALUES(?, ?, ?)", (self.__nome(), self.__nacionalidade(), self.__sigla())
        )
        self.conexao.commit()

    def atualizar(self):
        """Atualiza uma empresa do banco de dados."""
        codigo = self.__listar()
        coluna = self.__colunas()
        self.cursor.execute(
            f"UPDATE Empresas SET {coluna[0]}=? WHERE COD_EMPRESA=?", (coluna[1](), codigo)
        )
        self.conexao.commit()

    def deletar(self):
        """Deleta uma empresa do banco de dados."""
        codigo = self.__listar()
        while True:
            confirmacao = input(
                f"Você está prester a deleter a empresa Código-{codigo}, "
                f"têm certeza desta ação? [ S / N ]"
            )
            if confirmacao.lower() == "s":
                break
            elif confirmacao.lower() == "n":
                raise self.CancelarErro
            else:
                print("\nEscolha inválida.\n")
        self.cursor.execute(
            f"DELETE FROM Empresas WHERE COD_EMPRESA={codigo}"
        )
        self.conexao.commit()

    def __nome(self):
        """Entrada do nome da empresa."""
        nome_empresa = input("Nome da Empresa: ")
        if nome_empresa == "":
            raise self.ValorNuloErro("O nome da empresa não foi preenchido.")
        return nome_empresa

    def __nacionalidade(self):
        """Entrada da nacionalidade da empresa."""
        nacionalidade_empresa = input("Nacionalidade da Empresa: ")
        if nacionalidade_empresa == "":
            raise self.ValorNuloErro("A nacionalidade da empresa não foi preenchida.")
        return nacionalidade_empresa

    def __sigla(self):
        """Entrada da sigla da empresa."""
        sigla_empresa = input("Sigla da Empresa: ")
        if sigla_empresa == "":
            raise self.ValorNuloErro("A sigla da empresa não foi preenchida.")
        return sigla_empresa

    def __colunas(self):
        """Seleção de colunas e as suas respetivas entradas."""
        colunas = {
            1: ["NOME_EMPRESA", self.__nome],
            2: ["NACIONALIDADE_DA_EMPRESA", self.__nacionalidade],
            3: ["SIGLA_DA_EMPRESA", self.__sigla]
        }
        while True:
            print(
                "Escolha qual coluna modificar:\n"
                "[1] - Nome da Empresa\n"
                "[2] - Nacionalidade da Empresa\n"
                "[3] - Sigla da Empresa\n"
                "[4] - Retornar / Sair"
            )
            try:
                escolha = int(input(">> "))
                if escolha == 4:
                    raise self.CancelarErro
                else:
                    return colunas.get(escolha)
            except ValueError:
                print("\nEscolha inválida.\n")

    def __listar(self):
        """Lista e escolhe um ID da tabela de empresas"""
        self.cursor.execute(
            "SELECT * FROM Empresas"
        )
        lista_ids = []
        while True:
            for linha in self.cursor.fetchall():
                print(*linha, sep=" - ")
            escolha = input("Escolha um ID de empresa ou pressione ENTER para cancelar: ")
            if escolha == "":
                raise self.CancelarErro
            try:
                escolha = int(escolha)
                if escolha not in lista_ids:
                    print("\nID inexistente...")
                    funcoes.continuar()
                    continue
                return escolha
            except ValueError:
                raise self.ValorInvalidoErro("\nID deve ser um número inteiro positivo...")


class Voos(BancoDados):
    def __init__(self):
        super().__init__()

    def registrar(self):
        """Registra um voo no banco de dados."""
        self.cursor.execute(
            "INSERT INTO Voos(DATA_SAIDA, HORA_SAIDA, COD_AEROPORTO_DECOLAGEM, COD_AEROPORTO_DESTINO,"
            "NUMERO_PASSAGEIROS, ASSENTOS_DISPONIVEIS, CARGA_CARREGADA, COD_AERONAVE, DATA_CHEGADA,"
            "HORA_CHEGADA, NATUREZA_DO_VOO, COD_EMPRESA)"
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                self.__data_saida(), self.__data_saida(), self.__aeroporto_decolagem(), self.__aeroporto_destino(),
                self.__passageiros(), self.__assentos(), self.__carga(), self.__aeronave(), self.__data_chegada(),
                self.__hora_chegada(), self.__natureza(), self.__empresa()
            )
        )
        self.conexao.commit()

    def atualizar(self):
        """Atualiza um voo do banco de dados."""
        codigo = self.__listar()
        coluna = self.__colunas()
        self.cursor.execute(
            f"UPDATE Voos SET {coluna[0]}=? WHERE COD_VOO=?", (coluna[1](), codigo)
        )
        self.conexao.commit()

    def deletar(self):
        """Deleta um voo do banco de dados."""
        codigo = self.__listar()
        while True:
            confirmacao = input(
                f"Você está prester a deleter o voo Código-{codigo}, "
                f"têm certeza desta ação? [ S / N ]"
            )
            if confirmacao.lower() == "s":
                break
            elif confirmacao.lower() == "n":
                raise self.CancelarErro
            else:
                print("\nEscolha inválida.\n")
        self.cursor.execute(
            f"DELETE FROM Voos WHERE COD_VOO={codigo}"
        )
        self.conexao.commit()

    def relatorio_aeroporto(self):
        self.cursor.execute(
            "SELECT * FROM Voos WHERE COD_AEROPORTO_DECOLAGEM=?"
        )

    def __data_saida(self):
        """Entrada da data de saída do voo."""
        data_saida = input("Data de Saída: ")
        if data_saida == "":
            raise self.ValorNuloErro("A data de saída não foi preenchida.")
        return data_saida

    def __hora_saida(self):
        """Entrada da hora de saída do voo."""
        hora_saida = input("Hora de Saída: ")
        if hora_saida == "":
            raise self.ValorNuloErro("A hora de saída não foi preenchida.")
        return hora_saida

    def __aeroporto_decolagem(self):
        """Entrada do aeroporto de decolagem do voo."""
        try:
            aeroporto_decolagem = int(input("ID do aeroporto de decolagem: "))
            lista_ids = [
                codigo[0] for codigo in self.cursor.execute(
                    "SELECT COD_AEROPORTO FROM Aeroportos"
                ).fetchall()
            ]
            if aeroporto_decolagem not in lista_ids:
                raise self.ValorInvalidoErro("O aeroporto em questão não existe...")
            else:
                return aeroporto_decolagem
        except ValueError:
            raise self.ValorInvalidoErro("ID deve ser um número inteiro positivo...")

    def __aeroporto_destino(self):
        """Entrada do aeroporto de destino do voo."""
        try:
            aeroporto_destino = int(input("ID do aeroporto de destino: "))
            lista_ids = [
                codigo[0] for codigo in self.cursor.execute(
                    "SELECT COD_AEROPORTO FROM Aeroportos"
                ).fetchall()
            ]
            if aeroporto_destino not in lista_ids:
                raise self.ValorInvalidoErro("O aeroporto em questão não existe...")
            else:
                return aeroporto_destino
        except ValueError:
            raise self.ValorInvalidoErro("ID deve ser um número inteiro positivo...")

    def __passageiros(self):
        """Entrada do número de passageiros no voo."""
        try:
            numero_passageiros = int(input("Número de Passageiros: "))
            if numero_passageiros < 0:
                raise self.ValorInvalidoErro("O número de passageiros deve ser um número positivo.")
            return numero_passageiros
        except ValueError:
            raise ValueError("O número de passageiros deve ser um número inteiro.")

    def __assentos(self):
        """Entrada dos assentos disponíveis no voo."""
        try:
            assentos_disponiveis = int(input("Assentos Disponíveis: "))
            if assentos_disponiveis < 0:
                raise self.ValorInvalidoErro("O número de assentos disponíveis deve ser um número positivo.")
            return assentos_disponiveis
        except ValueError:
            raise ValueError("O número de assentos disponíveis deve ser um número inteiro.")

    def __carga(self):
        """Entrada da carga carregada no voo."""
        try:
            carga = float(input("Carga Carregada: "))
            if carga < 0:
                raise self.ValorInvalidoErro("A carga carregada deve ser um número positivo.")
            return carga
        except ValueError:
            raise ValueError("A carga carregada deve ser um número real.")

    def __aeronave(self):
        """Entrada da aeronave do voo."""
        try:
            aeronave = int(input("ID da aeronave do voo: "))
            lista_ids = [
                codigo[0] for codigo in self.cursor.execute(
                    "SELECT COD_AERONAVE FROM Aeronaves"
                ).fetchall()
            ]
            if aeronave not in lista_ids:
                raise self.ValorInvalidoErro("A aeronave em questão não existe...")
            else:
                return aeronave
        except ValueError:
            raise self.ValorInvalidoErro("ID deve ser um número inteiro positivo...")

    def __data_chegada(self):
        """Entrada da data de chegada do voo."""
        data_chegada = input("Data de Chegada: ")
        if data_chegada == "":
            raise self.ValorNuloErro("A data de chegada não foi preenchida.")
        return data_chegada

    def __hora_chegada(self):
        """Entrada da hora de chegada do voo."""
        hora_chegada = input("Hora de Chegada: ")
        if hora_chegada == "":
            raise self.ValorNuloErro("A hora de chegada não foi preenchida.")
        return hora_chegada

    def __natureza(self):
        """Entrada da natureza do voo."""
        natureza = input("Natureza do voo: ")
        if natureza == "":
            raise self.ValorNuloErro("Natureza do voo não foi preenchida.")
        return natureza

    def __empresa(self):
        """Entrada da empresa do voo."""
        try:
            empresa = int(input("ID da empresa do voo: "))
            lista_ids = [
                codigo[0] for codigo in self.cursor.execute(
                    "SELECT COD_EMPRESA FROM Empresas"
                ).fetchall()
            ]
            if empresa not in lista_ids:
                raise self.ValorInvalidoErro("A empresa em questão não existe...")
            else:
                return empresa
        except ValueError:
            raise self.ValorInvalidoErro("ID deve ser um número inteiro positivo...")

    def __colunas(self):
        """Seleção de colunas e as suas respetivas entradas."""
        colunas = {
            1: ["DATA_SAIDA", self.__data_saida],
            2: ["HORA_SAIDA", self.__hora_saida],
            3: ["COD_AEROPORTO_DECOLAGEM", self.__aeroporto_decolagem],
            4: ["COD_AEROPORTO_DESTINO", self.__aeroporto_destino],
            5: ["NUMERO_PASSAGEIROS", self.__passageiros],
            6: ["ASSENTOS_DISPONIVEIS", self.__assentos],
            7: ["CARGA_CARREGADA", self.__carga],
            8: ["COD_AERONAVE", self.__aeronave],
            9: ["DATA_CHEGADA", self.__data_chegada],
            10: ["HORA_CHEGADA", self.__hora_chegada],
            11: ["NATUREZA_DO_VOO", self.__natureza],
            12: ["COD_EMPRESA", self.__empresa]
        }
        while True:
            print(
                "Escolha qual coluna modificar:\n"
                "[1] - Data de Saída\n"
                "[2] - Hora de Saída\n"
                "[3] - Aeroporto de Decolagem\n"
                "[4] - Aeroporto de Destino\n"
                "[5] - Número de Passageiros\n"
                "[6] - Assentos Disponíveis\n"
                "[7] - Carga Carregada\n"
                "[8] - Aeronave\n"
                "[9] - Data de Chegada\n"
                "[10] - Hora de Chegada\n"
                "[11] - Natureza do Voo\n"
                "[12] - Empresa\n"
                "[13] - Retornar / Sair"
            )
            try:
                escolha = int(input(">> "))
                if escolha == 4:
                    raise self.CancelarErro
                else:
                    return colunas.get(escolha)
            except ValueError:
                print("\nEscolha inválida.\n")

    def __listar(self):
        """Lista e escolhe um ID da tabela de voos"""
        self.cursor.execute(
            "SELECT * FROM Voos"
        )
        lista_ids = []
        while True:
            for linha in self.cursor.fetchall():
                print(*linha, sep=" - ")
            escolha = input("Escolha um ID de voo ou pressione ENTER para cancelar: ")
            if escolha == "":
                raise self.CancelarErro
            try:
                escolha = int(escolha)
                if escolha not in lista_ids:
                    print("\nID inexistente...")
                    funcoes.continuar()
                    continue
                return escolha
            except ValueError:
                raise self.ValorInvalidoErro("\nID deve ser um número inteiro positivo...")
