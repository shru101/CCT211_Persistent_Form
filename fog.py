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
