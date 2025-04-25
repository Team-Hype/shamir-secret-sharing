#!/bin/bash

if [ "$(basename $(pwd))" != "shard" ]; then
    echo "Ошибка: скрипт должен быть запущен из директории 'shard'."
    exit 1
fi

source scripts/utils.sh

PROTO_DIR="schema_registry"
OUT_DIR="generated"

if ! python3 -c "import grpc_tools" &> /dev/null || ! python3 -c "import mypy_protobuf" &> /dev/null
then
    colored_echo "Libraries for grpc are not installed. Please install them:" red
    echo
    echo "    pip install grpcio-tools mypy-protobuf"
    echo " or"
    echo "    poetry install"
    exit 1
fi

if [ ! -d $PROTO_DIR ]; then
  colored_echo "Directory $PROTO_DIR does not exist. You must be in the 'shard' directory." red
  exit 1
fi

PROTO_FILES=$(find $PROTO_DIR -name "*.proto")

if [ -z "$PROTO_FILES" ]; then
    colored_echo "No .proto files to compile." yellow
    exit 1
fi

mkdir -p $OUT_DIR

for PROTO_FILE in $(find $PROTO_DIR -name "*.proto")
do
    echo " - Compiling $PROTO_FILE..."
    python3 -m grpc_tools.protoc \
      -I$PROTO_DIR \
      --python_out=$OUT_DIR \
      --grpc_python_out=$OUT_DIR \
      --mypy_out=$OUT_DIR \
      $PROTO_FILE &> /dev/null
done

for GENERATED_FILE in $OUT_DIR/*.py
do
    sed -i 's/^import \(.*\)_pb2$/from shard.generated import \1_pb2/' $GENERATED_FILE
    sed -i 's/^import \(.*\)_pb2_grpc$/from shard.generated import \1_pb2_grpc/' $GENERATED_FILE
done

colored_echo "✅  Compilation is finished. All files are in '$OUT_DIR'." green
