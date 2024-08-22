# noqa: A005

from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'account/activation.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['frontend_url'] = f"http://localhost:5173/activate-user/{context['uid']}/{context['token']}"
        return context


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'account/password_reset.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['frontend_url'] = f"http://localhost:5173/reset-password/{context['uid']}/{context['token']}"
        return context
