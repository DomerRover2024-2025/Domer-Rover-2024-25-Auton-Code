#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "custom_msgs::custom_msgs__rosidl_generator_py" for configuration "Release"
set_property(TARGET custom_msgs::custom_msgs__rosidl_generator_py APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(custom_msgs::custom_msgs__rosidl_generator_py PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libcustom_msgs__rosidl_generator_py.so"
  IMPORTED_SONAME_RELEASE "libcustom_msgs__rosidl_generator_py.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS custom_msgs::custom_msgs__rosidl_generator_py )
list(APPEND _IMPORT_CHECK_FILES_FOR_custom_msgs::custom_msgs__rosidl_generator_py "${_IMPORT_PREFIX}/lib/libcustom_msgs__rosidl_generator_py.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
