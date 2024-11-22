import os


def get_upload_path(instance, filename):
    # Create the upload path using the current date
    upload_path = os.path.join(instance.created_at.strftime("%Y%m%d"), filename)
    return upload_path
