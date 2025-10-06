import pandas as pd
import numpy as np
from scipy import stats
from google.adk.tools import ToolContext

def analyze_data(context: ToolContext, analysis_type: str, params: dict = None) -> dict:
    """Executa análises estatísticas específicas no dataset.
    
    Args:
        analysis_type: Tipo de análise ('describe', 'outliers', 'correlation', 'distribution').
        params: Parâmetros adicionais (ex: {'column': 'col1'}).
    
    Returns:
        dict: {'status': 'success', 'result': str(result)} ou error.
    """
    try:
        if 'current_dataset' not in context.session.state:
            return {'status': 'error', 'error_message': 'Dataset não carregado.'}
        df_json = context.session.state['current_dataset']
        df = pd.read_json(df_json, orient='records')
        
        if analysis_type == 'describe':
            result = df.describe().to_string()
        elif analysis_type == 'outliers':
            column = params.get('column')
            z_scores = np.abs(stats.zscore(df[column]))
            outliers = df[z_scores > 3]
            result = outliers.to_string()
        elif analysis_type == 'correlation':
            result = df.corr().to_string()
        elif analysis_type == 'distribution':
            column = params.get('column')
            result = df[column].value_counts().to_string()
        else:
            return {'status': 'error', 'error_message': 'Tipo de análise inválido.'}
        
        return {'status': 'success', 'result': result}
    except Exception as e:
        return {'status': 'error', 'error_message': str(e)}