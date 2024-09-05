import os
import pandas as pd
import pdfkit as pdf
from jinja2 import Environment, FileSystemLoader


class geracaoFaturas:

    def __init__(self,wkhtml_path):
        """
        This program creates reports bills.
        
        """
        self.wkhtml_path = wkhtml_path 
        print("Class Started.")


    def _get_environment(self,filepath,filename="template_bill.html"):
        """
        Load Environment Jinja Template

        Params
        ---------
        path: str
        
        Returns
        ---------
        template: str
            template file address
        root: str
            folders address         
        
        """
        root = os.path.abspath(filepath)
        env = Environment(loader = FileSystemLoader(root))
        template = env.get_template(filename)
        return root,template
        
        
    def _clean_environment(self,filepath,pattern="historico_fatura"):
        """
        Clean environment with the html file created.

        Params
        ---------
        path: str
        
        Returns
        ---------
        template: str
            template file address
        root: str
            folders address         
        
        """
        filepath = os.path.abspath(filepath)
        for file in os.listdir(filepath):
            if pattern in file and '.html' in file:
                os.remove(os.path.join(filepath,file))
            else:
                pass



    def _get_variables(self,df_account):
        """
        Get all variables needed to render template

        Params
        ---------
        df_account: pandas.DataFrame
        
        Returns
        ---------
        name: str 
        cpf: str
        endereco: str
        telefone: str
        cidade: str
        estado: str
        cep: str
        df_dict: dict 
        df_colunas: list
        quebras_dict: dict         
        
        """
        account = df_account["NR_CONTA"][0]
        name = df_account["NOME_TITULAR"][0]
        cpf = df_account["NR_CPF_CNPJ"][0]
        endereco = df_account["ENDERECO"][0]
        telefone = df_account["TELEFONE_CELULAR"][0]
        cidade = df_account["CIDADE"][0]
        estado = df_account["UF"][0]
        cep = df_account["CEP"][0]

        df_account_final = df_account[["DT_VENCIMENTO","VL_TOTAL_FATURA","NR_CARTAO","DT_TRANSACAO","ST_DEB_CRED","DS_TRANSACAO","VL_TRANSACAO"]]

        df_dict = df_account_final.to_dict("records")
        df_colunas = df_account_final.columns
        
        quebras = [i for i in range(0,len(df_account_final),24)]
        quebras_2 = quebras[1:]
        quebras_2.append(len(df_account_final)+1)
        data = []
        data.append(quebras)
        data.append(quebras_2)
        quebras = pd.DataFrame(data).transpose()
        quebras.columns=['quebras_1', 'quebras_2']
        quebras_dict = quebras.to_dict("records")

        return account,name,cpf,endereco,telefone,cidade,estado,cep,df_dict,df_colunas,quebras_dict 

    def _render_template(
            self,
            root,
            template,
            account,
            _nome,
            _cpf_mask,
            _endereco,
            _telefone,
            _cidade,
            _estado,
            _cep,
            _df_dict,
            _df_colunas,
            _quebras_dict,
            account_mask
        ):
        """
        Render templates File to HTML of all contents of an account.

        Params
        ---------
        root:str
            folder path
        template: str
            template path
        account:str
        _nome: str 
        _cpf: str
        _endereco: str
        _telefone: str
        _cidade: str
        _estado: str
        _cep: str
        _df_dict: dict 
        _df_colunas: list
        _quebras_dict: dict

        Returns
        ---------
        name: str

        """
        name = f"historico_fatura_{str(account)}.html"
        filename = os.path.join(root, name)
        with open(filename, 'w', encoding='utf-8') as fh:
            fh.write(template.render(
                conta = account_mask,
                nome = _nome,
                cpf = _cpf_mask,
                endereco = _endereco,
                telefone = _telefone,
                cidade = _cidade,
                estado = _estado,
                cep = _cep,
                df_dict = _df_dict,
                df_colunas = _df_colunas,
                quebras_dict = _quebras_dict,
                image_path = "marca_chess.png"
            )
        )
        return name
    

    def _get_pdf(
            self,
            root,
            account,
            name
        ):
        """
        Render PDF file from htmls files.

        Params
        ---------
        account:int or str
            account
        name: str 
            name of the html created
        wkhtml_path: str
            instalation file executer path
        
        Returns
        ---------
        name: str        
        """
        config = pdf.configuration(wkhtmltopdf=self.wkhtml_path)
        final_name = os.path.join(root, f"historico_fatura_{str(account)}.pdf")
        print(final_name)
        pdf.from_file(
            os.path.join(root, name), 
            final_name,
            configuration=config,
            options = {
                'enable-local-file-access': True,
                'page-size'    : 'A4',
                'margin-top'   : '0.40in',
                'margin-right' : '0.45in',
                'margin-bottom': '0.45in',
                'margin-left'  : '0.45in',
                'encoding': "UTF-8" 
                }
            )
        return 'PDF CREATED!'


    def __call__(self,df):
        """
        Pass an account number and generate a file pdf from its bills

        Params
        --------
        account_number:int
        
        """       

        root, template = self._get_environment('')
        account,name,cpf,endereco,telefone,cidade,estado,cep,df_dict,df_colunas,quebras_dict = self._get_variables(df)
        cpf_mask = str(cpf)[:3]+"*****"+str(cpf)[8:]
        account_mask = str(account)[:3]+"********"+str(account)[:-3]
        _name = self._render_template(root,template,account,name,cpf_mask,endereco,telefone,cidade,estado,cep,df_dict,df_colunas,quebras_dict,account_mask)
        self._get_pdf(root, account,_name)
        self._clean_environment('')
