import pandas as pd
import numpy as np

def get_fake_data():
    """
    This functions generate fake data to test the Project. 

    """
    dados_cadastrais = {
        'NR_CONTA': 123456,
        'NR_CPF_CNPJ': '000.000.000-00',
        'ID_CONTA_EMPR': 987654,
        'NOME_TITULAR': 'Fulano de Tal',
        'ENDERECO': 'Rua Exemplo, 123',
        'BAIRRO': 'Bairro Exemplo',
        'COMPLEMENTO': 'Apto 101',
        'CEP': '00000-000',
        'CIDADE': 'Cidade Exemplo',
        'EMAIL': 'exemplo@email.com',
        'TELEFONE_CELULAR': '(11) 99999-9999',
        'UF': 'SP'
    }
    num_linhas = 100
    dados_variaveis = {
        'DT_VENCIMENTO': [i.strftime('%Y-%m-%d') for i in pd.date_range('2023-01-01', periods=num_linhas, freq='ME')],
        'VL_TOTAL_FATURA': np.round(np.random.uniform(200, 1500, size=num_linhas),2),
        'ID_TRANSACAO_FATURA': np.random.randint(1000, 9999, size=num_linhas),
        'NR_CARTAO': '123456789123456',
        'DT_TRANSACAO': [i.strftime('%Y-%m-%d') for i in pd.date_range('2023-01-01', periods=num_linhas, freq='D')],
        'ST_DEB_CRED': np.random.choice(['DEB', 'CRED'], size=num_linhas),
        'DS_TRANSACAO': np.random.choice(['Compra', 'Pagamento', 'Transferência'], size=num_linhas),
        'VL_TRANSACAO': np.round(np.random.uniform(10, 1000, size=num_linhas),2),
        'ANO': np.random.randint(2020, 2024, size=num_linhas)
    }

    df = pd.DataFrame(dados_cadastrais, index=range(num_linhas))
    df = pd.concat([df, pd.DataFrame(dados_variaveis)], axis=1)

    return df