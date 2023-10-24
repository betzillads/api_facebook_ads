import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse o Token da API a partir da variável de ambiente
base_url = os.environ.get('base_url')
id_user_1 = os.environ.get('id_user_1')
token_1 = os.environ.get('token_1')
# Configurações


def request(resource):
    data_start = '2023-09-01'
    data_today = datetime.now().strftime('%Y-%m-%d')
    open_col = "{"
    close_col = "}"
    time_range = f'{open_col}"since":"{data_start}","until":"{data_today}"{close_col}'
    url = f"{base_url}act_{id_user_1}/insights?time_increment=1&time_range={time_range}&{resource}&access_token={token_1}"
    response = requests.get(url)
    print(url)
    return response.json()
    
def pagination(resource, results=None):
    if results is None:
        results = []
    current_response = request(resource)
    data_count = len(current_response.get('data', []))
    next_page_url = current_response.get('paging', {}).get('next', None)
    if next_page_url:
        next_page_url = next_page_url.split(base_url)[1]
    results.append(current_response)
    if data_count == 0 or not next_page_url:
        return results
    else:
        return pagination(next_page_url, results)

# Exemplo de uso
resource = "level=adset&fields=account_name,campaign_name,campaign_id,adset_name,adset_id,ad_name,ad_id,spend,impressions,reach,clicks,cpc,cpm,cpp,ctr,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p95_watched_actions&limit=5"
result = pagination(resource)
print(result)
