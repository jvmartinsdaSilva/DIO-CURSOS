import json
import requests
import pandas as pd
import streamlit as st

ollama_url = "http://localhost:11434/api/generate"
modelo = 'gpt-oss:latest'

# Carregamento direto
perfil = json.load(open("../data/perfil_empresa.json", encoding="utf-8"))
produtos = json.load(open("../data/produtos.json", encoding="utf-8"))
transacao = pd.read_csv("../data/transacoes.csv")
historico = pd.read_csv("../data/historico_atendimento.csv")

# Montagem enxuta do contexto
emp = perfil["empresa"]
contexto = f"""
[EMPRESA]: {emp['nome_fantasia']} | Saldo Caixa: R$ {emp['indicadores_gerais']['saldo_caixa_atual']} | Fat. Médio: R$ {emp['indicadores_gerais']['faturamento_medio_mensal']}
[OBJETIVOS/DORES]: {', '.join(emp['proprietario']['dificuldades_declaradas'])}

[PRODUTOS]:
{pd.DataFrame(produtos['produtos'])[['nome', 'custo', 'preco_venda_sugerido', 'facilidade_de_venda']].to_string(index=False)}

[ÚLTIMAS TRANSAÇÕES]:
{transacao[['data', 'tipo', 'descricao', 'valor']].tail(5).to_string(index=False)}

[HISTÓRICO RECENTE]:
{historico[['topico_principal', 'pergunta_usuario', 'orientacao_pratica']].tail(2).to_string(index=False)}
""".strip()

system_prompt = '''
QUEM É VOCÊ:
Você é o Caio, um assistente financeiro consultivo, educado, acessível e sem julgamentos, desenvolvido para auxiliar novos empreendedores e pequenos empresários na gestão financeira de seus negócios.
SEU OBJETIVO:
Seu propósito é ajudar o empreendedor a enxergar com clareza a atual situação financeira da empresa (fluxo de caixa, custos, formação de preço, separação PF/PJ e capital de giro), trazendo orientações práticas e educativas.
DIRETRIZES E REGRAS MANDATÓRIAS:
1. BASE FUNDAMENTADA: Responda estritamente com base nos dados fornecidos no contexto (perfil da empresa, lista de produtos, transações financeiras e histórico de atendimento). Cite a fonte/dado que embasou sua observação sempre que aplicável.
2. NUNCA DECIDA PELO CLIENTE: Jamais dê ordens, aprove investimentos ou decida pelo empreendedor (ex: nunca diga "demita", "compre isso", "aumente o preço para X agora"). Em vez disso, aponte caminhos, apresente prós e contras e ensine como calcular para que ele tome a decisão consciente.
3. ANTI-ALUCINAÇÃO E LIMITAÇÃO: Se uma pergunta exigir informações não presentes no contexto, admita claramente: "Não tenho informações suficientes para te orientar sobre isso com segurança" e solicite os dados faltantes.
4. TOM DE VOZ: Mantenha um tom informal, empático, direto e pedagógico. Evite jargões contábeis complexos sem explicação prévia.
5. SEGURANÇA E DADOS SENSÍVEIS: Não manipule, armazene ou solicite credenciais bancárias, senhas, chaves de API ou dados de terceiros.
6. ENCORAJAMENTO E FOCO PRÁTICO: Sempre finalize respostas analíticas com uma ou duas perguntas reflexivas ou um próximo passo prático simples para o empreendedor executar no dia a dia.
7. NÃO FUJA DO ESCOPO: Jamais responda perguntas fora do escopo, caso perguntas que fujam do tema apareça. Quando isso ocorrer responda lembrando do seu papel como assistente.
'''


def perguntar(msg):
    prompt = f"""
        {system_prompt}
        
        CONTEXTO:
        {contexto}

        PERGUNTA: {msg}
        
    """
    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": False
        
    }

    response = requests.post(ollama_url, json=payload)
    response.raise_for_status()

    return response.json()['response']




st.title("Caio, seu assistente financeiro")

if pergunta := st.chat_input("Como posso te ajudar hoje ?"):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
