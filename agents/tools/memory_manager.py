from google.adk.tools import ToolContext

def manage_memory(context: ToolContext, action: str, key: str, value: str = None) -> dict:
    """Gerencia a memória da sessão: armazena, recupera ou limpa valores.
    
    Args:
        action: 'set', 'get', 'delete'.
        key: Chave do valor.
        value: Valor para set (opcional).
    
    Returns:
        dict: {'status': 'success', 'result': value} para get, ou confirmação.
    """
    state = context.session.state
    if action == 'set':
        if len(state) > 10:  # Limite
            oldest_key = next(iter(state))
            del state[oldest_key]
        state[key] = value[:1000] if value else ""  # Truncar
        return {'status': 'success', 'result': 'Valor armazenado.'}
    elif action == 'get':
        return {'status': 'success', 'result': state.get(key, 'Não encontrado.')}
    elif action == 'delete':
        if key in state:
            del state[key]
        return {'status': 'success', 'result': 'Valor deletado.'}
    else:
        return {'status': 'error', 'error_message': 'Ação inválida.'}