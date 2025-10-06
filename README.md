# edaAgent

Este projeto fornece um conjunto de agentes para exploração de dados construídos sobre o Google ADK. Quando o pacote `google-adk` não estiver disponível, o módulo `agents.agent._adk_compat` oferece uma implementação compatível mínima para que o pacote continue funcional. 

## Executando localmente

1. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Defina as variáveis de ambiente necessárias no arquivo `.env`, se houver.
3. Inicie o aplicativo Streamlit:
   ```bash
   streamlit run streamlit_app.py
   ```

## Estrutura de agentes

- `agents.root_agent` (ou simplesmente `agents.agent`) expõe o agente raiz que coordena a execução.
- `agents.agent.coordenador` contém o agente coordenador que orquestra especialistas.
- `agents.agent.data_explorer` e `agents.agent.visualization_expert` implementam agentes especialistas.
- A pasta `agents/agent/tools` reúne ferramentas utilitárias como carregamento de CSV, geração de gráficos e análise de dados.

## Testes rápidos

Para validar se o pacote está acessível sem o Google ADK, execute:

```bash
python - <<'PY'
import agents
print('has root_agent:', hasattr(agents, 'root_agent'))
root = agents.root_agent
print('type:', type(root))
print('sub_agents:', [getattr(agent, 'name', type(agent)) for agent in getattr(root, 'sub_agents', [])])
PY
```

O script deve confirmar que o agente raiz é carregado e listar os agentes filhos registrados.
