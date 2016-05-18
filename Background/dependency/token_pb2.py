# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: token.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='token.proto',
  package='com.xiang.proto.pilot',
  syntax='proto3',
  serialized_pb=b'\n\x0btoken.proto\x12\x15\x63om.xiang.proto.pilot\x1a\x0c\x63ommon.proto\"\x84\x01\n\x0cRequest11001\x12.\n\x06\x63ommon\x18\x01 \x01(\x0b\x32\x1e.com.xiang.proto.RequestCommon\x12:\n\x06params\x18\x02 \x01(\x0b\x32*.com.xiang.proto.pilot.Request11001.Params\x1a\x08\n\x06Params\"\x94\x01\n\rResponse11001\x12.\n\x06\x63ommon\x18\x01 \x01(\x0b\x32\x1e.com.xiang.proto.RequestCommon\x12\x37\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32).com.xiang.proto.pilot.Response11001.Data\x1a\x1a\n\x04\x44\x61ta\x12\x12\n\nqiniuToken\x18\x01 \x01(\t\"\x9f\x01\n\x0cRequest11002\x12.\n\x06\x63ommon\x18\x01 \x01(\x0b\x32\x1e.com.xiang.proto.RequestCommon\x12:\n\x06params\x18\x02 \x01(\x0b\x32*.com.xiang.proto.pilot.Request11002.Params\x1a#\n\x06Params\x12\x19\n\x11oldTokenCannotUse\x18\x01 \x01(\x08\"\x96\x01\n\rResponse11002\x12.\n\x06\x63ommon\x18\x01 \x01(\x0b\x32\x1e.com.xiang.proto.RequestCommon\x12\x37\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32).com.xiang.proto.pilot.Response11002.Data\x1a\x1c\n\x04\x44\x61ta\x12\x14\n\x0crongyunToken\x18\x01 \x01(\tb\x06proto3'
  ,
  dependencies=[common__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REQUEST11001_PARAMS = _descriptor.Descriptor(
  name='Params',
  full_name='com.xiang.proto.pilot.Request11001.Params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=177,
  serialized_end=185,
)

_REQUEST11001 = _descriptor.Descriptor(
  name='Request11001',
  full_name='com.xiang.proto.pilot.Request11001',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='common', full_name='com.xiang.proto.pilot.Request11001.common', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='params', full_name='com.xiang.proto.pilot.Request11001.params', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_REQUEST11001_PARAMS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=185,
)


_RESPONSE11001_DATA = _descriptor.Descriptor(
  name='Data',
  full_name='com.xiang.proto.pilot.Response11001.Data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='qiniuToken', full_name='com.xiang.proto.pilot.Response11001.Data.qiniuToken', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=310,
  serialized_end=336,
)

_RESPONSE11001 = _descriptor.Descriptor(
  name='Response11001',
  full_name='com.xiang.proto.pilot.Response11001',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='common', full_name='com.xiang.proto.pilot.Response11001.common', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='com.xiang.proto.pilot.Response11001.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RESPONSE11001_DATA, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=188,
  serialized_end=336,
)


_REQUEST11002_PARAMS = _descriptor.Descriptor(
  name='Params',
  full_name='com.xiang.proto.pilot.Request11002.Params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='oldTokenCannotUse', full_name='com.xiang.proto.pilot.Request11002.Params.oldTokenCannotUse', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=463,
  serialized_end=498,
)

_REQUEST11002 = _descriptor.Descriptor(
  name='Request11002',
  full_name='com.xiang.proto.pilot.Request11002',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='common', full_name='com.xiang.proto.pilot.Request11002.common', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='params', full_name='com.xiang.proto.pilot.Request11002.params', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_REQUEST11002_PARAMS, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=339,
  serialized_end=498,
)


_RESPONSE11002_DATA = _descriptor.Descriptor(
  name='Data',
  full_name='com.xiang.proto.pilot.Response11002.Data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rongyunToken', full_name='com.xiang.proto.pilot.Response11002.Data.rongyunToken', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=623,
  serialized_end=651,
)

_RESPONSE11002 = _descriptor.Descriptor(
  name='Response11002',
  full_name='com.xiang.proto.pilot.Response11002',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='common', full_name='com.xiang.proto.pilot.Response11002.common', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='com.xiang.proto.pilot.Response11002.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RESPONSE11002_DATA, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=501,
  serialized_end=651,
)

_REQUEST11001_PARAMS.containing_type = _REQUEST11001
_REQUEST11001.fields_by_name['common'].message_type = common__pb2._REQUESTCOMMON
_REQUEST11001.fields_by_name['params'].message_type = _REQUEST11001_PARAMS
_RESPONSE11001_DATA.containing_type = _RESPONSE11001
_RESPONSE11001.fields_by_name['common'].message_type = common__pb2._REQUESTCOMMON
_RESPONSE11001.fields_by_name['data'].message_type = _RESPONSE11001_DATA
_REQUEST11002_PARAMS.containing_type = _REQUEST11002
_REQUEST11002.fields_by_name['common'].message_type = common__pb2._REQUESTCOMMON
_REQUEST11002.fields_by_name['params'].message_type = _REQUEST11002_PARAMS
_RESPONSE11002_DATA.containing_type = _RESPONSE11002
_RESPONSE11002.fields_by_name['common'].message_type = common__pb2._REQUESTCOMMON
_RESPONSE11002.fields_by_name['data'].message_type = _RESPONSE11002_DATA
DESCRIPTOR.message_types_by_name['Request11001'] = _REQUEST11001
DESCRIPTOR.message_types_by_name['Response11001'] = _RESPONSE11001
DESCRIPTOR.message_types_by_name['Request11002'] = _REQUEST11002
DESCRIPTOR.message_types_by_name['Response11002'] = _RESPONSE11002

Request11001 = _reflection.GeneratedProtocolMessageType('Request11001', (_message.Message,), dict(

  Params = _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), dict(
    DESCRIPTOR = _REQUEST11001_PARAMS,
    __module__ = 'token_pb2'
    # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Request11001.Params)
    ))
  ,
  DESCRIPTOR = _REQUEST11001,
  __module__ = 'token_pb2'
  # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Request11001)
  ))
