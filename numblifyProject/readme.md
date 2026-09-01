# Wiki Corporativa Inteligente na AWS

## Quest 1 — O Mapa dos Arquivos Perdidos

A primeira etapa para  a construção do nosso agente, é identificar os tipos de dados. Analizando a pasta raw, podemos identificar os seguintes tipos de arquivo:

- `ata_reuniao_vendas_sa.pdf`: Um arquivo PDF com camadas de texto, nesse caso o ORD não é necessário .
- `ata_resultados_vendas_novos_dados.png`: Imagem digitalizada de uma ata. Como contém apenas pixels, precisa de OCR..
- `vendas_sa_dados_ficticios_laboratorio.csv`: Arquivo que deve ser tratado como dado estruturado.

---

## Quest 2 — O Portal de Entrada na AWS


Utilizaremos o **Amazon S3** para o armazenamento dos nossos arquivos. Para manter a integridade dos dados da pasta raw/, mandaremos uma cópia desses arquivos para um bucket; assim, a base de dados original nunca será alterada.

O fluxo pode ser coordenado pelo **AWS Step Functions**, acionando funções **AWS Lambda** para identificar o tipo de arquivo e direcionar cada documento para o processamento adequado.

### PDF

Arquivos em PDF, na maioria das vezes, já possuem camada de texto. Portanto, poderemos extrair o conteúdo do arquivo `ata_reuniao_vendas_sa.pdf` diretamente, sem passar por um OCR.

### Imagem

Para extrairmos os dados de uma imagem precisariamos de um OCR. O **Amazon Textract** será utilizado para reconhecer o texto da imagem `ata_resultados_vendas_novos_dados.png` e retornar o conteúdo extraído, em formato de tabela ou JSON, por exemplo.


### CSV

O CSV representa dados estruturados do CRM; por esse motivo, ele deve ser processado como uma tabela, preservando suas colunas e registros. Para essa tarefa, podemos utilizar o **AWS Glue** para catalogar e organizar esses dados, enquanto o conteúdo permanece armazenado no S3.

### Dados processados

Após extrairmos os textos e os normalizarmos, poderíamos armazená-los em uma área separada do S3, em um diretório `processed/`, por exemplo, mantendo a separação entre dados originais e processados.

Em caso de erro, o Step Functions identificaria a etapa que falhou e utilizaríamos o Amazon CloudWatch para registrar logs e métricas para acompanhamento do processamento.

O acesso ao S3 e aos demais serviços seria controlado pelo **AWS IAM**, enquanto o **AWS KMS** poderia proteger os dados armazenados por meio de criptografia.

### Fluxo inicial

```text
Arquivos locais
      |
      v
   Amazon S3
      |
      v
AWS Step Functions
      |
      +--------------------+--------------------+
      |                    |                    |
      v                    v                    v
    PDF                 Imagem                CSV
      |                    |                    |
Extração direta       Amazon Textract       AWS Glue
      |                    |                    |
      +--------------------+--------------------+
                           |
                           v
                    Dados processados
                           |
                           v
                    S3 / metadados
```

---

## Quest 3 — A Relíquia dos Metadados

Depois da extração, os documentos devem ser normalizados para possuir uma estrutura consistente.

Um registro de documento poderia conter:

```json
{
  "documento": "ata_reuniao_vendas_sa.pdf",
  "tipo": "ata_reuniao",
  "data": "2026-03-15",
  "tema": "planejamento comercial",
  "participantes": [],
  "decisoes": [],
  "responsaveis": [],
  "prazos": [],
  "riscos": [],
  "pendencias": [],
  "projetos": [],
  "departamentos": [],
  "confidencialidade": "interno",
  "arquivo_original": "s3://bucket/raw/ata_reuniao_vendas_sa.pdf"
}
```

A limpeza deve remover ruídos de OCR, quebras de linha desnecessárias, espaços duplicados e conteúdos repetidos, sem alterar o significado do documento.

O **Amazon Bedrock** pode auxiliar na identificação de informações como temas, decisões, responsáveis, riscos e próximos passos. Para dados estruturados, o **AWS Glue Data Catalog** pode ajudar na organização e descoberta dos dados.

