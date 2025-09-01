# #!/usr/bin/env python3
# """
# Test runner script that disables pytest plugin autoloading to avoid OpenSSL conflicts.
# """
# import os
# import sys
# import subprocess

# def main():
#     # Set environment variable to disable plugin autoloading
#     env = os.environ.copy()
#     env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    
#     # Run pytest with the modified environment
#     cmd = [sys.executable, '-m', 'pytest'] + sys.argv[1:]
#     result = subprocess.run(cmd, env=env)
    
#     sys.exit(result.returncode)

# if __name__ == '__main__':
#     main()
