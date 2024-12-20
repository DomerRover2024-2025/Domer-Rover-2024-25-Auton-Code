// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from zed_msgs:msg/ObjectsStamped.idl
// generated code does not contain a copyright notice

#ifndef ZED_MSGS__MSG__DETAIL__OBJECTS_STAMPED__FUNCTIONS_H_
#define ZED_MSGS__MSG__DETAIL__OBJECTS_STAMPED__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "zed_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "zed_msgs/msg/detail/objects_stamped__struct.h"

/// Initialize msg/ObjectsStamped message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * zed_msgs__msg__ObjectsStamped
 * )) before or use
 * zed_msgs__msg__ObjectsStamped__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
bool
zed_msgs__msg__ObjectsStamped__init(zed_msgs__msg__ObjectsStamped * msg);

/// Finalize msg/ObjectsStamped message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
void
zed_msgs__msg__ObjectsStamped__fini(zed_msgs__msg__ObjectsStamped * msg);

/// Create msg/ObjectsStamped message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * zed_msgs__msg__ObjectsStamped__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
zed_msgs__msg__ObjectsStamped *
zed_msgs__msg__ObjectsStamped__create();

/// Destroy msg/ObjectsStamped message.
/**
 * It calls
 * zed_msgs__msg__ObjectsStamped__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
void
zed_msgs__msg__ObjectsStamped__destroy(zed_msgs__msg__ObjectsStamped * msg);

/// Check for msg/ObjectsStamped message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
bool
zed_msgs__msg__ObjectsStamped__are_equal(const zed_msgs__msg__ObjectsStamped * lhs, const zed_msgs__msg__ObjectsStamped * rhs);

/// Copy a msg/ObjectsStamped message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
bool
zed_msgs__msg__ObjectsStamped__copy(
  const zed_msgs__msg__ObjectsStamped * input,
  zed_msgs__msg__ObjectsStamped * output);

/// Initialize array of msg/ObjectsStamped messages.
/**
 * It allocates the memory for the number of elements and calls
 * zed_msgs__msg__ObjectsStamped__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
bool
zed_msgs__msg__ObjectsStamped__Sequence__init(zed_msgs__msg__ObjectsStamped__Sequence * array, size_t size);

/// Finalize array of msg/ObjectsStamped messages.
/**
 * It calls
 * zed_msgs__msg__ObjectsStamped__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
void
zed_msgs__msg__ObjectsStamped__Sequence__fini(zed_msgs__msg__ObjectsStamped__Sequence * array);

/// Create array of msg/ObjectsStamped messages.
/**
 * It allocates the memory for the array and calls
 * zed_msgs__msg__ObjectsStamped__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
zed_msgs__msg__ObjectsStamped__Sequence *
zed_msgs__msg__ObjectsStamped__Sequence__create(size_t size);

/// Destroy array of msg/ObjectsStamped messages.
/**
 * It calls
 * zed_msgs__msg__ObjectsStamped__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
void
zed_msgs__msg__ObjectsStamped__Sequence__destroy(zed_msgs__msg__ObjectsStamped__Sequence * array);

/// Check for msg/ObjectsStamped message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
bool
zed_msgs__msg__ObjectsStamped__Sequence__are_equal(const zed_msgs__msg__ObjectsStamped__Sequence * lhs, const zed_msgs__msg__ObjectsStamped__Sequence * rhs);

/// Copy an array of msg/ObjectsStamped messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_zed_msgs
bool
zed_msgs__msg__ObjectsStamped__Sequence__copy(
  const zed_msgs__msg__ObjectsStamped__Sequence * input,
  zed_msgs__msg__ObjectsStamped__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ZED_MSGS__MSG__DETAIL__OBJECTS_STAMPED__FUNCTIONS_H_
