# uketabs
A very simple and quick command line ukulele ascii tab editor

This editor is intended to be a quick way to write down a ukulele solo. This style of tab does not represent rhythms, decorations, or strumming. For sharing, teaching, or remembering music over long periods of time, these tabs should be paired with videos. 

## Run

`python uketabs.py`

## Commands

##### `help`
show this help message

##### `exit` / `quit` / `q` 
exit program

##### `load [filename]`
load ascii tab file that has been created with this editor

##### `save [filename]`
save tab as plain text file

if filename unspecified, overwrites last exported file

##### `new`
create blank document

##### `show`
display current tab 

##### `mpl [measures per line]`
adjust measures displayed per line (default = 4)

##### `autospace`
toggle autospace mode (default = ON) 

autospace mode: a blank column is automatically appended whenever a non-blank column is added

##### `bar` / `b` 
append a new measure

##### `barline [measure #] [column #]`
insert a barline at the specified measure and column

##### `del barline [measure #]`
delete the barline before the specified measure

##### `[column]`
append a new column to the last measure

specify columns with four space-separated tokens, in top-down order, for example:
    
    1
    |-||
    |-||
    |-||
    |-|| 
   
    >> 2 3 2 0
    1
    |-2-||
    |-3-||
    |-2-||
    |-0-||

    >> - - - 4
    1
    |-2---||
    |-3---||
    |-2---||
    |-0-4-||

    >> 7- 8- 9- 10
    1
    |-2---7--||
    |-3---8--||
    |-2---9--||
    |-0-4-10-||

unspecified tokens are interpreted as '-', for example:

    1
    |-||
    |-||
    |-||
    |-|| 
   
    >> - 3
    1
    |---||
    |-3-||
    |---||
    |---||

    >> 4
    1
    |---4-||
    |-3---||
    |-----||
    |-----||

    >>
    1
    |---4--||
    |-3----||
    |------||
    |------||

columns can also be specified with chord names. the most common fingering will be applied. all major, minor, and 7 chords supported. examples:

    1
    |-||
    |-||
    |-||
    |-|| 
   
    >> F
    1
    |-0-||
    |-1-||
    |-0-||
    |-2-||

    >> Am
    1
    |-0-0-||
    |-1-0-||
    |-0-0-||
    |-2-2-||

    >> G7
    1
    |-0-0-1-||
    |-1-0-2-||
    |-0-0-1-||
    |-2-2-0-||

    >> Bb
    1
    |-0-0-1-1-||
    |-1-0-2-1-||
    |-0-0-1-2-||
    |-2-2-0-3-||

##### `del` / `d`
delete the last column of the last measure (when in autospace mode, deletes last two columns)

##### `del measure [measure #]`
delete the given measure

##### `insert measure [measure #]`
insert a blank measure at a given location

##### `copy measure [measure #]`
copy the given measure to the clipboard

##### `copy range [begin] [end]`
copy the range of measures to the clipboard

##### `paste`
append the clipboard to the end of the tab

##### `paste insert [measure #]`
insert the clipboard at the specified measure number

##### `insert [measure #] [column #] [column]`
insert a column in the given measure at the given column number

##### `edit [measure #] [column #] [column]`
replace the specified column with a new one

##### `del [measure #] [column #]`
delete the specified column

## What do the colors mean?
The program will always emphasize the last-made edit using colors.
Green indicates an addition, yellow an update to a column, and red a
deletion (between the two red columns).

## Todo
- Undo command (Edit history)
- Load file with command line argument
- Column entry shortcut without spaces
- Cursor
  - Move to specific spot, beginning, end, left, right, up, down
- More bar numbers when mpl is large
- Display columns per line instead of measure per line
- Repeats
- Stop the user from leaving without saving
- Look up specific command
- Autospace should change behavior for insert/del barline
