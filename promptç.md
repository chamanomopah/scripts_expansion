Role: Senior DevOps Engineer & Node.js Windows Specialist.

Context:
I am running a Node.js v20 environment on Windows. I frequently encounter the "Error: connect EPERM //./pipe/rpc.sock" when trying to use PM2. This is caused by a permission mismatch between the PM2 daemon (likely spawned by a different user or Admin context) and my current CLI session.

Goal:
I need a "fix-and-forget" PowerShell automation script that I can run once as Administrator to:
1. PERMANENTLY fix the permission issues.
2. Ensure PM2 starts automatically on Windows boot without errors.
3. Allow me to run `pm2` commands from my standard user terminal without needing constant Admin rights.

Task:
Generate a comprehensive `setup_pm2_robust.ps1` script that performs the following steps safely:
1. Cleanup: Kill all running PM2 processes and delete the existing `C:\Users\Lofrey\.pm2` directory (nuclear option to remove locked socket files).
2. Environment: Set a system-wide environment variable `PM2_HOME` to a custom, accessible path (e.g., `C:\.pm2` or `C:\pm2_data`) to avoid user-profile permission conflicts.
3. Installation: Install the `@nick92/pm2-windows-service` (or the most reliable current equivalent) global package.
4. Service Configuration: Run the necessary commands (`pm2-service-install`) to install PM2 as a Windows Service that runs ON BOOT.
   - Crucial: The script should configure the service to run preferably as the current user OR ensure the `PM2_HOME` permissions allow my user to connect to the pipe.
5. Verification: Add a step to start a dummy process (e.g., `pm2 start echo --name "test-service"`), save the list, and verify `pm2 list` works.

problem: connect EPERM //./pipe/rpc.sock
[PM2] Spawning PM2 daemon with pm2_home=C:\Users\Lofrey\.pm2
node:events:497
      throw er; // Unhandled 'error' event
      ^

Error: connect EPERM //./pipe/rpc.sock
    at PipeConnectWrap.afterConnect [as oncomplete] (node:net:1607:16)
Emitted 'error' event on ReqSocket instance at:
    at Socket.<anonymous> (C:\Users\Lofrey\AppData\Roaming\npm\node_modules\pm2\node_modules\pm2-axon\lib\sockets\sock.js:201:49)
    at Socket.emit (node:events:519:28)
    at emitErrorNT (node:internal/streams/destroy:169:8)
    at emitErrorCloseNT (node:internal/streams/destroy:128:3)
    at process.processTicksAndRejections (node:internal/process/task_queues:82:21) {
  errno: -4048,
  code: 'EPERM',
  syscall: 'connect',
  address: '//./pipe/rpc.sock'
}

Node.js v20.18.0

Output Requirements:
- Provide ONLY the robust PowerShell script.
- Add comments explaining what each block does.
- Include a small "How to use" section telling me exactly how to execute this script as Admin.
