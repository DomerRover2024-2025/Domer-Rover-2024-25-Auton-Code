// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:msg/Coords.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__COORDS__BUILDER_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__COORDS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/msg/detail/coords__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace msg
{

namespace builder
{

class Init_Coords_altitude
{
public:
  explicit Init_Coords_altitude(::custom_msgs::msg::Coords & msg)
  : msg_(msg)
  {}
  ::custom_msgs::msg::Coords altitude(::custom_msgs::msg::Coords::_altitude_type arg)
  {
    msg_.altitude = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::msg::Coords msg_;
};

class Init_Coords_longitude
{
public:
  explicit Init_Coords_longitude(::custom_msgs::msg::Coords & msg)
  : msg_(msg)
  {}
  Init_Coords_altitude longitude(::custom_msgs::msg::Coords::_longitude_type arg)
  {
    msg_.longitude = std::move(arg);
    return Init_Coords_altitude(msg_);
  }

private:
  ::custom_msgs::msg::Coords msg_;
};

class Init_Coords_latitude
{
public:
  Init_Coords_latitude()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Coords_longitude latitude(::custom_msgs::msg::Coords::_latitude_type arg)
  {
    msg_.latitude = std::move(arg);
    return Init_Coords_longitude(msg_);
  }

private:
  ::custom_msgs::msg::Coords msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::msg::Coords>()
{
  return custom_msgs::msg::builder::Init_Coords_latitude();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__COORDS__BUILDER_HPP_
