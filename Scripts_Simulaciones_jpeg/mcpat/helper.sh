#!/bin/bash

is_power_of_2() {
    local number="$1"
    [[ $(($number & ($number - 1))) -eq 0 && $number -ne 0 ]]
}