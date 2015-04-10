# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: filter.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='filter.proto',
  package='',
  serialized_pb='\n\x0c\x66ilter.proto\"\xa2\x02\n\x06\x46ilter\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08min_mean\x18\x02 \x01(\x01\x12#\n\x1bnegative_gradient_variation\x18\x03 \x01(\x08\x12\x1b\n\x13min_linear_gradient\x18\x04 \x01(\x01\x12\x19\n\x11min_linear_offset\x18\x05 \x01(\x01\x12\x0e\n\x06\x63onvex\x18\x06 \x01(\x08\x12\x1f\n\x17\x66ilter_if_no_market_cap\x18\x07 \x01(\x08\x12\x16\n\x0emin_market_cap\x18\x08 \x01(\x01\x12\x16\n\x0emax_market_cap\x18\t \x01(\x01\x12\x10\n\x08\x63odeword\x18\n \x03(\t\x12\x11\n\tmin_value\x18\x0b \x01(\x01\x12\x15\n\rx_convex_poly\x18\x0c \x01(\x01')




_FILTER = _descriptor.Descriptor(
  name='Filter',
  full_name='Filter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Filter.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_mean', full_name='Filter.min_mean', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='negative_gradient_variation', full_name='Filter.negative_gradient_variation', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_linear_gradient', full_name='Filter.min_linear_gradient', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_linear_offset', full_name='Filter.min_linear_offset', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='convex', full_name='Filter.convex', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='filter_if_no_market_cap', full_name='Filter.filter_if_no_market_cap', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_market_cap', full_name='Filter.min_market_cap', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_market_cap', full_name='Filter.max_market_cap', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='codeword', full_name='Filter.codeword', index=9,
      number=10, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_value', full_name='Filter.min_value', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x_convex_poly', full_name='Filter.x_convex_poly', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
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
  extension_ranges=[],
  serialized_start=17,
  serialized_end=307,
)

DESCRIPTOR.message_types_by_name['Filter'] = _FILTER

class Filter(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FILTER

  # @@protoc_insertion_point(class_scope:Filter)


# @@protoc_insertion_point(module_scope)
