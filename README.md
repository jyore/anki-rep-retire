anki-rep-retire
===============

This add-on allows you to automatically retire cards after they grow past a certain interval. At a certain point, the knowledge on any given card will be committed to memory or has material that is intrinsically covered through other cards. Continuing to rep cards at this level of maturity is not worth the time spent reviewing when comparing what benefit you are gaining from the review. 

By using this add-on, you can tailor a specific threshold for each one of your decks. When reviewing cards from a deck, if a card's new interval exceeds the configured threshold, then that card will be `retired`. A `retired` card will be automatically suspended and tagged so that you no longer will see this card in reps and that you can easily find a whole list of retired cards in the browser. If you want to practice a retired card again, you can simply unsuspend and remove the tag, then reset the card.

> **Note**: The mobile app cannot run add-ons, so you cannot gain the benefit from the automatic trigger that runs after a review  when using anki mobile. To run the retire algorithm over all cards, simply open the add-on configuration menu on desktop anki after syncing all of your reviews and hit the `Save & Run` button. This will retire all cards that need to be retired from your mobile review session.



# Support

Anki Version Support
- For Anki 2.0, use Version 1.0.0-final or lower
- For Anki 2.1, use Version 2.0.0-beta or higher

This document will only cover Anki 2.1 support. For Anki 2.0, please load a previous tag.



# Installing Rep Retire

Installing this add-on is done by following these steps:

- Visit the [Releases](https://github.com/jyore/anki-rep-retire/releases) page
- Download the latest release
- Extract the downloaded zip file
- Copy the deflated directory to the addons21 folder
- Restart Anki


# Running Rep Retire

After installing, by default, Rep Retire is disabled for all decks. You must open the configuration menu to enable and configure thresholds for each deck you wish to enable automatic-retiring on.

Defaulting the add-on to off was done inentionally to minimize the impact the add-on may have before users have had the opportunity to configure everything how they desire.

To begin configuring Rep Retire, in Anki, do the following:
- Click `Tools->Add-ons`
- Select `Rep Retire` and click "configure"
- Update the settings as desired (see below)
- Save the changes


## Configuration Details

When you open the confiuration menu, you will be presented with a json file, detailing configuration for all of your decks. The settings are organized by the internal deck id to avoid any issues with naming collisions between decks or profiles. It should looks similar to the following:

~~~
{
    "1": {
        "enabled": false,
        "name": "Default",
        "tag": "RETIRED",
        "threshold": 40
    },
    "1521988881021": {
        "enabled": false,
        "name": "Japanese",
        "tag": "RETIRED",
        "threshold": 40
    }
}
~~~

> **Note:** The default deck is given the id of '1' by anki. This is somewhat a special deck and should probably be avoided, if possible. If you switch profiles, the default deck will always have the same id, so the settings will not be unique per-profile unless you use a different deck.


Locate the settings of the deck you wish to use by finding the "name" field that corresponds to the deck name. Set the following settings as desired:

- **enabled**: Set whether or not the add-on will trigger for this deck
- **threshold**: The threshold, in days, in which a card will be retired if the next interval exceeds it
- **tag**: The tag to add to the card when being retired




## Reviewing w/ Rep Retire

Once Rep Retire is enabled for a deck, it will execute the algorithm after every card has been answered correctly to determine if it should be retired or not. It if is retired, you will receive a tool-tip notification that the card was retired. When saving configuration settings, it will run the algorithm over all enabled decks and retire any cards it determines to need retiring. Again, for those who review on Anki mobile, to retroactively retire cards, open anki desktop, open the Rep Retire Configuration settings and click "Save & Run". A tool-tip notification will be displayed with the number of cards that it retired.



## Manually Triggering a Run

Simply click `Tools->Run Rep Retire` and it will retire cards from all decks, based on your settings.
