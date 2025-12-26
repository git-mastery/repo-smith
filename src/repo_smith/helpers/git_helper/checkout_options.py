from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class CheckoutOptions(TypedDict, total=False):
    branch: bool


CHECKOUT_SPEC = CommandSpec().flag("branch", "-b", default=False)
