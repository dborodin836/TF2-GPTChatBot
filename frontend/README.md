# Project Commands Guide

## Table of Contents

- [Running the Application](#running-the-application)
    - [`npm run dev`](#npm-run-dev)
    - [`npm run demo`](#npm-run-demo)
- [Development Utilities](#development-utilities)
    - [`npm run start`](#npm-run-start)
    - [`npm run electron:dev`](#npm-run-electrondev)
    - [`npm run electron:demo`](#npm-run-electrondemo)
- [Building and Packaging](#building-and-packaging)
    - [`npm run build`](#npm-run-build)
    - [`npm run pack`](#npm-run-pack)
- [Testing and Ejection](#testing-and-ejection)
    - [`npm run test`](#npm-run-test)
    - [`npm run eject`](#npm-run-eject)

Below is a detailed explanation of the commands defined in the `package.json` file of the project, which can be run
using `npm run <command>` from your terminal. These commands help manage the development, testing, building, and
packaging of your application.

## Running the Application

### `npm run dev`

Starts the application in the development environment. It concurrently runs both the Electron process and the Vite
server. It loads Electron with development environment settings and starts the Vite server for serving the Electron
application. **Note that the backend must be started manually.**

### `npm run demo`

Starts the application in a demo environment, which is useful for previewing the app without packaging the app.
Similar to the development environment, it runs both the Electron process in demo mode and the Vite server. Python
backend is started automatically.

## Development Utilities

### `npm run start`

Serves the application using Vite. This command is configured to disable the default browser launching, making it useful
only when used together with an Electron shell, as Electron independently opens a window to load the app.

### `npm run electron:dev`

Starts the Electron process in the development environment. It waits until the Vite server at tcp:3000 is ready before
launching Electron with specific environment variables to enhance development, such as enabling the backend API and
developer tools.

### `npm run electron:demo`

Launches the Electron process in the demo environment. This setup is similar to the development setup but with fewer
development tools enabled. It waits for the Vite server to be ready before launching.

## Building and Packaging

### `npm run build`

Builds the React application using Vite, tailored for an Electron environment. This ensures that the build output is
compatible with the Electron platform.

### `npm run pack`

Builds and then packages the application using Electron Builder. This command ensures that your application is ready for
distribution, creating installable software packages for supported operating systems.

## Testing and Ejection

### `npm run test`

Placeholder command for running tests, which isn't implemented yet.

### `npm run eject`

Placeholder command for ejecting the configuration files of the build tool. This isn't implemented at the moment.