from anki.hooks import wrap
from anki.utils import ids2str

from aqt.qt import *
from aqt.deckbrowser import DeckBrowser
from aqt.reviewer import Reviewer
from aqt.utils import showInfo,tooltip


class RepRetire:

    def __init__(self, mw):
        self.mw = mw

        self.action = QAction(self.mw)
        self.action.setText("Run Rep Retire")
        self.mw.form.menuTools.addAction(self.action)
        self.action.triggered.connect(self.run)
        
        Reviewer._answerCard = wrap(Reviewer._answerCard, self.trigger, "after")
        DeckBrowser._renderStats = wrap(DeckBrowser._renderStats, self.build_config, "after")


    def build_config(self, orig):
        self.config = self.mw.addonManager.getConfig(__name__)
        decks = self.mw.col.decks.all()

        for deck in decks:
            if str(deck['id']) not in self.config:
                self.config[str(deck['id'])] = {
                    'name':      deck['name'],
                    'threshold': 40,
                    'enabled':   False,
                    'tag':       'RETIRED'
                }

        self.mw.addonManager.writeConfig(__name__, self.config)
        


    def run(self):
        self.config = self.mw.addonManager.getConfig(__name__)
        decks = self.mw.col.decks.all()

        for deck in decks:
            if str(deck['id']) in self.config:
                settings = self.config[str(deck['id'])]
                if settings['enabled']:
                    ids_and_nids = self.mw.col.db.all("select id,nid from cards where queue != -1 and ivl >= %s and did = %s" % (
                        settings['threshold'], deck['id']
                    ))
                    ids  = [i[0] for i in ids_and_nids]
                    nids = [i[1] for i in ids_and_nids]

                    self.suspend(ids)
                    self.tag(nids, settings['tag'])
                    self.mw.requireReset()


    def trigger(self, reviewer=None, answer=None):
        self.config = self.mw.addonManager.getConfig(__name__)
        if reviewer is not None and answer in [2,3,4]:
            card = reviewer.lastCard()
            if card is not None:
                settings = self.config[str(card.did)]

                if settings['enabled'] and int(card.ivl) >= int(settings['threshold']):
                    self.suspend([card.id])
                    self.tag([card.nid], settings['tag'])


    def suspend(self, ids):
        if ids is None or len(ids) <= 0:
            return False
        self.mw.col.db.execute("update cards set queue = -1 where id in %s" % ids2str(ids))
        tooltip(ngettext("Retired %d Card", "Retired %d Cards", len(ids)) % len(ids))    
        return True


    def tag(self,nids,tag):
        if nids is None or len(nids) <= 0 or tag == "":
            return False
        self.mw.col.tags.bulkAdd(nids, tag)
        return True
