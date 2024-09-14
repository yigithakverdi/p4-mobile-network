#!/bin/bash

# Function to display network information for a device
display_network_info() {
    device=$1
    echo "Network information for $device:"
    kathara exec $device ifconfig
    echo "Routing table for $device:"
    kathara exec $device route -n
    echo "----------------------------"
}

# Main monitoring loop
while true; do
    clear
    echo "Monitoring Kathara lab network..."
    echo "================================"
    
    # Get list of running devices
    devices=$(kathara ps --quiet)
    
    # Display network information for each device
    for device in $devices; do
        display_network_info $device
    done
    
    # Wait for 5 seconds before refreshing
    sleep 5
done
