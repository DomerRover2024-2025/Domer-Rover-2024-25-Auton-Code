#include "include/custom_hardware/custom_hardware.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "hardware_interface/system_interface.hpp"
#include "rclcpp/rclcpp.hpp"

#include <chrono>
#include <cmath>
#include <limits>
#include <memory>
#include <vector>

#include <fcntl.h>
#include <errno.h>
#include <unistd.h>

namespace custom_hardware
{
    hardware_interface::CallbackReturn CustomHardware::on_init(const hardware_interface::HardwareInfo & info)
{
  if (hardware_interface::SystemInterface::on_init(info) != hardware_interface::CallbackReturn::SUCCESS)
  {
    return hardware_interface::CallbackReturn::ERROR;
  }
  // hw_states_position_ = std::numeric_limits<double>::quiet_NaN();
  // hw_commands_ = std::numeric_limits<double>::quiet_NaN();

  hw_states_position_.resize(info_.joints.size(), std::numeric_limits<double>::quiet_NaN());
  hw_commands_.resize(info_.joints.size(), std::numeric_limits<double>::quiet_NaN());

  const hardware_interface::ComponentInfo & joint = info_.joints[0];
  // RRBotModularJoint has exactly one state and command interface on each joint
  if (joint.command_interfaces.size() != 1)
  {
    RCLCPP_FATAL(
      rclcpp::get_logger("RRBotModularJoint"),
      "Joint '%s' has %zu command interfaces found. 1 expected.", joint.name.c_str(),
      joint.command_interfaces.size());
    return hardware_interface::CallbackReturn::ERROR;
  }

  if (joint.command_interfaces[0].name != hardware_interface::HW_IF_POSITION)
  {
    RCLCPP_FATAL(
      rclcpp::get_logger("RRBotModularJoint"),
      "Joint '%s' have %s command interfaces found. '%s' expected.", joint.name.c_str(),
      joint.command_interfaces[0].name.c_str(), hardware_interface::HW_IF_POSITION);
    return hardware_interface::CallbackReturn::ERROR;
  }

  if (joint.state_interfaces.size() != 1)
  {
    RCLCPP_FATAL(
      rclcpp::get_logger("RRBotModularJoint"), "Joint '%s' has %zu state interface. 1 expected.",
      joint.name.c_str(), joint.state_interfaces.size());
    return hardware_interface::CallbackReturn::ERROR;
  }

  if (joint.state_interfaces[0].name != hardware_interface::HW_IF_POSITION)
  {
    RCLCPP_FATAL(
      rclcpp::get_logger("RRBotModularJoint"), "Joint '%s' have %s state interface. '%s' expected.",
      joint.name.c_str(), joint.state_interfaces[0].name.c_str(),
      hardware_interface::HW_IF_POSITION);
    return hardware_interface::CallbackReturn::ERROR;
  }

  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn CustomHardware::on_configure(const rclcpp_lifecycle::State & /*previous_state*/)
{
  for(uint i = 0; i<hw_commands_.size(); i++){
    hw_commands_[i] = 0;
    hw_states_position_[i] = 0;
  }
  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn CustomHardware::on_activate(const rclcpp_lifecycle::State & /*previous_state*/)
{
  std::string port = "/dev/ttyACM0"; // EDIT TO PROPER PORT WHEN USED
  SerialPort = open(port.c_str(), O_RDWR);

  if(SerialPort < 0){
    return hardware_interface::CallbackReturn::ERROR;
  }
  if(tcgetattr(SerialPort, &tty) != 0){
    return hardware_interface::CallbackReturn::ERROR;
  }

  tty.c_cflag &= ~PARENB;
  tty.c_cflag &= ~CSTOPB;
  tty.c_cflag &= ~CSIZE;
  tty.c_cflag |= ~CS8;
  tty.c_cflag &= ~CRTSCTS;
  tty.c_cflag |= CREAD | CLOCAL;

  tty.c_cflag &= ~ICANON;
  tty.c_cflag &= ~ECHO;
  tty.c_cflag &= ~ECHOE;
  tty.c_cflag &= ~ECHONL;
  tty.c_cflag &= ~ISIG;
  tty.c_cflag &= ~(IXON | IXOFF | IXANY);
  tty.c_cflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL);

  tty.c_oflag &= ~OPOST;
  tty.c_oflag &= ~ONLCR;

  tty.c_cc[VTIME] = 1;
  tty.c_cc[VMIN] = 1;

  speed_t speed = B115200;
  cfsetospeed(&tty, speed);
  cfsetospeed(&tty, speed);

  tcflush(SerialPort, TCIOFLUSH);
  if(tcsetattr(SerialPort, TCSANOW, &tty) != 0){
    close(SerialPort);
    return hardware_interface::CallbackReturn::ERROR;
  }

  auto t_start = std::chrono::high_resolution_clock::now();
  while(true){
    auto t_end = std::chrono::high_resolution_clock::now();
    double elapsed_time_ms = std::chrono::duration<double, std::milli>(t_end-t_start).count();
    if(elapsed_time_ms > 3000){
      break;
    }
  }

  return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn CustomHardware::on_deactivate(const rclcpp_lifecycle::State & /*previous_state*/)
{
  if(SerialPort == -1){
    return hardware_interface::CallbackReturn::ERROR;
  }

  tcflush(SerialPort, TCIOFLUSH);
  close(SerialPort);

  return hardware_interface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface> CustomHardware::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;
  for (auto i = 0u; i < info_.joints.size(); i++)
  {
    state_interfaces.emplace_back(hardware_interface::StateInterface(
      info_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_states_position_[i]));
  }

  return state_interfaces;
}

std::vector<hardware_interface::CommandInterface> CustomHardware::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;
  for (auto i = 0u; i < info_.joints.size(); i++)
  {
    command_interfaces.emplace_back(hardware_interface::CommandInterface(
      info_.joints[i].name, hardware_interface::HW_IF_POSITION, &hw_commands_[i]));
  }

  return command_interfaces;
}

hardware_interface::return_type CustomHardware::read(const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
  unsigned char r[1] = {'r'};
  WriteToSerial(r, 1);
  float ret[] = {0,0,0,0,0,0,0,0};
  uint8_t* v = (uint8_t*)ret;
  ReadSerial(v, sizeof(ret));

  return hardware_interface::return_type::OK;
}

hardware_interface::return_type CustomHardware::write(const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
  const int sz = hw_commands_.size();
  double ret[sz];

  for (auto i = 0u; i < hw_commands_.size(); i++)
  {
    // Simulate sending commands to the hardware
    RCLCPP_INFO(
      rclcpp::get_logger("DiffBotSystemHardware"), "Got command %.5f for '%s'!", hw_commands_[i],
      info_.joints[i].name.c_str());

    hw_states_position_[i] = hw_commands_[i];
    ret[i] = hw_commands_[i];
  }
  unsigned char w[1] = {'w'};
  WriteToSerial(w, 1);
  ::write(SerialPort, ret, 8*hw_commands_.size());

  return hardware_interface::return_type::OK;
}

int CustomHardware::WriteToSerial(unsigned char* buf, int nBytes){
  return ::write(SerialPort, buf, nBytes);
}

int CustomHardware::ReadSerial(unsigned char* buf, int nBytes){
  auto t_start = std::chrono::high_resolution_clock::now();
  int n = 0;
  while(n < nBytes){
    int ret = ::read(SerialPort, &(buf[n]), 1);
    if(ret < 0){
      return ret;
    }

    n += ret;
    auto t_end = std::chrono::high_resolution_clock::now();
    double elapsed_time_ms = std::chrono::duration<double, std::milli>(t_end-t_start).count();
    if(elapsed_time_ms > 10000){
      break;
    }
  }
  return n;
}

}

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(custom_hardware::CustomHardware, hardware_interface::SystemInterface)
