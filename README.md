# python-airmash

Python client API for Airma.sh

This is an experimental Python client which uses construct to handle parsing of binary data from the server to the client,
and encoding of binary packets from the client to the server.

All of the client<->server packets are implemented, but not all of them have been fully tested. There's lots still to do!

# Feedback / Contributions

Discuss this project on the unofficial Airmash Discord server: https://discord.gg/FuwGezZ

# Objectives

This library is intended to be a set of tools for building Airmash client applications such as bots, stats monitors, chat clients, etc.

This library is by no means intended to be a complete Airmash client. You should implement your own display/analysis routines, or log in to Airma.sh and spectate your bot for diagnosis.

This library is entirely unofficial and all commands are reverse-engineered from the Javascript client. As such it may not be 100% correct, and may break with new game releases.
