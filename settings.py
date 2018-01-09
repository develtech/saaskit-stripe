# -*- coding: utf-8 -*-
from django.conf import settings

#: saaskit default settings
SAASKIT_STRIPE_DEFAULTS = {
    # This setting sets the model target for the customer_relation field
    #
    # Purpose:
    #
    # Your website will probably want to associate the stripe customer
    # with an user/account/group/company or some other object.
    #
    # This sets the field "to" field on a OneToOneField
    #
    # It defaults to settings.AUTH_USER_MODEL
    'CUSTOMER_RELATION_TO': settings.AUTH_USER_MODEL,
    # This setting toggles the "null" arg on Customer.customer_relation
    #
    # Purpose:
    #
    # Strictly enforce relation with Customer model and other django model
    # Make this False if you need to sync stripe customers with no established
    # relation to your CUSTOMER_RELATION_MODEL (whether or not you intend
    # on adding it in the future.)
    #
    # This means even if it's your intention to associate all stripe customers
    # with a CUSTOMER_RELATIONAL_MODEL object/row, your import script may
    # need to set this to True unless you're prepared to *immediately* include
    # the customer_relation before saving.
    'CUSTOMER_RELATION_NULLABLE': True,
}


def saaskit_stripe_setting(key):
    """Return stripe setting/switchable settings.

    If no SAASKIT_STRIPE in settings, will default to SAASKIT_STRIPE_DEFAULTS.

    If no setting present in SAASKIT_STRIPE for key, defaults to
    SAASKIT_STRIPE_DEFAULTS.

    If key is not in SAASKIT_STRIPE_DEFAULTS (invalid setting), a KeyError
    will be raised.

    :param key: setting to pull from settings.SAASKIT_STRIPE/defaults
    :type key: string
    :returns: key inside of settings.SAASKIT_STRIPE, falls back on
        SAASKIT_STRIPE_DEAFULTS.
    :rtype: string, bool
    :raises: KeyError
    """
    try:
        subsettings = settings.SAASKIT_STRIPE
    except AttributeError:
        return SAASKIT_STRIPE_DEFAULTS[key]

    try:
        subsettings[key]
    except KeyError:
        return SAASKIT_STRIPE_DEFAULTS[key]
