from google.cloud import storage
from datetime import datetime
import time
import logging


def upload_data_to_gcs(data, bucket_name='historical_images_directory'):
    try:
        try:
            client = storage.Client.from_service_account_json('cloud-storage-services.json')
        except:
            client = storage.Client()
        file_name = "Image-" + datetime.fromtimestamp(time.time()).strftime('%d%m%Y%H%M%S')
        bucket = client.bucket(bucket_name)
        bucket.blob(file_name).upload_from_string(data, predefined_acl='publicRead')
        return True, bucket.blob(file_name).public_url
    except Exception as e:
        logging.error(e)

    return False, None
