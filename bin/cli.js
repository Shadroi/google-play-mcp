#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Determine the root directory of the package
const packageRoot = path.join(__dirname, '..');
const venvDir = path.join(packageRoot, '.venv');
const requirementsFile = path.join(packageRoot, 'requirements.txt');

// Platform specific paths
const isWindows = process.platform === 'win32';
const pythonExecutable = isWindows
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python');

const pipExecutable = isWindows
    ? path.join(venvDir, 'Scripts', 'pip.exe')
    : path.join(venvDir, 'bin', 'pip');

function runCommand(command, args, options = {}) {
    return new Promise((resolve, reject) => {
        const proc = spawn(command, args, {
            stdio: 'inherit',
            cwd: packageRoot,
            ...options
        });

        proc.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error(`Command exited with code ${code}`));
            }
        });

        proc.on('error', (err) => {
            reject(err);
        });
    });
}

async function setupEnvironment() {
    console.log('Initializing Python virtual environment...');

    // Create venv if it doesn't exist
    if (!fs.existsSync(venvDir)) {
        console.log('Creating .venv...');
        try {
            await runCommand('python3', ['-m', 'venv', '.venv']);
        } catch (e) {
            // Try just 'python' if 'python3' fails (e.g. Windows)
            await runCommand('python', ['-m', 'venv', '.venv']);
        }
    }

    // Install dependencies
    if (fs.existsSync(requirementsFile)) {
        console.log('Installing dependencies...');
        await runCommand(pipExecutable, ['install', '-r', 'requirements.txt']);
    }
}

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    // Check if environment needs setup
    if (!fs.existsSync(pythonExecutable)) {
        try {
            await setupEnvironment();
        } catch (error) {
            console.error('Failed to setup Python environment:', error);
            process.exit(1);
        }
    }

    // Determine which script to run
    let scriptToRun;
    let pythonArgs = [];

    if (command === 'init-key') {
        scriptToRun = 'setup_key.py';
        pythonArgs = args.slice(1);
    } else if (command === 'start' || !command) {
        scriptToRun = 'server.py';
        pythonArgs = args.slice(1);
        if (command === 'start') {
            pythonArgs = args.slice(1); // 'start' is consumed
        } else {
            pythonArgs = args; // No command provided, pass all args
        }
    } else {
        // Unknown command, maybe it's an arg for server.py?
        // Default to running server.py with these args
        scriptToRun = 'server.py';
        pythonArgs = args;
    }

    const scriptPath = path.join(packageRoot, scriptToRun);

    try {
        await runCommand(pythonExecutable, [scriptPath, ...pythonArgs]);
    } catch (error) {
        console.error('Error executing script:', error);
        process.exit(1);
    }
}

main();
