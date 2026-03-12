# Secure Net Stack Architecture

## Overview
- Modular Python framework
- Components: Node, Networking, Encryption

## Networking
- `SecureSocket`: basic TCP wrapper
- Ready for expansion with P2P protocols

## Encryption
- Symmetric encryption using Fernet (from the `cryptography` library)
- `SecureChannel` provides `encrypt()` and `decrypt()` methods

## Node
- `NetworkNode` integrates `SecureSocket` and `SecureChannel`
- Exposes `send_message()` and `receive_message()` for encrypted communication
