import boto3
import io
import json
from constants import *

class GlobalStore:
    # Number of deletions so far
    deletions = 0
    # Map of channel ids to State values
    destroy = {}
    # List of lists in the form [slackbot response text, % occurrence as 0-1 value]
    responses = []
    s3 = None

    def __init__(self):
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            self.s3 = boto3.resource('s3')
            self.bucket = self.s3.Bucket(AWS_BUCKET_NAME)

    def state_in_channel(self, channel_id):
        """Return state of bot in the given channel."""
        if channel_id not in self.destroy.keys():
            self.update_channel(channel_id, State.DEACTIVATED)
        return self.destroy[channel_id]

    def increment(self):
        """Increase the number of deletions and save."""
        self.deletions += 1
        self.save()

    def update_channel(self, channel_id, state):
        """Change the state value for a channel and save."""
        old_value = self.destroy.get(channel_id, None)
        self.destroy[channel_id] = state
        if old_value != state:
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

    def add_response(self, new_response):
        """Add a new response with default chance to the list."""
        for response, chance in self.responses:
            if response == new_response:
                return
        self.responses.append((new_response, 1.0))
        self.save()

    def get_response_chance(self, response):
        """Get the chance of being seen for a given response."""
        for known_response, chance in self.responses:
            if known_response == response:
                return chance
        return 1.0

    def set_response_chance(self, index, new_chance):
        """Set the chance of being seen for a given response."""
        self.responses[index][1] = new_chance
        self.save()

    def format_responses(self):
        """Return responses formatted for output."""
        if not self.responses:
            return 'N O  D A T A  A V A I L A B L E'
        formatted = ['[{:02d}]: {} @ {}'.format(idx, response, freq)
                     for idx, [response, freq] in enumerate(self.responses)]
        return '\n'.join(formatted)
    
    def _from_dict(self, json_config):
        self.deletions = json_config.get('deletions', 0)
        self.responses = json_config.get('responses', [])
        for channel, enum_val in json_config.get('destroy', {}).items():
            self.destroy[channel] = State(enum_val)

    def _to_dict(self):
        result = {}
        result['deletions'] = self.deletions
        result['responses'] = self.responses
        result['destroy'] = {}
        for channel, enum_obj in self.destroy.items():
            result['destroy'][channel] = enum_obj.value
        return result

    def __repr__(self):
        return self._to_dict().__repr__()
