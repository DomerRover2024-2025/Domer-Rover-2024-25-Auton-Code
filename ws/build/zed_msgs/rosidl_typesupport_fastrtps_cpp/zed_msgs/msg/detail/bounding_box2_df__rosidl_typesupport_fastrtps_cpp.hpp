// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from zed_msgs:msg/BoundingBox2Df.idl
// generated code does not contain a copyright notice

#ifndef ZED_MSGS__MSG__DETAIL__BOUNDING_BOX2_DF__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define ZED_MSGS__MSG__DETAIL__BOUNDING_BOX2_DF__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "zed_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "zed_msgs/msg/detail/bounding_box2_df__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace zed_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
cdr_serialize(
  const zed_msgs::msg::BoundingBox2Df & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  zed_msgs::msg::BoundingBox2Df & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
get_serialized_size(
  const zed_msgs::msg::BoundingBox2Df & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
max_serialized_size_BoundingBox2Df(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace zed_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_zed_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, zed_msgs, msg, BoundingBox2Df)();

#ifdef __cplusplus
}
#endif

#endif  // ZED_MSGS__MSG__DETAIL__BOUNDING_BOX2_DF__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
