from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter


class UploadStatusRouter(BaseRouter):
    route_name = 'sys'

    def get_subscription_channels(self, **kwargs):
        return ['upload_status']


route_handler.register(UploadStatusRouter)
