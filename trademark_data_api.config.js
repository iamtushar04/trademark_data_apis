module.exports = {
  apps: [
    {
      name: "trademark-data-apis-app",  // Name of your PM2 process
      script: "uvicorn",  // The command to run
      args: "main:app --reload --port 5040",  // Arguments to the gunicorn command
      interpreter: "/root/tools/backend/trademark_data_apis/.venv/bin/python",  // Path to the Python interpreter in your virtual environment
      watch: false,  // Set to true if you want PM2 to watch for file changes
      autorestart: true,  // Enable automatic restart on failure
      instances: 1,  // Number of instances to run
      exec_mode: "fork",  // Use 'cluster' for multiple instances
      env: {
        FLASK_ENV: "production",  // Environment variables
      },
    },
  ],
};