Os metadados podem ser armazenados no **Amazon DynamoDB**, mantendo uma referência para o arquivo original no S3. Dessa forma, cada informação extraída continua relacionada ao documento de origem.

---

## Quest 4 — O Oráculo da Wiki Inteligente

A solução pode utilizar **Amazon Bedrock Knowledge Bases** para criar uma arquitetura de RAG (Retrieval-Augmented Generation).

Primeiro, os textos processados seriam divididos em trechos menores (*chunks*). Esses trechos seriam transformados em **embeddings**, que representam semanticamente o conteúdo.

Os embeddings seriam armazenados em uma base vetorial. Uma opção seria utilizar **Amazon S3 Vectors**, enquanto outra possibilidade seria utilizar **Amazon OpenSearch Serverless**.

O fluxo de consulta seria:

```text
Usuário
   |
   v
Interface da Wiki
   |
   v
Amazon API Gateway
   |
   v
AWS Lambda
   |
   v
Knowledge Bases
   |
   +--> Busca semântica
   |
   +--> Recuperação dos trechos relevantes
   |
   v
Amazon Bedrock
   |
   v
Resposta fundamentada nos documentos
```

Ao responder uma pergunta do usuário, a busca semântica localizará os trechos mais relevantes, mesmo que os documentos não utilizem exatamente as mesmas palavras da pergunta. Esses trechos serão enviados ao modelo do **Amazon Bedrock**, que produzirá uma resposta baseada no conteúdo recuperado.

A resposta deve apresentar não apenas o resumo, mas também referências aos documentos utilizados, datas, pessoas envolvidas, decisões e possíveis próximos passos. Isso reduz o risco de uma resposta sem rastreabilidade.

### Interface

A Wiki poderia possuir:

- campo de pesquisa em linguagem natural;
- filtros por data, documento, tema e departamento;
- resposta gerada pela IA;
- documentos utilizados como fonte, indicando trecos os páginas relacionadas à resposta;

### Segurança e auditoria

Documentos confidenciais devem possuir controle de acesso adequado, evitando que usuários consultem informações que não têm autorização para visualizar.

O **Amazon Cognito** pode controlar a autenticação dos usuários. O IAM controla permissões entre os serviços, enquanto o KMS protege os dados armazenados.

O **AWS CloudTrail** registra atividades relacionadas aos recursos da AWS e o **Amazon CloudWatch** pode acompanhar logs, erros, métricas e consumo.

---

## Arquitetura Final

```text
                    +------------------+
                    |   Usuário        |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Cognito / Wiki   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | API Gateway      |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | Lambda           |
                    +--------+---------+
                             |
                             v
              +-----------------------------+
              | Bedrock Knowledge Bases     |
              +-------------+---------------+
                            |
                  Busca semântica / RAG
                            |
                            v
                 +-----------------------+
                 | Base vetorial         |
                 | S3 Vectors/OpenSearch |
                 +-----------------------+

Ingestão:

Arquivos --> S3 --> Step Functions
                       |
             +---------+---------+
             |                   |
             v                   v
        Textract             Glue
             |                   |
             +---------+---------+
                       |
                       v
                 Dados processados
                       |
                       v
                    S3 / DynamoDB
                       |
                       v
             Knowledge Bases / RAG
```

## Conclusão

A proposta transforma os arquivos brutos em uma fonte de conhecimento organizada e pesquisável usando apenas serviços AWS.
O **Amazon S3** preserva os documentos, o **Textract** resolve o problema dos arquivos digitalizados, o **AWS Glue** organiza os dados tabulares, o **Step Functions** coordena o processamento e o **Bedrock Knowledge Bases** permite criar a busca semântica e o fluxo de RAG.
A combinação de IAM, KMS, Cognito, CloudWatch e CloudTrail acrescenta segurança, monitoramento e rastreabilidade.
A arquitetura também pode crescer conforme novos documentos sejam adicionados, mantendo os arquivos originais preservados e permitindo que a Wiki seja continuamente atualizada.