const { exec } = require('node:child_process')
const { promisify } = require('node:util')

// Promisify correctly handles the (cmd, options, callback) signature
const execAsync = promisify(exec)

exports.runCmd = async (cmd, options = {}) => {
  try {
    // This is the standard!
    const { stdout, stderr } = await execAsync(cmd, options)
    return stdout
  } catch (err) {
    // If it fails with options, you can try a fallback without them
    // though usually, errors here are command-related, not signature-related
    const { stdout } = await execAsync(cmd)
    return stdout
  }
}
