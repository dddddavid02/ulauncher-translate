from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from src.functions import strip_list
from src.translate_shell import TranslateShell
from src.items import no_input_item, missing_dep_item, show_used_args, generate_trans_items, no_translation_available, generate_back_item, generate_copy_item, generate_trans_link_item

class TranslateExtension(Extension):
    def __init__(self):
        super(TranslateExtension, self).__init__()

        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


parser = None
translations = None


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()

        params = strip_list(query.split(' '))

        global parser
        parser = TranslateShell(extension.preferences, params)

        if parser.is_dep_missing():
            return RenderResultListAction(missing_dep_item())

        if len(query.strip()) == 0:
            return RenderResultListAction(no_input_item())

        if not parser.has_query():
            return RenderResultListAction(show_used_args(parser))

        global translations
        translations = parser.execute()

        if not translations:
            return RenderResultListAction(no_translation_available())

        return RenderResultListAction(generate_trans_items(translations, parser.from_lang.split('+')))


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):

        data = event.get_data()

        translation = data[0]
        original = data[1]
        from_lang = data[2]
        to_lang = data[3]

        return RenderResultListAction([
            generate_back_item(translations, parser),
            generate_copy_item(translation),
            generate_trans_link_item(translation, original, from_lang, to_lang)
        ])



if __name__ == '__main__':
    TranslateExtension().run()