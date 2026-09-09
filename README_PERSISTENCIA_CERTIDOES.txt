CORRECAO - PERSISTENCIA PERMANENTE DAS CERTIDOES

IMPORTANTE: esta versao NAO inclui backend/omega.db justamente para impedir que uma
instalacao nova sobrescreva a base de dados existente.

O backend cria/migra as tabelas automaticamente na inicializacao.

CORRECOES:
1. Toda consulta estadual cria/atualiza a fotografia atual em certidoes.
2. Toda consulta gera uma linha permanente em consultas_certidoes e certidoes_historico.
3. O historico permanente e append-only: UPDATE/DELETE sao bloqueados por triggers.
4. PDFs sao salvos com nome unico e hash SHA-256.
5. O banco gera backup permanente apos cada consulta registrada.
6. Bancos antigos que possuem consultas mas nao possuem a linha atual em certidoes sao
   reconstruidos automaticamente a partir da ultima consulta.
7. A tela de Certidoes carrega os registros persistidos ao entrar novamente na area.
8. A empresa selecionada fica gravada no navegador e e restaurada ao voltar para Certidoes.
9. Sem empresa selecionada, a tela mostra todas as certidoes atuais persistidas.

INSTALACAO:
- Substitua os arquivos do projeto pelos arquivos desta versao.
- NAO apague nem substitua backend/omega.db.
- NAO apague a pasta storage/ se ela ja possuir PDFs/backup.
- Reinicie o backend uma vez para executar a migracao.
- Atualize o frontend com recarregamento forcado do navegador.
