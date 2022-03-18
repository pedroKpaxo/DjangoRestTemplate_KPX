from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.user.models import User


class PasswordResetForm(DjangoPasswordResetForm):
    def get_users(self, email):
        return User.objects.filter(email=email, is_active=True)

    def save(self, domain_override=None, site_name_override=None,
             subject_template_name='restauth/password_reset_subject.txt',
             email_template_name='restauth/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                domain = current_site.domain
                site_name = current_site.name
            else:
                # Overwrite django's default to allow site_name override
                domain = domain_override
                site_name = site_name_override or domain
            user_email = user.email
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )
