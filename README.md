# FakerPost

Ferramenta simples para gerar credenciais falsas com a biblioteca [Faker](https://faker.readthedocs.io/en/master/)
e enviá-las para um endpoint HTTP através de requisições `POST`. O objetivo é
facilitar testes de fluxos de autenticação e simulações de carga utilizando
dados fictícios.

## Pré-requisitos

- Python 3.9 ou superior
- [pip](https://pip.pypa.io/) para instalar dependências

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

> Caso não exista um arquivo `requirements.txt`, instale manualmente:
> `pip install faker requests`.

## Uso básico

Execute o script `faker_post.py` passando a URL desejada. Por padrão, o script
envia apenas uma requisição para `https://example.com/login`.

```bash
python faker_post.py https://httpbin.org/post
```

### Argumentos disponíveis

| Opção              | Descrição                                                                 | Valor padrão                |
|--------------------|---------------------------------------------------------------------------|-----------------------------|
| `url`              | Endpoint que receberá a requisição `POST`.                               | `https://example.com/login` |
| `--count`          | Número de requisições a enviar. Use `0` para executar continuamente.      | `1`                         |
| `--delay`          | Intervalo (em segundos) entre as requisições.                            | `0.05`                      |
| `--timeout`        | Tempo máximo de espera pela resposta (em segundos).                      | `10.0`                      |
| `--allow-redirects`| Segue redirecionamentos HTTP caso presentes.                              | Desativado                  |
| `--dry-run`        | Não envia requisições; apenas exibe os dados e cabeçalhos gerados.        | Desativado                  |
| `--verbose`        | Exibe logs detalhados, útil para depuração.                               | Desativado                  |

#### Exemplo enviando múltiplas requisições

```bash
python faker_post.py https://httpbin.org/post --count 5 --delay 0.5 --verbose
```

#### Exemplo sem realizar requisições (dry-run)

```bash
python faker_post.py --dry-run
```

## Execução contínua

O script `looping.sh` fornece um exemplo de execução contínua, chamando
`faker_post.py` em um loop infinito. Para utilizá-lo:

```bash
bash looping.sh
```

Use `Ctrl + C` para interromper a execução.

## Observações

- Os dados gerados são completamente fictícios e não devem ser utilizados em
  ambientes de produção sem autorização.
- Ajuste a URL alvo e os cabeçalhos conforme necessário para o seu cenário.
- Considere adicionar mecanismos de limitação de taxa quando executar testes
  contra serviços sensíveis.

## Contribuindo

Sinta-se à vontade para abrir *issues* ou enviar *pull requests* com melhorias.
