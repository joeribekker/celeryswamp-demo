import time
from celery import shared_task
from swampdragon.pubsub_providers.data_publisher import publish_data


@shared_task(bind=True)
def process_file(self, content):
    lines = content.split('\n')
    line_count = len(lines)

    for i, line in enumerate(lines):
        time.sleep(0.1)
        status_data = {
            'current': i,
            'total': line_count
        }

        if not self.request.called_directly:
            self.update_state(
                state='PROGRESS',
                meta=status_data
            )

        # Swampdragon
        channel_data = status_data.copy()
        channel_data['status'] = 'PROGRESS'
        publish_data('upload_status', channel_data)

    return True
