import garth

from getpass import getpass

email = input("Enter your email address: ")
password = getpass("Enter your password: ")
save_path = input("Enter path to save credentials (empty for ~/.garth): ")
if not save_path:
    save_path = "~/.garth"

# If there's MFA, you'll be prompted during the login
garth.login(email, password)

garth.save(save_path)

print(f"Successfuly saved credentials to {save_path}")

