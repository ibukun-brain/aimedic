# import logging
# from threading import Thread

# logger = logging.getLogger(__name__)


# class BackgroundThread(Thread):
#     """
#     An Helper class for running background task
#     """

#     def __init__(
#             self, group=None, target=None, name=None, args=(), kwargs={}
#     ):
#         Thread.__init__(self, group, target, name, args, kwargs)

#     def run(self):
#         logger.info("Starting background task")
#         if self._target != None:
#             self._return = self._target(*self._args, **self._kwargs)

#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return
