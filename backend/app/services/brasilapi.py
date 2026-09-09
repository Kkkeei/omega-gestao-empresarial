import httpx
async def consultar_cnpj(cnpj:str)->dict:
    digits=''.join(ch for ch in cnpj if ch.isdigit())
    async with httpx.AsyncClient(timeout=15) as client:
        r=await client.get(f'https://brasilapi.com.br/api/cnpj/v1/{digits}');r.raise_for_status();return r.json()
def mapear_brasilapi(d:dict)->dict:
    return {
      'razao_social':d.get('razao_social'),'nome_fantasia':d.get('nome_fantasia'),'data_abertura':d.get('data_inicio_atividade'),
      'natureza_juridica':d.get('natureza_juridica'),'porte':d.get('porte'),'capital_social':d.get('capital_social'),
      'cnae_principal':str(d.get('cnae_fiscal')) if d.get('cnae_fiscal') is not None else None,
      'logradouro':d.get('logradouro'),'numero':d.get('numero'),'complemento':d.get('complemento'),'bairro':d.get('bairro'),
      'municipio':d.get('municipio'),'codigo_ibge':str(d.get('codigo_municipio')) if d.get('codigo_municipio') is not None else None,
      'uf':d.get('uf'),'cep':d.get('cep'),'telefone':d.get('ddd_telefone_1') or d.get('ddd_telefone_2')
    }
