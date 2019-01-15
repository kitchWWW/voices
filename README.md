# Voices
idk man I need a name for it. Taking suggestions.

A short script that combines the instruction fragments found in `audio/` in to longer audio files that instruct the performers.

All performers stand on stage with headphones and listen to their own sets of instructions. (`out/<timestamp>/part_no_#.wav`) The majority of the compute time comes from using the utility `lame` to convert the `.wav` files to `.mp3`.

A sample score, short score, and parts are available in `sampleOut`.