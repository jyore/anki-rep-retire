import json

from anki.hooks import wrap
from anki.utils import ids2str

from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.webview import AnkiWebView
from aqt.utils import showInfo,tooltip




class Settings:

  def __init__(self, enabled=False, threshold=40, tag="RETIRED"):
    self.enabled   = enabled
    self.threshold = threshold
    self.tag       = tag

  def reset(self):
    self.enabled   = False
    self.threshold = 40
    self.tag       = "RETIRED"


  def obj(self):
    return vars(self)


DEFAULTS = Settings()


class ConfigurationManager:

  def __init__(self, mw, fn="repretire.json"):
    self.mw = mw
    self.fn = os.path.join(self.mw.pm.addonFolder(), fn)


  def load(self):
    self.settings = {}
    self.deck_map = {}

    try:
      with open(self.fn, 'r') as f:
        saved = json.load(f)
    except Exception as e:
      saved = {}


    skeys = saved.keys()
    decks = self.mw.col.decks.all()

    for deck in decks:
      did = str(deck['id'])
      name = deck['name']

      if did not in skeys:
        saved[did] = Settings().obj()

      self.deck_map[name] = did
      

    for did in saved:
      s = saved[did]
      self.settings[did] = Settings(
        enabled   = s['enabled'] if 'enabled' in s else DEFAULTS.enabled,
        threshold = s['threshold'] if 'threshold' in s else DEFAULTS.threshold,
        tag       = s['tag'] if 'tag' in s else DEFAULTS.tag,
      )


  def save(self):
    out = {}
    for deck in self.settings:
      out[deck] = self.settings[deck].obj()

    with open(self.fn, 'w') as f:
      f.write(json.dumps(out))


  def deck_list(self):
    return self.settings.keys()

  def deck_names(self):
    return self.deck_map.keys()

  def id_from_name(self, name):
    return self.deck_map[name]

  def __getitem__(self,key):
    return self.settings[key]
        


class UI:

  def __init__(self, mw, cm):
    self.mw = mw
    self.cm = cm
    self.controls = {}
    self.selected = 0


  def widgets(self, window):
    self.db = QComboBox()
    self.db.addItems(self.cm.deck_names())
    self.db.currentIndexChanged.connect(self.select_deck)

    self.enabled = QCheckBox("Enabled")
    self.enabled.stateChanged.connect(self.enabled_changed)

    self.threshold = QLineEdit()
    self.threshold.setValidator(QIntValidator())
    self.threshold.textChanged.connect(self.threshold_changed)

    self.tag = QLineEdit()
    self.tag.textChanged.connect(self.tag_changed)

    self.defaults = QPushButton("Defaults")
    self.defaults.clicked.connect(self.reset)

    self.cancel = QPushButton("Cancel")
    self.cancel.connect(self.cancel, SIGNAL("clicked()"), window, SLOT("reject()"))
    
    self.save = QPushButton("Save && Run")
    self.save.connect(self.save, SIGNAL("clicked()"), window, SLOT("accept()"))
    



  def layout(self, window):
    self.cm.load() 

    hz_group_box = QGroupBox()
    layout = QGridLayout()
    self.widgets(window)

    layout.addWidget(QLabel("Select Deck:"), 0, 0, 1, 12)
    layout.addWidget(self.db, 1, 0, 1, 8)
    layout.addWidget(self.enabled, 1, 9, 1, 3)

    layout.addWidget(QLabel(""), 2, 0, 1, 12)

    layout.addWidget(QLabel("Threshold (days):"), 3, 0, 1, 6)
    layout.addWidget(QLabel("Tag As:"), 3, 6, 1, 6)

    layout.addWidget(self.threshold, 4, 0, 1, 6)
    layout.addWidget(self.tag, 4, 6, 1, 6)

    layout.addWidget(QLabel(""), 5, 0, 1, 12)

    layout.addWidget(self.defaults, 6, 0, 1, 3)
    layout.addWidget(self.cancel, 6, 6, 1, 3)
    layout.addWidget(self.save, 6, 9, 1, 3)


    hz_group_box.setLayout(layout)

    self.select_deck(0)
    return hz_group_box


  def current_settings(self):
    return self.cm[str(self.mw.col.decks.all()[self.selected]['id'])]


  def select_deck(self, index):
    self.selected = index
    settings = self.current_settings()
    self.enabled.setChecked(settings.enabled)
    self.threshold.setText(str(settings.threshold))
    self.tag.setText(settings.tag)


  def enabled_changed(self, index):
    settings = self.current_settings()
    settings.enabled = self.enabled.isChecked()


  def threshold_changed(self, index):
    settings = self.current_settings()
    settings.threshold = self.threshold.text()


  def tag_changed(self, index):
    settings = self.current_settings()
    settings.tag = self.tag.text()


  def reset(self):
    self.current_settings().reset()
    self.select_deck(self.selected)




class RepRetire:

  def __init__(self, mw):
    self.mw = mw

    self.cm = ConfigurationManager(self.mw)
    self.ui = UI(self.mw, self.cm)
    
    self.conf_action = QAction("Rep Retire", self.mw)
    self.mw.connect(self.conf_action, SIGNAL("triggered()"), self.setup)
    self.mw.form.menuTools.addAction(self.conf_action)


    Reviewer._answerCard = wrap(Reviewer._answerCard, self.trigger, "after")


  def setup(self):
    self.swin = QDialog(mw)
    self.swin.setWindowTitle("Rep Retire Configuration")

    layout = QVBoxLayout()
    layout.addWidget(self.ui.layout(self.swin))

    self.swin.setLayout(layout)

    if self.swin.exec_():
      self.mw.progress.start(immediate=True)
      self.cm.save()
      self.run()
      self.mw.progress.finish()



  def trigger(self, reviewer=None, answer=None):
    self.cm.load()

    if reviewer is not None and answer in [2,3,4]:
      card = reviewer.lastCard()
      if card is not None:
        settings = self.cm[str(card.did)]

        if settings.enabled and int(card.ivl) >= int(settings.threshold):
          self.suspend([card.id])
          self.tag([card.nid], settings.tag)



  def run(self):
    for deck in self.cm.deck_list():
      settings = self.cm[deck]

      if settings.enabled:
        ids_and_nids = self.mw.col.db.all("select id,nid from cards where queue != -1 and ivl >= %s and did = %s" % (settings.threshold, deck))
        ids  = [i[0] for i in ids_and_nids]
        nids = [i[1] for i in ids_and_nids]

        self.suspend(ids)
        self.tag(nids, settings.tag)
 


  def suspend(self, ids):
    if ids is None or len(ids) <= 0:
      return False
    mw.col.db.execute("update cards set queue = -1 where id in %s" % ids2str(ids))
    tooltip(ngettext("Retired %d Card", "Retired %d Cards", len(ids)) % len(ids))    
    return True


  def tag(self,nids,tag):
    if nids is None or len(nids) <= 0 or tag == "":
      return False
    mw.col.tags.bulkAdd(nids, tag)
    return True
  

mw.rep_retire = RepRetire(mw) 
