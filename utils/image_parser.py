from google.cloud import vision
import logging

client = vision.ImageAnnotatorClient()


def get_text_from_image(uri):
    """Detects document features in the file located in Google Cloud Storage."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)

    logging.info(response.full_text_annotation.text)
    return response.full_text_annotation.text
