import requests
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse o Token da API a partir da variável de ambiente
base_url = os.environ.get('base_url')
id_user_df = os.environ.get('id_user_df')
token_df = os.environ.get('token_df')

def request(resource):
    data_start = '2023-08-01'
    data_today = datetime.now().strftime('%Y-%m-%d')
    time_range = f'{{"since":"{data_start}","until":"{data_today}"}}'
    url = f"{base_url}act_{id_user_df}/insights?time_increment=1&time_range={time_range}&{resource}&access_token={token_df}"
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
    results.extend(current_response.get('data', []))
    if data_count == 0 or not next_page_url:
        return results
    else:
        return pagination(next_page_url, results)

def flatten_video_fields(data):
    for item in data:
        for field in ["video_p25_watched_actions", "video_p50_watched_actions", "video_p75_watched_actions", "video_p95_watched_actions"]:
            if field in item:
                item[field] = item[field][0].get("value", "") if item[field] else ""
    return data

def save_to_csv(data, filename="output_ads_DF.csv"):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Exemplo de uso
resource = "level=ad&fields=account_name,campaign_name,campaign_id,adset_name,adset_id,ad_name,ad_id,spend,impressions,reach,clicks,cpc,cpm,cpp,ctr,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p95_watched_actions&limit=500"
result = pagination(resource)
result = flatten_video_fields(result)  # Adicione esta linha para achatar os campos de vídeo
save_to_csv(result)
