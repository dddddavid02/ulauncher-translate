from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from src.functions import arg_to_help

ICON_FILE = 'images/icon.png'

def no_input_item():
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='No input',
            on_enter=DoNothingAction()
        )
    ]


def no_translation_available():
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='No translation available',
            on_enter=DoNothingAction()
        )
    ]

def missing_dep_item():
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='Translate-shell is required for this extension',
            description="Select to follow install instructions",
            on_enter=OpenUrlAction('https://github.com/soimort/translate-shell#installation')
        )
    ]


def generate_trans_item(translation, original, from_lang, to_lang):
    return ExtensionResultItem(
        icon=ICON_FILE,
        name=translation,
        description='{}: {}'.format(to_lang, original),
        on_enter=ExtensionCustomAction([translation, original, from_lang, to_lang], keep_app_open=True)
    )


def generate_trans_items(translations, from_languages):
    return [
        generate_trans_item(translation, original, from_lang, to_lang)
    for (translation, original, to_lang) in translations for from_lang in from_languages]


def generate_back_item(translations, parser):
    return ExtensionResultItem(
        icon='images/back.png',
        name='Go back',
        on_enter=RenderResultListAction(generate_trans_items(translations, parser.from_lang.split('+')))
    )


def generate_copy_item(translation):
    return ExtensionResultItem(
        icon='images/copy.png',
        name='Copy to clipboard',
        description=translation,
        on_enter=CopyToClipboardAction(translation)
    )


def generate_trans_link_item(original, from_lang, to_lang):
    return ExtensionResultItem(
        icon='images/open.png',
        name='Open in Google Translate',
        description='https://translate.google.com/?sl={}&tl={}&text={}&op=translate'.format(from_lang, to_lang, original),
        on_enter=OpenUrlAction('https://translate.google.com/?sl={}&tl={}&text={}&op=translate'.format(from_lang, to_lang, original))
    )


def lang_items(from_lang, to_lang):
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='Translating {} -> {}'.format(from_lang, lang),
            description='With Google Translation engine',
            on_enter=DoNothingAction()
        )
    for lang in to_lang.split('+')]


def generate_args_items(args):
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='{}: {}'.fromat(arg, arg_to_help(arg)),
            on_enter=DoNothingAction()
        )
    for arg in args]


def show_used_args(parser):
    return lang_items(parser.from_lang, parser.to_lang) \
        + generate_args_items(parser.args)