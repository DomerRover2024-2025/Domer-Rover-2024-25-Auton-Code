// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from zed_msgs:msg/PosTrackStatus.idl
// generated code does not contain a copyright notice

#ifndef ZED_MSGS__MSG__DETAIL__POS_TRACK_STATUS__BUILDER_HPP_
#define ZED_MSGS__MSG__DETAIL__POS_TRACK_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "zed_msgs/msg/detail/pos_track_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace zed_msgs
{

namespace msg
{

namespace builder
{

class Init_PosTrackStatus_status
{
public:
  explicit Init_PosTrackStatus_status(::zed_msgs::msg::PosTrackStatus & msg)
  : msg_(msg)
  {}
  ::zed_msgs::msg::PosTrackStatus status(::zed_msgs::msg::PosTrackStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::zed_msgs::msg::PosTrackStatus msg_;
};

class Init_PosTrackStatus_spatial_memory_status
{
public:
  explicit Init_PosTrackStatus_spatial_memory_status(::zed_msgs::msg::PosTrackStatus & msg)
  : msg_(msg)
  {}
  Init_PosTrackStatus_status spatial_memory_status(::zed_msgs::msg::PosTrackStatus::_spatial_memory_status_type arg)
  {
    msg_.spatial_memory_status = std::move(arg);
    return Init_PosTrackStatus_status(msg_);
  }

private:
  ::zed_msgs::msg::PosTrackStatus msg_;
};

class Init_PosTrackStatus_odometry_status
{
public:
  Init_PosTrackStatus_odometry_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PosTrackStatus_spatial_memory_status odometry_status(::zed_msgs::msg::PosTrackStatus::_odometry_status_type arg)
  {
    msg_.odometry_status = std::move(arg);
    return Init_PosTrackStatus_spatial_memory_status(msg_);
  }

private:
  ::zed_msgs::msg::PosTrackStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::zed_msgs::msg::PosTrackStatus>()
{
  return zed_msgs::msg::builder::Init_PosTrackStatus_odometry_status();
}

}  // namespace zed_msgs

#endif  // ZED_MSGS__MSG__DETAIL__POS_TRACK_STATUS__BUILDER_HPP_
