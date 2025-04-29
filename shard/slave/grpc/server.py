import grpc

import shard.resources.generated.slave_pb2 as cf
import shard.resources.generated.slave_pb2_grpc as cf_grpc


class SlaveServer(cf_grpc.SlaveServicer):

    def PutSecretPart(self, request: cf.SecretPart, context: grpc.ServicerContext):
        pass

    def GetSecretPart(self, request: cf.Key, context: grpc.ServicerContext):
        pass



