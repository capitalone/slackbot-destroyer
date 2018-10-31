import boto3
import io
import json
from constants import *

class GlobalStore:
    # Number of deletions so far
    deletions = 0
    # Map of channel ids to boolean values
    destroy = {}
    s3 = None

    def __init__(self):
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            self.s3 = boto3.resource('s3')
            self.bucket = self.s3.Bucket(AWS_BUCKET_NAME)

    def active_in_channel(self, channel_id):
        """Return boolean if the bot is active in the given channel."""
        if channel_id in self.destroy.keys():
            return self.destroy[channel_id]
        return False

    def increment(self):
        """Increase the number of deletions and save."""
        self.deletions += 1
        self.save()

    def update_channel(self, channel_id, is_active):
        """Change the boolean value for a channel and save."""
        old_value = self.destroy[channel_id]
        self.destroy[channel_id] = is_active
        if old_value != is_active:
            self.save()

    def load(self):
        """Load from S3 if that is possible."""
        if self.s3:
            for obj in self.bucket.objects.all():
                if obj.key == CONFIG_FILE:
                    config_bytes = io.BytesIO()
                    self.bucket.download_fileobj(CONFIG_FILE, config_bytes)
                    json_config = json.loads(config_bytes.getvalue())
                    self._from_dict(json_config)
        # Otherwise just use the default

    def save(self):
        """Save to S3 if it is possible."""
        if self.s3:
            dict_repr = self._to_dict()
            json_string = json.dumps(dict_repr)
            byte_repr = io.BytesIO(json_string.encode('utf-8'))
            self.bucket.upload_fileobj(byte_repr, CONFIG_FILE)

    def _from_dict(self, json_config):
        self.deletions = json_config['deletions']
        self.destroy = json_config['destroy']

    def _to_dict(self):
        result = {}
        result['deletions'] = self.deletions
        result['destroy'] = self.destroy
        return result

    def __repr__(self):
        return self._to_dict().__repr__()
