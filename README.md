# Projeto de Geração de Faturas

---

## Descrição

Este projeto tem como objetivo gerar faturas em formato PDF a partir de dados fornecidos em um formato tabular (como um DataFrame do Pandas). Ele usa templates HTML para formatar o conteúdo da fatura e converte esses templates para PDF utilizando a biblioteca **pdfkit** (que depende do **wkhtmltopdf** para funcionar). Além disso, o projeto permite a criação de dados fictícios para teste.

---

## Estrutura do Projeto

bills/
│
├── bill_engine.py              # Script principal que gera as faturas
├── fake_data.py                # Script para gerar dados falsos para testes
├── template_bill.html          # Template HTML usado para renderizar as faturas
├── wkhtmltopdf.exe             # Executável do wkhtmltopdf para Windows (converter HTML para PDF)
├── marca_chess.png             # Logo/imagem utilizada no template da fatura
└── historico_fatura_123456.pdf # Exemplo de uma fatura gerada em PDF


---

## Dependências

Para rodar este projeto, você precisará das seguintes bibliotecas:

- **Python 3.x**
- **pandas** (`pip install pandas`)
- **pdfkit** (`pip install pdfkit`)
- **jinja2** (`pip install jinja2`)
- **wkhtmltopdf** (Necessário para converter HTML em PDF)

Certifique-se de que o caminho para o `wkhtmltopdf.exe` esteja configurado corretamente ao instanciar a classe.

---

## Instalação

1. Clone ou baixe o repositório.
2. Instale as dependências do Python mencionadas acima.
3. Baixe e configure o `wkhtmltopdf`:
   - No Windows, o executável está incluído na pasta `bills/`.
   - Em outros sistemas operacionais, baixe e configure o **wkhtmltopdf** de acordo com o seu ambiente.

---

## Utilização

### Gerando Faturas

O processo de geração de faturas é gerenciado pela classe `geracaoFaturas` contida no arquivo `bill_engine.py`. Para utilizá-la:

1. Importe e instancie a classe `geracaoFaturas`, fornecendo o caminho para o `wkhtmltopdf.exe` (no caso de uso no Windows).
   
   ```python
   from bill_engine import geracaoFaturas
   
   caminho_wkhtml = r'caminho/para/wkhtmltopdf.exe'
   gerador = geracaoFaturas(wkhtml_path=caminho_wkhtml)```


### Explicação das Funções

__init__: Inicia a classe e configura o caminho para o wkhtmltopdf.
_get_environment: Carrega o template HTML a partir de um diretório específico.
_clean_environment: Remove arquivos HTML temporários gerados após a criação do PDF.
_get_variables: Extrai as variáveis necessárias para a renderização da fatura a partir do DataFrame.
_render_template: Gera o arquivo HTML da fatura baseado no template e nas variáveis extraídas.
_get_pdf: Converte o arquivo HTML gerado para PDF.
__call__: Executa todo o processo de geração de faturas chamando as funções internas na sequência correta.


### Gerando Dados Falsos para Testes

O script fake_data.py contém a função get_fake_data, que gera um DataFrame com dados fictícios para testar o pipeline de geração de faturas.

   ```python
  Copiar código
  from fake_data import get_fake_data
  df = get_fake_data()```

Os dados incluem informações sobre a conta, como CPF, nome do titular, endereço e transações financeiras.

### Modificações e Personalizações
* Template: O arquivo template_bill.html pode ser modificado para personalizar a aparência da fatura. Este template utiliza a sintaxe do Jinja2 para preencher os dados dinâmicos.
* Imagens: A imagem marca_chess.png é inserida na fatura. Pode ser alterada conforme a necessidade.

## Observações
O script foi projetado para rodar em Windows, mas pode ser adaptado para outros sistemas operacionais alterando a forma como o caminho para o wkhtmltopdf é tratado.
O PDF gerado é salvo no mesmo diretório em que o script é executado.
