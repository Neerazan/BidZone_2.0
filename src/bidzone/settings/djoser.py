DJOSER = {
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'SERIALIZERS': {
        'user_create': 'src.core.serializers.UserCreateSerializer',
        'current_user': 'src.core.serializers.UserSerializer',
    },
    'EMAIL': {
        'activation': 'auction.email.ActivationEmail',
        'password_reset': 'auction.email.PasswordResetEmail',
    },
}
