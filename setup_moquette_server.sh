#!/bin/bash
echo "Cloning MQTT repo..."
git clone https://github.com/moquette-io/moquette
echo "Reverting repo to required version.."
cd moquette
git reset --hard e59217bd10dd70a028ff25c8da40b68f0190f2e5
echo "Building source files..."
./gradlew clean moquette-distribution:distMoquetteTar
echo "Unpacking build..."
cd distribution/build
tar xvf moquette-0.12.1.tar.gz
echo "Setup complete!"
