// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from zed_msgs:msg/BoundingBox3D.idl
// generated code does not contain a copyright notice
#include "zed_msgs/msg/detail/bounding_box3_d__rosidl_typesupport_fastrtps_cpp.hpp"
#include "zed_msgs/msg/detail/bounding_box3_d__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace zed_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const zed_msgs::msg::Keypoint3D &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  zed_msgs::msg::Keypoint3D &);
size_t get_serialized_size(
  const zed_msgs::msg::Keypoint3D &,
  size_t current_alignment);
size_t
max_serialized_size_Keypoint3D(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace zed_msgs


namespace zed_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
cdr_serialize(
  const zed_msgs::msg::BoundingBox3D & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: corners
  {
    for (size_t i = 0; i < 8; i++) {
      zed_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.corners[i],
        cdr);
    }
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  zed_msgs::msg::BoundingBox3D & ros_message)
{
  // Member: corners
  {
    for (size_t i = 0; i < 8; i++) {
      zed_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr,
        ros_message.corners[i]);
    }
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
get_serialized_size(
  const zed_msgs::msg::BoundingBox3D & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: corners
  {
    size_t array_size = 8;

    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        zed_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.corners[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
max_serialized_size_BoundingBox3D(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: corners
  {
    size_t array_size = 8;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        zed_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Keypoint3D(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = zed_msgs::msg::BoundingBox3D;
    is_plain =
      (
      offsetof(DataType, corners) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _BoundingBox3D__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const zed_msgs::msg::BoundingBox3D *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _BoundingBox3D__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<zed_msgs::msg::BoundingBox3D *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _BoundingBox3D__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const zed_msgs::msg::BoundingBox3D *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _BoundingBox3D__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_BoundingBox3D(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _BoundingBox3D__callbacks = {
  "zed_msgs::msg",
  "BoundingBox3D",
  _BoundingBox3D__cdr_serialize,
  _BoundingBox3D__cdr_deserialize,
  _BoundingBox3D__get_serialized_size,
  _BoundingBox3D__max_serialized_size
};

static rosidl_message_type_support_t _BoundingBox3D__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_BoundingBox3D__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace zed_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_zed_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<zed_msgs::msg::BoundingBox3D>()
{
  return &zed_msgs::msg::typesupport_fastrtps_cpp::_BoundingBox3D__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, zed_msgs, msg, BoundingBox3D)() {
  return &zed_msgs::msg::typesupport_fastrtps_cpp::_BoundingBox3D__handle;
}

#ifdef __cplusplus
}
#endif
