from classes import Aeronaves, Aeroportos, Empresas, Voos
from funcoes import *


def voos():
    tabela = Voos()
    menu = {"1": tabela.registrar, "2": tabela.atualizar, "3": tabela.deletar, "4": main}
    print("Menu de Voos:\n"
          "[1] - Registrar\n"
          "[2] - Atualizar\n"
          "[3] - Deletar\n"
          "[4] - Voltar")
    escolha = input(">> ")
    print()
    if escolha not in menu.keys():
        print("Escolha inválida.")
        continuar()
        voos()
    elif escolha == "4":
        return main()
    else:
        try:
            return menu.get(escolha)()
        except ValueError as erro:
            print("\n", erro)
            continuar()
            return voos()
        except tabela.ValorNuloErro as erro:
            print("\n", erro)
            continuar()
            return voos()
        except tabela.ValorInvalidoErro as erro:
            print("\n", erro)
            continuar()
            return voos()
        except tabela.CancelarErro:
            return voos()


def empresas():
    tabela = Empresas()
    menu = {"1": tabela.registrar, "2": tabela.atualizar, "3": tabela.deletar, "4": main}
    print("Menu de Empresas:\n"
          "[1] - Registrar\n"
          "[2] - Atualizar\n"
          "[3] - Deletar\n"
          "[4] - Voltar")
    escolha = input(">> ")
    print()
    if escolha not in menu.keys():
        print("Escolha inválida.")
        continuar()
        empresas()
    elif escolha == "4":
        return main()
    else:
        try:
            return menu.get(escolha)()
        except ValueError as erro:
            print("\n", erro)
            continuar()
            return empresas()
        except tabela.ValorNuloErro as erro:
            print("\n", erro)
            continuar()
            return empresas()
        except tabela.ValorInvalidoErro as erro:
            print("\n", erro)
            continuar()
            return empresas()
        except tabela.CancelarErro:
            return empresas()


def aeroportos():
    tabela = Aeroportos()
    menu = {"1": tabela.registrar, "2": tabela.atualizar, "3": tabela.deletar, "4": main}
    print("Menu de Aeroportos:\n"
          "[1] - Registrar\n"
          "[2] - Atualizar\n"
          "[3] - Deletar\n"
          "[4] - Voltar")
    escolha = input(">> ")
    print()
    if escolha not in menu.keys():
        print("Escolha inválida.")
        continuar()
        aeroportos()
    elif escolha == "4":
        return main()
    else:
        try:
            return menu.get(escolha)()
        except ValueError as erro:
            print("\n", erro)
            continuar()
            return aeroportos()
        except tabela.ValorNuloErro as erro:
            print("\n", erro)
            continuar()
            return aeroportos()
        except tabela.ValorInvalidoErro as erro:
            print("\n", erro)
            continuar()
            return aeroportos()
        except tabela.CancelarErro:
            return aeroportos()


def aeronaves():
    tabela = Aeronaves()
    menu = {"1": tabela.registrar, "2": tabela.atualizar, "3": tabela.deletar, "4": main}
    print("Menu de Aeronaves:\n"
          "[1] - Registrar\n"
          "[2] - Atualizar\n"
          "[3] - Deletar\n"
          "[4] - Voltar")
    escolha = input(">> ")
    print()
    if escolha not in menu.keys():
        print("Escolha inválida.")
        continuar()
        aeronaves()
    elif escolha == "4":
        return main()
    else:
        try:
            return menu.get(escolha)()
        except ValueError as erro:
            print("\n", erro)
            continuar()
            return aeronaves()
        except tabela.ValorNuloErro as erro:
            print("\n", erro)
            continuar()
            return aeronaves()
        except tabela.ValorInvalidoErro as erro:
            print("\n", erro)
            continuar()
            return aeronaves()
        except tabela.CancelarErro:
            return aeronaves()


def main():
    menu = {"1": aeronaves, "2": aeroportos, "3": empresas, "4": voos, "5": None}
    print("Menu Principal:\n"
          "[1] - Aeronaves\n"
          "[2] - Aeroportos\n"
          "[3] - Empresas\n"
          "[4] - Voos\n"
          "[5] - Sair")
    escolha = input(">> ")
    print()
    if escolha not in menu.keys():
        print("Escolha inválida.")
        continuar()
        main()
    elif escolha == "5":
        return None
    else:
        return menu.get(escolha)()


if __name__ == '__main__':
    main()
