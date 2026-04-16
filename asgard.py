from urllib.request import urlopen, Request
from pyfiglet import figlet_format
from colorama import Fore, Style, init
import time
import re
import socket

init()


def mostrar_titulo():
    print(Fore.CYAN + figlet_format("ASGARD") + Style.RESET_ALL)


def pegar_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    html = response.read().decode('utf-8', errors='ignore')
    return response, html


def analisar_site(url):
    try:
        inicio = time.time()

        response, html = pegar_html(url)

        fim = time.time()

        print(Fore.GREEN + "\n=== RESULTADO ===" + Style.RESET_ALL)

        print(Fore.BLUE + "Status:" + Style.RESET_ALL, response.status)

        print(Fore.BLUE + "Tempo de resposta:" + Style.RESET_ALL, f"{fim - inicio:.2f}s")

        if url.startswith("https"):
            print(Fore.BLUE + "Segurança:" + Style.RESET_ALL, Fore.GREEN + "HTTPS (seguro)" + Style.RESET_ALL)
        else:
            print(Fore.BLUE + "Segurança:" + Style.RESET_ALL, Fore.RED + "HTTP (não seguro)" + Style.RESET_ALL)

        host = url.replace("https://", "").replace("http://", "").split("/")[0]

        try:
            ip = socket.gethostbyname(host)
            print(Fore.BLUE + "IP do site:" + Style.RESET_ALL, ip)
        except:
            print(Fore.BLUE + "IP do site:" + Style.RESET_ALL, "Não encontrado")

        servidor = response.headers.get("Server")
        print(Fore.BLUE + "Servidor:" + Style.RESET_ALL, servidor if servidor else "Não informado")

        print(Fore.BLUE + "Tamanho (bytes):" + Style.RESET_ALL, len(html))

        links = re.findall(r'<a\s+href=', html)
        print(Fore.BLUE + "Links:" + Style.RESET_ALL, len(links))

        imagens = re.findall(r'<img', html)
        print(Fore.BLUE + "Imagens:" + Style.RESET_ALL, len(imagens))

        titulo_site = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if titulo_site:
            print(Fore.BLUE + "Título:" + Style.RESET_ALL, titulo_site.group(1))

        print(Fore.MAGENTA + "\n=== ANÁLISE DE SEGURANÇA ===" + Style.RESET_ALL)

        if "login" in html.lower():
            print(Fore.YELLOW + "Possível página de login detectada" + Style.RESET_ALL)

        if "password" in html.lower():
            print(Fore.YELLOW + "Campo de senha detectado" + Style.RESET_ALL)

        if not url.startswith("https"):
            print(Fore.RED + "Site não usa HTTPS!" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + "\nErro:" + Style.RESET_ALL, e)


def menu():
    while True:
        print(Fore.CYAN + "\n=== MENU ===" + Style.RESET_ALL)
        print("1 - Analisar site")
        print("2 - Sair")

        op = input(Fore.YELLOW + "Escolha: " + Style.RESET_ALL)

        if op == "1":
            url = input(Fore.YELLOW + "Digite a URL (com https://): " + Style.RESET_ALL)
            analisar_site(url)

        elif op == "2":
            print(Fore.RED + "Saindo..." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Opção inválida!" + Style.RESET_ALL)


# EXECUÇÃO
mostrar_titulo()
menu()