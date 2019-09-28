# uketabs
A very simple, quick, free command line ukulele tab editor

This editor is intended to be a quick way to write down a ukulele solo. This style of tab does not represent rhythms or decorations. For sharing, teaching, or remembering music over long periods of time, these tabs should be paired with videos.

## Run

`python uketabs.py`

## Commands

`help`\
    show this help message\
`exit` / `quit` / `q`\
    exit program\
`load [filename]`\
    load tab file that has been saved with this editor\
`save [filename]`\
    save tab as pickle file that can be reloaded with this editor\
    if filename unspecified, overwrites last loaded or saved file\
`export [filename]`\
    save tab as plain text file\
    if filename unspecified, overwrites last exported file\
`new`\
    create blank document\
`show`\
    display current tab\
`mpl [measures per line]`\
    adjust measures displayed per line (default = 4)\
`autospace`\
    toggle autospace mode (default = ON)\
    autospace mode: a blank column is automatically appended whenever
    a non-blank column is added\
`bar` / `b`\
    append a new measure\
`[column]`\
    append a new column to the last measure\
    specify columns with four space-separated tokens, in top-down order\
        for example:\
        `2 3 2 0`\
        `- - - 4`\
        `7- 8- 9- 10`\
    unspecified tokens are interpreted as '-'\
        for example:\
        `- 3` becomes `- 3 - -`\
        `4` becomes `4 - - -`\
        a blank line becomes `- - - -`\
    columns can also be specified with chord names\
    the most common fingering will be applied\
    all major, minor, and 7 chords supported\
        examples:\
        `F` becomes `0 1 0 2`\
        `Am` becomes `0 0 0 2`\
        `G7` becomes `1 2 1 0`\
        `Bb` becomes `1 1 2 3`\
`del`\
    delete the last column of the last measure\
`del measure [measure #]`\
    delete the given measure\
`insert measure [measure #]`\
    insert a blank measure at a given location\
`copy measure [measure #]`\
    copy the given measure to the clipboard\
`copy range [begin] [end]`\
    copy the range of measures to the clipboard\
`paste`\
    append the clipboard to the end of the tab\
`paste insert [measure #]`\
    insert the clipboard at the specified measure number\
`insert [measure #] [column #] [column]`\
    insert a column in the given measure at the given column number\
`edit [measure #] [column #] [column]`\
    replace the specified column with a new one\
`del [measure #] [column #]`\
    delete the specified column
