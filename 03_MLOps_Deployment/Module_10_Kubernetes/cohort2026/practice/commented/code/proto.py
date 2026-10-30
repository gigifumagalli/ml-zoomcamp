# Commented copy of ../../../notebooks/code/proto.py (lesson 10.3).
# A hand-written tf.make_tensor_proto, so the gateway needs only the small `tensorflow-protobuf`
# package (the compiled .proto definitions) instead of the whole TensorFlow library.
#
# Difference from the lecture: data.tostring() -> data.tobytes(). ndarray.tostring() was removed in
# NumPy 2.3 (it was a deprecated alias of tobytes); the lecture line raises AttributeError there.

# PYTHON: these are generated protobuf message classes; they ship with tensorflow-protobuf.
from tensorflow.core.framework import tensor_pb2, tensor_shape_pb2, types_pb2


# GOAL: map the NumPy dtype name to TensorFlow's protobuf dtype enum.
# WHY: the model's signature says DT_FLOAT (float32). Supporting only that and failing loudly otherwise
#      is safer than guessing a conversion.
def dtypes_as_dtype(dtype):
    if dtype == "float32":
        return types_pb2.DT_FLOAT
    raise Exception("dtype %s is not supported" % dtype)


# GOAL: build a TensorProto = shape + dtype + the raw bytes of the array.
# WHY: protobuf does not know NumPy. We describe the tensor (dims, dtype) and attach the memory buffer as
#      bytes; TF Serving rebuilds the identical array on its side.
# PYTHON: a list comprehension builds one Dim message per axis, e.g. (1, 299, 299, 3) -> four Dims.
def make_tensor_proto(data):
    shape = data.shape
    dims = [tensor_shape_pb2.TensorShapeProto.Dim(size=i) for i in shape]
    proto_shape = tensor_shape_pb2.TensorShapeProto(dim=dims)

    proto_dtype = dtypes_as_dtype(data.dtype)

    tensor_proto = tensor_pb2.TensorProto(dtype=proto_dtype, tensor_shape=proto_shape)
    # PYTHON: .tobytes() returns the array's memory as a bytes object (C order). Lecture: .tostring().
    tensor_proto.tensor_content = data.tobytes()

    return tensor_proto


# GOAL: public entry point used by gateway.py: cast to float32 if needed, then convert.
def np_to_protobuf(data):
    if data.dtype != "float32":
        data = data.astype("float32")
    return make_tensor_proto(data)
