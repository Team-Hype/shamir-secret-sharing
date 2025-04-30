import grpc

import shard.resources.generated.slave_pb2 as cf
import shard.resources.generated.slave_pb2_grpc as cf_grpc


class SlaveServer(cf_grpc.SlaveServicer):

    def PutSecretPart(self, request: cf.SecretPart, context: grpc.ServicerContext):
        from shard.slave.db import get_db
        from shard.slave.db.managers.secret import SecretManager

        db = next(get_db())
        try:
            manager = SecretManager(db)
            manager.save(key=str(request.key.key), part=request.part)
            return cf.Key(key=request.key.key)
        finally:
            db.close()

    def GetSecretPart(self, request: cf.Key, context: grpc.ServicerContext):
        from shard.slave.db import get_db
        from shard.slave.db.managers.secret import SecretManager

        db = next(get_db())
        try:
            manager = SecretManager(db)
            secret = manager.get(key=str(request.key))
            if not secret:
                context.abort(grpc.StatusCode.NOT_FOUND, "Part not found")

            return cf.SecretPart(key=request, part=secret.part)
        finally:
            db.close()


