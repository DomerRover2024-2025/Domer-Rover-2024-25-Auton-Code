// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from zed_msgs:msg/GnssFusionStatus.idl
// generated code does not contain a copyright notice

#ifndef ZED_MSGS__MSG__DETAIL__GNSS_FUSION_STATUS__STRUCT_HPP_
#define ZED_MSGS__MSG__DETAIL__GNSS_FUSION_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__zed_msgs__msg__GnssFusionStatus __attribute__((deprecated))
#else
# define DEPRECATED__zed_msgs__msg__GnssFusionStatus __declspec(deprecated)
#endif

namespace zed_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct GnssFusionStatus_
{
  using Type = GnssFusionStatus_<ContainerAllocator>;

  explicit GnssFusionStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gnss_fusion_status = 0;
    }
  }

  explicit GnssFusionStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gnss_fusion_status = 0;
    }
  }

  // field types and members
  using _gnss_fusion_status_type =
    uint8_t;
  _gnss_fusion_status_type gnss_fusion_status;

  // setters for named parameter idiom
  Type & set__gnss_fusion_status(
    const uint8_t & _arg)
  {
    this->gnss_fusion_status = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t OK =
    0u;
  static constexpr uint8_t OFF =
    1u;
  static constexpr uint8_t CALIBRATION_IN_PROGRESS =
    2u;
  static constexpr uint8_t RECALIBRATION_IN_PROGRESS =
    3u;

  // pointer types
  using RawPtr =
    zed_msgs::msg::GnssFusionStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const zed_msgs::msg::GnssFusionStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      zed_msgs::msg::GnssFusionStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      zed_msgs::msg::GnssFusionStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__zed_msgs__msg__GnssFusionStatus
    std::shared_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__zed_msgs__msg__GnssFusionStatus
    std::shared_ptr<zed_msgs::msg::GnssFusionStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GnssFusionStatus_ & other) const
  {
    if (this->gnss_fusion_status != other.gnss_fusion_status) {
      return false;
    }
    return true;
  }
  bool operator!=(const GnssFusionStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GnssFusionStatus_

// alias to use template instance with default allocator
using GnssFusionStatus =
  zed_msgs::msg::GnssFusionStatus_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GnssFusionStatus_<ContainerAllocator>::OK;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GnssFusionStatus_<ContainerAllocator>::OFF;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GnssFusionStatus_<ContainerAllocator>::CALIBRATION_IN_PROGRESS;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GnssFusionStatus_<ContainerAllocator>::RECALIBRATION_IN_PROGRESS;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace zed_msgs

#endif  // ZED_MSGS__MSG__DETAIL__GNSS_FUSION_STATUS__STRUCT_HPP_
