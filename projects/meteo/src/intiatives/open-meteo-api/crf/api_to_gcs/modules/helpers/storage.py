from google.cloud.storage import Client as GCSClient, Bucket

class GCSHandler:
    def __init__(self, project_id:str, bucket_name: str):
        self.client: GCSClient = GCSClient(project=project_id)
        self.bucket: Bucket = self.client.bucket(bucket_name)

    def upload_file(self, source_file_path: str, destination_blob_name: str) -> None:
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)
        print(f"Uploaded {source_file_path} to {destination_blob_name}")

    def download_file(self, source_blob_name: str, destination_file_path: str) -> None:
        blob = self.bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_path)
        print(f"Downloaded {source_blob_name} to {destination_file_path}")

    def list_files(self, prefix: str = None) -> str:
        blobs = self.client.list_blobs(self.bucket, prefix=prefix)
        return [blob.name for blob in blobs]

    def delete_file(self, blob_name: str) -> None:
        blob = self.bucket.blob(blob_name)
        blob.delete()
        print(f"Deleted {blob_name}")

    def file_exists(self, blob_name: str) -> bool:
        blob = self.bucket.blob(blob_name)
        return blob.exists()

    def upload_bytes(self, data: bytes, destination_blob_name: str) -> None:
        """
        Uploads bytes to a blob in the given bucket.

        Args:
            data: The bytes to be uploaded.
            destination_blob_name: The name of the blob to be uploaded to.
        """
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_string(data)
        print(f"Uploaded bytes to {destination_blob_name}")

    def download_as_string(self, blob_name: str) -> str:
        blob = self.bucket.blob(blob_name)
        return blob.download_as_text()

    def copy_file(self, source_blob_name: str, destination_blob_name: str, destination_bucket_name: str = None) -> None:
        source_blob = self.bucket.blob(source_blob_name)
        destination_bucket = self.client.bucket(destination_bucket_name) if destination_bucket_name else self.bucket
        self.bucket.copy_blob(source_blob, destination_bucket, destination_blob_name)
        print(f"Copied {source_blob_name} to {destination_blob_name} in {destination_bucket.name}")

    def rename_file(self, old_blob_name: str, new_blob_name: str) -> None:
        self.copy_file(old_blob_name, new_blob_name)
        self.delete_file(old_blob_name)
        print(f"Renamed {old_blob_name} to {new_blob_name}")