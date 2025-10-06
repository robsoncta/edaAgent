import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import base64
from io import BytesIO
from google.adk.tools import ToolContext

def generate_chart(context: ToolContext, chart_type: str, params: dict) -> dict:
    """Gera um gráfico e retorna o caminho da imagem salva.
    
    Args:
        chart_type: Tipo de gráfico ('histogram', 'scatter', 'box', 'heatmap', 'bar').
        params: Parâmetros (ex: {'x': 'col1', 'y': 'col2', 'data': df_json}).
    
    Returns:
        dict: {'status': 'success', 'image_path': path} ou error.
    """
    try:
        if 'current_dataset' not in context.session.state:
            return {'status': 'error', 'error_message': 'Dataset não carregado.'}
        df_json = context.session.state['current_dataset']
        df = pd.read_json(df_json, orient='records')
        
        fig = None
        if chart_type == 'histogram':
            column = params['column']
            fig = px.histogram(df, x=column)
        elif chart_type == 'scatter':
            x, y = params['x'], params['y']
            fig = px.scatter(df, x=x, y=y)
        elif chart_type == 'box':
            column = params['column']
            fig = px.box(df, y=column)
        elif chart_type == 'heatmap':
            corr = df.corr()
            fig = px.imshow(corr)
        elif chart_type == 'bar':
            x, y = params['x'], params['y']
            fig = px.bar(df, x=x, y=y)
        else:
            return {'status': 'error', 'error_message': 'Tipo de gráfico inválido.'}
        
        temp_dir = 'temp_files'
        os.makedirs(temp_dir, exist_ok=True)
        image_path = os.path.join(temp_dir, f"chart_{os.urandom(4).hex()}.png")
        fig.write_image(image_path)
        return {'status': 'success', 'image_path': image_path}
    except Exception as e:
        return {'status': 'error', 'error_message': str(e)}