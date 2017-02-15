from django.conf import settings
from django.utils.translation import ugettext_noop as _


def create_notice_types(sender, **kwargs):
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        NoticeType.create("Referral_registered", _("New Referral"), _("One referral of you, has join the page!"))
    else:
        print("Skipping creation of NoticeTypes as notification app not found")