_sym_db.RegisterMessage(Request11001)
_sym_db.RegisterMessage(Request11001.Params)

Response11001 = _reflection.GeneratedProtocolMessageType('Response11001', (_message.Message,), dict(

  Data = _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), dict(
    DESCRIPTOR = _RESPONSE11001_DATA,
    __module__ = 'token_pb2'
    # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Response11001.Data)
    ))
  ,
  DESCRIPTOR = _RESPONSE11001,
  __module__ = 'token_pb2'
  # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Response11001)
  ))
_sym_db.RegisterMessage(Response11001)
_sym_db.RegisterMessage(Response11001.Data)

Request11002 = _reflection.GeneratedProtocolMessageType('Request11002', (_message.Message,), dict(

  Params = _reflection.GeneratedProtocolMessageType('Params', (_message.Message,), dict(
    DESCRIPTOR = _REQUEST11002_PARAMS,
    __module__ = 'token_pb2'
    # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Request11002.Params)
    ))
  ,
  DESCRIPTOR = _REQUEST11002,
  __module__ = 'token_pb2'
  # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Request11002)
  ))
_sym_db.RegisterMessage(Request11002)
_sym_db.RegisterMessage(Request11002.Params)

Response11002 = _reflection.GeneratedProtocolMessageType('Response11002', (_message.Message,), dict(

  Data = _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), dict(
    DESCRIPTOR = _RESPONSE11002_DATA,
    __module__ = 'token_pb2'
    # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Response11002.Data)
    ))
  ,
  DESCRIPTOR = _RESPONSE11002,
  __module__ = 'token_pb2'
  # @@protoc_insertion_point(class_scope:com.xiang.proto.pilot.Response11002)
  ))
_sym_db.RegisterMessage(Response11002)
_sym_db.RegisterMessage(Response11002.Data)


# @@protoc_insertion_point(module_scope)
