# Overview

In our post-truth world, consider an image or video you watch. How do you know if it's AI-generated? How can you trust the very source of this image? The aim of Vusense is to provide a verifiable traceback to that very source by using a multi-layer signature record of the image itself, identifiers, and sensors.

The "identifiers" are UUIDs that are associated with attestation. User/Policy IDs, Device IDs, and Component IDs are all candidates (from top-down) for inclusion.

The "sensors" are both internal device and external timestamping, GPS location, Tower location (network), IMU orientation, and frankly any other low-latency reading we can get from the device. Technically, the image/video itself is also a "sensor".

The image and collection of identifiers and sensors (the "attestation signature") is then first checked to "pass" on mobile-side before getting encrypted and securely broadcast to a Vusense server. At server side, we decrypt and run a second "server-side" check. Any check failure returns message to user and logs failure. Upon passing, the attestation signature is injected into a L2 sidechain (thinking Hedera) or potentially a client-owned federated chain (like Hyperfabric).

## Project Naming Scheme

We'll need to set up repos. I propose SOLID seperate projects to avoid a monorepo. We ought use a standard naming scheme for our projects. I propose the format: **`[domain]-[function]-[optional-target]`**

* **`[domain]`** : The architectural boundary or layer (e.g., `sdk`, `core`, `ledger`, `web`, `shared`, `infra`). This groups related repos together alphabetically in GitHub.
* **`[function]`** : What the repository actually does (e.g., `server`, `adapter`, `schemas`, `dashboard`).
* **`[target]`** : (Optional) The specific technology or platform it applies to (e.g., `ios`, `android`, `hedera`).

## Proposed Project Structure

#### 1. The Mobile Layer (`sdk-`)

This is the "edge" layer - these repos may be semi-open for clients to use in their own apps.

* **`sdk-ios`** : The native iOS Swift library for sensor capture and local attestation.
* **`sdk-android`** : The native Android Kotlin library.
* **`sdk-demo-app`** : A bare-bones reference app to test and showcase the SDK integrations.

  **NOTE:** We could merge `ios` and `android` using React Native & Expo. May be a better option, since Expo allows C++ object handling. 

#### 2. The Shared Contracts (`shared-`)

* **`shared-protocol`**: The single source of truth for your data models. This holds your Protobufs, JSON schemas, or OpenAPI specs that both the `sdk` and `core` repos will import to ensure the "Attestation Signature" shape never drifts.
  * *See [attestation_schema.json](./attestation_schema.json) for the drafted ProofMode-compatible payload structure.*

#### 3. The Backend Layer (`core-`)

* **`core-server`** : The central backend orchestration service that handles decryption, second-pass validation, and event routing.

#### 4. The Blockchain Integrations (`ledger-`)

Using the `ledger-` prefix keeps all our DLT (Distributed Ledger Technology) concerns grouped together.

* **`ledger-adapter-hedera`** : The microservice that listens for valid attestations and pushes them to Hedera.
* **`ledger-adapter-fabric`** : The equivalent service for Hyperledger Fabric.
* **`ledger-contracts`** : The actual Solidity/Go/Rust smart contracts and chaincode deployed to the networks.

#### 5. User Interfaces (`web-`)

* **`web-dashboard`** : The React/Next.js frontend portal for clients and admins to view logs and manage policies. Maybe later stage build. This is implementation of MJ's [Etherscan](https://etherscan.io/) idea.

#### 6. Operations (`infra-`)

* **`infra-deployment`**: Our Terraform, Kubernetes manifests, or deployment scripts.
  **NOTE:** This might be moved to project-level: `deployment` directory in each project.
