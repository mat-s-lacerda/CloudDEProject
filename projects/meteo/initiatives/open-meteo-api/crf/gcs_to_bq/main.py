import json
from functions_framework import http
from google.cloud import storage, bigquery
from flask import Request, jsonify

@http
def entrypoint(request: Request):
    """Cloud Function com trigger HTTP para ler JSON do GCS, flatten e carregar no BQ."""
    try:
        request_json = request.get_json()
        bucket_name = request_json['bucket_name']
        file_name = request_json['file']
        dataset_id = request_json['dataset']
        table_id = request_json['table']
    except (TypeError, KeyError) as e:
        return jsonify({"error": f"Parâmetros ausentes ou inválidos: {e}"}), 400

    # Inicializa os clientes do GCP
    storage_client = storage.Client()
    bq_client = bigquery.Client()

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_text()
        json_data = json.loads(content)
    except Exception as e:
        return jsonify({"error": f"Erro ao acessar arquivo no GCS: {e}"}), 500

    # Garante que json_data seja sempre uma lista
    if isinstance(json_data, dict):
        json_data = [json_data]

    flattened_rows = []

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

        # Validação extra: todos os campos de hourly devem ter o mesmo tamanho
        expected_length = len(hourly_data["time"])
        for key in hourly_data:
            if len(hourly_data[key]) != expected_length:
                return jsonify({
                    "error": f"Inconsistência no campo '{key}': tamanho diferente de 'time' ({len(hourly_data[key])} vs {expected_length})"
                }), 400

        # Flatten linha a linha
        for i in range(expected_length):
            row = {}
            for key in hourly_data:
                row[key] = hourly_data[key][i]
            row.update(meta)
            for col, unit in units.items():
                row[f"{col}_unit"] = unit
            flattened_rows.append(row)

    # Referência da tabela no BigQuery
    table_ref = f"{bq_client.project}.{dataset_id}.{table_id}"

    try:
        job_config = bigquery.LoadJobConfig(autodetect=True)
        job = bq_client.load_table_from_json(flattened_rows, table_ref, job_config=job_config)
        job.result()  # Aguarda a conclusão
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar no BigQuery: {e}"}), 500

    return jsonify({
        "message": f"{len(flattened_rows)} registros carregados na tabela {table_ref} com sucesso."
    }), 200
