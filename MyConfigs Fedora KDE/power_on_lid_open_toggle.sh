#!/bin/bash

ATTRIBUTE_PATH="/sys/class/firmware-attributes/samsung-galaxybook/attributes/power_on_lid_open"
VALUE_FILE="$ATTRIBUTE_PATH/current_value"

# Check for sudo/root
if [[ $EUID -ne 0 ]]; then
    echo "REQUIRE ADMIN RIGHTS! RUN USING SUDO."
    exit 1
fi

# Check if device supports the feature
if [[ ! -d "$ATTRIBUTE_PATH" ]]; then
    echo "DEVICE NOT SUPPORTED!"
    exit 1
fi

while true; do
    clear
    echo "================================="
    echo "     Power ON when lid open"
    echo "================================="
    echo
    echo "0. Show current status"
    echo "1. Turn ON"
    echo "2. Turn OFF"
    echo "3. Exit"
    echo

    read -rp "Enter option: " option
    echo

    case $option in
        0)
            current=$(cat "$VALUE_FILE" 2>/dev/null)

            if [[ "$current" == "1" ]]; then
                echo "Current Status: ON"
            elif [[ "$current" == "0" ]]; then
                echo "Current Status: OFF"
            else
                echo "Unable to read current status."
            fi

            echo
            echo "0 -> OFF"
            echo "1 -> ON"
            ;;

        1)
            echo 1 > "$VALUE_FILE"

            if [[ $? -eq 0 ]]; then
                echo "Successfully turned ON."
                echo "Reboot device to apply changes."
            else
                echo "Failed to turn ON."
            fi
            ;;

        2)
            echo 0 > "$VALUE_FILE"

            if [[ $? -eq 0 ]]; then
                echo "Successfully turned OFF."
                echo "Reboot device to apply changes."
            else
                echo "Failed to turn OFF."
            fi
            ;;

        3)
            echo "Exiting..."
            exit 0
            ;;

        *)
            echo "Invalid option!"
            ;;
    esac

    echo
    read -rp "Press Enter to continue..."
done
