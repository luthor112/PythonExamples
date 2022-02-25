import getpass
import ldap

SERVER_ADDRESS = "SERVER ADDRESS GOES HERE"
LOGIN_PREPEND = "PREPEND THIS TO THE USERNAME"
LOGIN_APPEND = "APPEND THIS TO THE USERNAME"

if __name__ == "__main__":
    ldap.set_option(ldap.OPT_REFERRALS, 0)  # Avoid errors by disabling referral chasing
    server = ldap.open(SERVER_ADDRESS)  # ldap.initialize("ldap://"+SERVER_ADDRESS) works as well
    username = raw_input("Login: ")
    password = getpass.getpass("Password: ")
    try:
        server.simple_bind_s(LOGIN_PREPEND+username+LOGIN_APPEND, password)
        print "Login successful!"
    except: # Varios classes exist representing different errors
        print "Login unsuccessful!"
    finally:
        print "Closing connection..."
        server.unbind_s()
