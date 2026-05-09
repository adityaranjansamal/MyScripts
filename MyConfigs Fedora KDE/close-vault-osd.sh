#!/bin/bash

STATUS=$(qdbus org.kde.kded6 /modules/plasmavault org.kde.plasmavault.hasOpenVaults)

if [ "$STATUS" != "true" ]; then
    kdialog \
    --icon folder-locked-symbolic \
    --passivepopup "Vault not unlocked!" 2
    exit 0
fi

qdbus org.kde.kded6 /modules/plasmavault closeAllVaults

sleep 1

NEW_STATUS=$(qdbus org.kde.kded6 /modules/plasmavault org.kde.plasmavault.hasOpenVaults)

if [ "$NEW_STATUS" = "false" ]; then
    kdialog \
    --icon folder-locked-symbolic \
    --passivepopup "Vault Locked" 2
else
    kdialog \
    --icon folder-important-symbolic \
    --passivepopup "Vault close failed!" 3
fi
