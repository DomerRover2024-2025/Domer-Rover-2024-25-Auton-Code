#ifndef CUSTOM_HARDWARE_HPP_
#define CUSTOM_HARDWARE_HPP_

#include <memory>
#include <string>
#include <vector>

#include <termios.h>

#include "hardware_interface/actuator_interface.hpp"
#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclcpp/macros.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"

namespace custom_hardware
{
class CustomHardware : public hardware_interface::SystemInterface
{
    public:
        RCLCPP_SHARED_PTR_DEFINITIONS(CustomHardware)

        hardware_interface::CallbackReturn on_init(const hardware_interface::HardwareInfo & info) override;

        std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

        std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

        hardware_interface::CallbackReturn on_configure(
            const rclcpp_lifecycle::State & previous_state) override;

        hardware_interface::CallbackReturn on_activate(
            const rclcpp_lifecycle::State & previous_state) override;

        hardware_interface::CallbackReturn on_deactivate(
            const rclcpp_lifecycle::State & previous_state) override;

        hardware_interface::return_type read(
            const rclcpp::Time & time, const rclcpp::Duration & period) override;

        hardware_interface::return_type write(
            const rclcpp::Time & time, const rclcpp::Duration & period) override;

    private:
        std::vector<double> hw_commands_;
        std::vector<double> hw_states_position_;
        int SerialPort = -1;
        struct termios tty;

        int WriteToSerial(unsigned char* buf, int nBytes);
        int ReadSerial(unsigned char* buf, int nBytes);
};

}

#endif
