anki-rep-retire
===============

This add-on allows you to automatically retire cards after they grow past a certain interval. At a certain point, the knowledge on any given card will be committed to memory or has material that is intrinsically covered through other cards. Continuing to rep cards at this level of maturity is not worth the time spent reviewing when comparing what benefit you are gaining from the review. 

By using this add-on, you can tailor a specific threshold for each one of your decks. When reviewing cards from a deck, if a card's new interval exceeds the configured threshold, then that card will be `retired`. A `retired` card will be automatically suspended and tagged so that you no longer will see this card in reps and that you can easily find a whole list of retired cards in the browser. If you want to practice a retired card again, you can simply unsuspend and remove the tag, then reset the card.

> **Note**: The mobile app cannot run add-ons, so you cannot gain the benefit from the automatic trigger that runs after a review  when using anki mobile. To run the retire algorithm over all cards, simply open the add-on configuration menu on desktop anki after syncing all of your reviews and hit the `Save & Run` button. This will retire all cards that need to be retired from your mobile review session.


# Installing Rep Retire

Installing this add-on is done by following these steps:

- Visit the [Releases](https://github.com/jyore/anki-rep-retire/releases) page
- Download the latest release
- Copy the `RepRetire.py` file to the Anki Addon directory
  - To find the Add-ons direcory, in Anki, click `Tools->Add-ons->Open Add-ons Folder`
- Restart Anki


# Running Rep Retire

After installing, by default, Rep Retire is disabled for all decks. You must open the configuration menu to enable and configure thresholds for each deck you wish to enable automatic-retiring on.

Defaulting the add-on to off was done inentionally to minimize the impact the add-on may have before users have had the opportunity to configure everything how they desire.

To begin configuring Rep Retire, in Anki, click `Tools->Rep Retire`. You should see an image similar to below:

![Rep Retire](https://user-images.githubusercontent.com/904738/48365260-0cc89e00-e670-11e8-85dd-2892d335d4a6.png)

There are several fields to fill out:

- **Select Deck**: This is a dropdown that will auto-populate with all of the decks in your profile. When selecting a deck, all of the other fields will change to reflect the settings for that deck
- **Enabled**: If it is _checked_, then Rep Retire is active for this deck.
- **Threshold**: The threshold at which a card in the selected should be retired when it's new-interval exceeds.
- **Tag As**: What to tag a card with when they are retired, for the selected deck
- **Defaults**: Restores the default settings for the selected deck
- **Cancel**: Cancel configuration, do not save any values.
- **Save & Run**: Save configuration and run the algorithm for all enabled decks.


# Reviewing w/ Rep Retire

Once Rep Retire is enabled for a deck, it will execute the algorithm after every card has been answered correctly to determine if it should be retired or not. It if is retired, you will receive a tool-tip notification that the card was retired. When saving configuration settings, it will run the algorithm over all enabled decks and retire any cards it determines to need retiring. Again, for those who review on Anki mobile, to retroactively retire cards, open anki desktop, open the Rep Retire Configuration settings and click "Save & Run". A tool-tip notification will be displayed with the number of cards that it retired.
