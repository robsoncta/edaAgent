import pandas as pd
from google.adk.tools import ToolContext

def load_csv(context: ToolContext, file_path: str) -> dict:
    """Carrega um arquivo CSV e retorna o DataFrame como string para análise.
    
    Args:
        file_path: Caminho do arquivo CSV.
    
    Returns:
        dict: {'status': 'success', 'data': str(df)} ou {'status': 'error', 'error_message': msg}
    """
    try:
        df = pd.read_csv(file_path)
        context.session.state['current_dataset'] = df.to_json(orient='records')
        return {'status': 'success', 'data': df.to_string(index=False)}
    except Exception as e:
        return {'status': 'error', 'error_message': str(e)}