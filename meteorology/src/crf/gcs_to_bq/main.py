import json
from functions_framework import http
import pandas as pd
import requests
from google.cloud import storage, bigquery
from flask import Request, jsonify

@http
def main(request: Request):
    """Cloud Function com trigger HTTP para ler JSON do GCS, flatten e carregar no BQ."""
    try:
        request_json = request.get_json()
        bucket_name = request_json['bucket_name']
        file_name = request_json['file']
        dataset_id = request_json['dataset']
        table_id = request_json['table']
    except (TypeError, KeyError) as e:
        return jsonify({"error": f"Parâmetros ausentes ou inválidos: {e}"}), 400

    # Inicializa os clientes
    storage_client: storage.Client = storage.Client()
    bq_client: bigquery.Client = bigquery.Client()

    try:
        bucket: storage.Bucket = storage_client.bucket(bucket_name)
        blob: storage.Blob = bucket.blob(file_name)
        content: str = blob.download_as_text()
        json_data: dict = json.loads(content)
    except Exception as e:
        return jsonify({"error": f"Erro ao acessar arquivo no GCS: {e}"}), 500

    if isinstance(json_data, dict):
        json_data = [json_data]

    dfs = []
    for data in json_data:
        try:
            meta = {
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "generationtime_ms": data["generationtime_ms"],
                "utc_offset_seconds": data["utc_offset_seconds"],
                "timezone": data["timezone"],
                "timezone_abbreviation": data["timezone_abbreviation"],
                "elevation": data["elevation"]
            }
            hourly_data = data["hourly"]
            units = data["hourly_units"]
        except KeyError as e:
            return jsonify({"error": f"Chave ausente no JSON: {e}"}), 400

        df = pd.DataFrame(hourly_data)
        for key, value in meta.items():
            df[key] = value
        for col in units:
            df[f"{col}_unit"] = units[col]
        dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)

    table_ref = f"{bq_client.project}.{dataset_id}.{table_id}"
    try:
        job = bq_client.load_table_from_dataframe(df_final, table_ref)
        job.result()  # Aguarda o job terminar
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar no BigQuery: {e}"}), 500

    return jsonify({
        "message": f"{len(df_final)} registros carregados na tabela {table_ref} com sucesso."
    }), 200
