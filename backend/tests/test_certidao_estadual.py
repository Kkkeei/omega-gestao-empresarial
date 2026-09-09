from app.services.sefaz_pe_service import analisar_certidao, formatar_cnpj, validar_cnpj


def test_cnpj_estadual():
    assert validar_cnpj("50.410.847/0001-12")
    assert formatar_cnpj("50410847000112") == "50.410.847/0001-12"


def test_classificacao_conservadora():
    assert analisar_certidao("CERTIDAO NEGATIVA DE DEBITOS", "x.pdf")["situacao"] == "REGULAR"
    assert analisar_certidao("CERTIDAO POSITIVA COM EFEITOS DE NEGATIVA", "x.pdf")["situacao"] == "POSITIVA COM EFEITOS DE NEGATIVA"
    assert analisar_certidao("CERTIDAO POSITIVA DE DEBITOS", "x.pdf")["situacao"] == "IRREGULAR"
    assert analisar_certidao("CERTIDAO DE REGULARIDADE FISCAL", "x.pdf")["situacao"] == "NAO IDENTIFICADO"


def test_nome_arquivo_fallback():
    assert analisar_certidao("CERTIDAO DE REGULARIDADE FISCAL", "RelatorioCertidaoRegularidadeFiscalInscritoRegular.pdf")["situacao"] == "REGULAR"
    assert analisar_certidao("CERTIDAO DE REGULARIDADE FISCAL", "RelatorioCertidaoRegularidadeFiscalInscritoIrregular.pdf")["situacao"] == "IRREGULAR"
