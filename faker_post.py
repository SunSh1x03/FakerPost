"""Ferramentas para gerar credenciais falsas e enviá-las para um endpoint HTTP.

O módulo pode ser utilizado como script através da linha de comando. Ele
aproveita a biblioteca Faker para criar combinações de usuário/senha, monta um
conjunto coerente de cabeçalhos HTTP e realiza uma requisição POST para a URL
informada.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from dataclasses import dataclass
from typing import Dict

import requests
from faker import Faker
from requests import Response

faker = Faker()


@dataclass
class FakeRequest:
    """Estrutura que representa os dados e cabeçalhos gerados."""

    data: Dict[str, str]
    headers: Dict[str, str]


def generate_fake_request() -> FakeRequest:
    """Gera um conjunto de dados falso para autenticação."""

    name = f"{faker.first_name()}.{faker.last_name()}"
    password = faker.password()
    country = faker.country()
    user_agent = faker.user_agent()

    return FakeRequest(
        data={"username": name, "password": password},
        headers={"User-Agent": user_agent, "Country": country},
    )


def send_fake_post(url: str, fake_request: FakeRequest, *, allow_redirects: bool, timeout: float) -> Response:
    """Realiza uma requisição POST com os dados fornecidos."""

    logging.debug("Enviando POST para %s com payload %s e cabeçalhos %s", url, fake_request.data, fake_request.headers)
    response = requests.post(
        url,
        data=fake_request.data,
        headers=fake_request.headers,
        allow_redirects=allow_redirects,
        timeout=timeout,
    )
    logging.info("Resposta %s recebida de %s", response.status_code, url)
    return response


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Constroi o parser de argumentos e realiza o parse da linha de comando."""

    parser = argparse.ArgumentParser(
        description="Gera credenciais falsas com Faker e envia uma requisição POST para um endpoint HTTP.",
    )
    parser.add_argument(
        "url",
        nargs="?",
        default="https://example.com/login",
        help="Endpoint para o qual as requisições POST serão enviadas.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Quantidade de requisições a serem enviadas. Use 0 para executar continuamente.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.05,
        help="Intervalo em segundos entre as requisições.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Tempo máximo de espera da resposta em segundos.",
    )
    parser.add_argument(
        "--allow-redirects",
        action="store_true",
        help="Permite seguir redirecionamentos HTTP ao enviar a requisição.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas exibe as cargas geradas sem realizar requisições.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostra logs detalhados durante a execução.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Função principal do script."""

    args = parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    execution_count = 0
    total = args.count if args.count > 0 else None

    logging.info("Iniciando envio de requisições falsas.")

    try:
        while total is None or execution_count < total:
            fake_request = generate_fake_request()

            if args.dry_run:
                logging.info("Dry-run ativo. Payload: %s, Headers: %s", fake_request.data, fake_request.headers)
            else:
                try:
                    send_fake_post(
                        args.url,
                        fake_request,
                        allow_redirects=args.allow_redirects,
                        timeout=args.timeout,
                    )
                except requests.RequestException as exc:
                    logging.error("Falha ao enviar requisição: %s", exc)

            execution_count += 1

            if total is None or execution_count < total:
                time.sleep(max(0.0, args.delay))
    except KeyboardInterrupt:
        logging.info("Execução interrompida pelo usuário.")
        return 130

    logging.info("Execução finalizada. %s requisição(ões) processada(s).", execution_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
