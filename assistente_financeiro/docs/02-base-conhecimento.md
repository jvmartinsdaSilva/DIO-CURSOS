# Base de Conhecimento

## Dados Utilizados

A base de conhecimento do agente **Caio** é alimentada pelos arquivos estruturados armazenados no diretório `data/`, refletindo a rotina operacional e financeira da empresa:

| Arquivo | Formato | Utilização no Agente |
|---|---|---|
| `perfil_empresa.json` | JSON | Fornece dados cadastrais, porte, regime tributário, indicadores macro (faturamento, custos fixos, capital de giro) e dores declaradas pelo empreendedor. |
| `produtos.json` | JSON | Permite analisar a estrutura de custos, margens praticadas e o giro de estoque com base na facilidade de venda (baixa, média ou alta) para apoiar na precificação. |
| `transacoes.csv` | CSV | Base para mapear o fluxo de caixa diário, identificar despesas concentradas, receitas por forma de pagamento e alertas de liquidez. |
| `historico_atendimento.csv` | CSV | Garante a continuidade do suporte consultivo, evitando repetições e servindo de referência para as instruções pedagógicas anteriores. |


---

## Estratégia de Integração

### Como os dados são carregados?
Os arquivos `.json` e `.csv` são lidos localmente na inicialização da aplicação Streamlit através do `pandas` e do módulo nativo `json` do Python. Para manter a resposta do modelo rápida e evitar I/O desnecessário no disco a cada mensagem, as bases são cacheadas em memória utilizando o `st.session_state`.

### Como os dados são usados no prompt?
A arquitetura utiliza uma abordagem híbrida de contexto:
- **System Prompt Estático:** Recebe a persona do Caio (educativo, acessível, sem emitir comandos executivos nem tomar decisões pelo negócio), as limitações éticas de segurança e o perfil sintetizado da empresa (`perfil_empresa.json`).
- **Injeção Dinâmica no Contexto (User Turn):** 
  - Quando a dúvida do empreendedor envolve fluxo de caixa ou saldo, um resumo das movimentações recentes do `transacoes.csv` é filtrado e injetado.
  - Para dúvidas sobre formação de preço, margem ou perdas, os itens correspondentes do `produtos.json` são anexados.
  - As últimas interações do `historico_atendimento.csv` entram como histórico imediato para manter a coerência da conversa.

---

## Exemplo de Contexto Montado

```text
[INSTRUÇÃO DO SISTEMA]
Você é o Caio, assistente financeiro consultivo e acessível para microempreendedores.
Seu objetivo é orientar e educar com base unicamente nos dados abaixo, sem tomar decisões pelo cliente.

[DADOS DA EMPRESA]
- Empresa: Cafeteria & Padaria Pão D'Ouro (Lucas Ferreira da Silva)
- Regime: Simples Nacional | Faturamento Médio: R$ 18.500,00
- Saldo Atual em Caixa: R$ 3.450,00 | Capital de Giro: 12 dias
- Principais Desafios: Fluxo de caixa, precificação e separação de despesas PF/PJ.

[PRODUTOS EM ANÁLISE]
- Café Espresso (50ml): Custo R$ 1,20 | Preço R$ 6,50 | Saída: Alta
- Torta Salgada Frango (Inteira): Custo R$ 38,00 | Preço R$ 85,00 | Saída: Baixa

[ÚLTIMAS TRANSAÇÕES]
- 05/05: Aluguel comercial (-R$ 2.800,00) [Boleto]
- 05/05: Energia elétrica (-R$ 720,40) [Débito]
- 06/05: Sinal cestas comemorativas (+R$ 145,00) [PIX]
- 10/05: DAS Simples Nacional (-R$ 480,00) [Pendente]

[HISTÓRICO RECENTE DE ATENDIMENTO]
- Usuário relatou perdas com sobras de tortas inteiras; orientado a avaliar venda fracionada ou encomenda.

[MENSAGEM DO USUÁRIO]
"Caio, sobrou pouco dinheiro após pagar o aluguel e a conta de energia no dia 5. O que posso fazer para melhorar meu fôlego nos primeiros dias do mês?"
```