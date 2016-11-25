import pygst
pygst.require('0.10')
import gst


#pipeline = gst.Pipeline("RadioPipe")

player = gst.element_factory_make("playbin2", "player")

#pipeline.add(player)

## Working uri for radio dj
#player.set_property('uri', 'http://radiodeejay-lh.akamaihd.net/i/RadioDeejay_Live_1@189857/index_96_a-b.m3u8?sd=10&rebase=on')

## Working uri for Virgin radio
#player.set_property('uri', 'http://icecast.unitedradio.it/Virgin.mp3')

## Working uri for RTL 102.5
player.set_property('uri', 'http://shoutcast.rtl.it:3010/')


player.set_state(gst.STATE_PLAYING)

bus = player.get_bus()
msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
    gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
print msg


#print "Ci siamo?!"
