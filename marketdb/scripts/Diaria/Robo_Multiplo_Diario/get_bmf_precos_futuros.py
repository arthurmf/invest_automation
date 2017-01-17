def get_bmf_precos_futuros(ano, mes, dia):

    import pandas as pd
    import pymysql as db
    import datetime

    connection = db.connect('localhost', user='root', passwd='root', db='projeto_inv')

    #Robo BMF PREÇOS FUTUROS
    dataBusca = dia+"/"+mes+"/"+ano
    endereco = "http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/Ajustes1.asp?txtData="
    endereco_data = endereco + dataBusca

    dadospd = pd.read_html(endereco_data, thousands=".")

    #Pegar a última tabela
    dadospd = dadospd[len(dadospd)-1]

    #Mudar nome tabela
    dadospd.columns =dadospd.iloc[0,:]

    #Tirar primeira linha
    dadospd = dadospd.iloc[1:len(dadospd),:]

    #Padronizar nome "Mercadorias"
    for i in range(len(dadospd["Mercadoria"])):
        dadospd["Mercadoria"].iloc[i]=str(dadospd["Mercadoria"].iloc[i])
        if dadospd["Mercadoria"].iloc[i]=='nan' :
            dadospd["Mercadoria"].iloc[i]=dadospd["Mercadoria"].iloc[i-1]


    #Padronizar nomes das colunas

    dadospd.columns=[
    "mercadoria",
    "vencimento",
    "preco_ajuste_anterior",
    "preco_ajuste_atual",
    "variacao",
    "valor_ajuste_por_contrato"
    ]

    # Trocar virgula por ponto

    lista_virgula=[
    "preco_ajuste_anterior",
    "preco_ajuste_atual",
    "variacao",
    "valor_ajuste_por_contrato"
    ]

    for coluna in lista_virgula:
        dadospd[coluna]=[str(linha).replace(".","") for linha in dadospd[coluna] ]

    dadospd = dadospd.replace({',': '.'}, regex=True)

    # Criar coluna com data_referencia
    dadospd["data_referencia"] = ano + mes + dia

    ## Criar coluna com data_bd para a data de inserção no BD

    horario_bd = datetime.datetime.now()
    dadospd["data_bd"] = horario_bd


    # Salvar na base de dados
    pd.io.sql.to_sql(dadospd, name='bmf_ajustes_pregao',
                     con = connection,
                     if_exists = "append",
                     flavor = 'mysql',
                     index = 0)