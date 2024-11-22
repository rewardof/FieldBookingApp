from user.permissions import create_groups


def create_groups_signal(sender, **kwargs):
    """
    post migration signal to create groups for users after migration
    """
    if sender.name == 'user':
        create_groups()
