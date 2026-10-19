# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Ola, pode me passar como foi as ultimas vendas ?"
- **Resposta esperada:** : "
    Essas foram as 3 ultimas vendes registradas na tabela. A respota deve conter alguns desses dados.

    TRX-106,2024-05-06,Receita,Encomendas,Sinal de reserva para 2 cestas comemorativas,145.0,PIX,Concluído
    TRX-108,2024-05-08,Receita,Vendas Balcão,Faturamento do dia,890.0,Dinheiro,Concluído/
    TRX-111,2024-05-12,Receita,Vendas Balcão,Movimento de Domingo (Dia das Mães),2140.0,Cartão de Crédito/PIX,Concluído
    "
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual foi a maior receita (em valor total) já registrada ?"
- **Resposta esperada:** "
    A resposta deve conter essa linha de dados

    TRX-108,2024-05-08,Receita,Vendas Balcão,Faturamento do dia,890.0,Dinheiro,Concluído
"
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual  o resultado do jogo do Brasil ?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [ ] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- [Liste aqui]

**O que pode melhorar:**
- [Liste aqui]

---
