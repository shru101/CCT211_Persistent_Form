import boot
import home

exit_fog = False
boot_window = boot.Start()
while not exit_fog:
    home_window = home.HomeScreen()
    if not home_window.is_logged_in:
        if not home_window.is_logged_in:
            boot_window = boot.Start()
        else:
            exit_fog = True
    else:
        exit_fog = True

print("Code proccessed")

"""
TO DO LIST
- Fix signed in implementation
- Fix LIN writing when logging in (needs to write which account as well)
- library with treeview
-   add scroll bar to any listbox or treeview
- store with treeview
- account settings window
"""