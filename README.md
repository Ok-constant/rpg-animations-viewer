# RPG animations viewer

A tool to decrypt and watch rpg maker games' animations

# Requirements

Like every project here, you first need to install everything.
Follow the instructions here to install python.
Then make sure you have installed these packages using pip install [package name]

+ opencv-python
+ Pillow

# How to use

+ [Gif maker](#gif-maker)
+ [Gif viewer](#gif-viewer)

## Gif maker

Making gifs<br>

+ [Making a single gif](#making-a-single-gif)
+ Other modes coming soon

### Making a single gif

To make a single gif out of multiple frames, first you have to edit the `animation.json` file<br>

here's what you need to edit<br>
```json
{
    "path":"the path of the folder that contains the files",
    "templ":"the first part of the files' names",
    "ext":"the files' extension",
    "range":"the range of the files",
    "out":"the file name of the gif created",
    "out_path":"the path of the folder where the gif will be",
    "type":"mode (later explained)"
}
```

All of the games I've tried use this way to save frames for animations:<br>
`[something]_[other details]_[animation number]_[frame number].[extension]`

This is an example of some frames:<br>
+ `01_monster_01_00.rpgmvp`
+ `01_monster_01_01.rpgmvp`
+ `01_monster_01_02.rpgmvp`
+ `01_monster_01_03.rpgmvp`

This is the first animation of a certain monster<br>
You can see the animation has a range of numbers at the end, from 0 to 3<br>
These are sequencially the frames of the animations, so this is what you need to put in the `range` field (in this case 0-3)<br>
For the `templ` field you just have to put everything that comes before the numbers, in this case `01_monster_01_0`.<br>

By still using the example above, the animation.json file would be

```json
{
    "path":"C:\\Users\\someone\\game\\images\\",
    "templ":"01_monster_01_0",
    "ext":"rpgmvp",
    "range":"0-3",
    "out":"gif",
    "out_path":"C:\\Users\\someone\\gifs\\",
    "type":"frames"
}
```

Some games may not have multiple frames, for example you may have just

+ `01_monster_01_00.rpgmvp`

In this case just edit the `range` field with `"0-0"`

### How to run

To run the project, after you've edited the `animation.json` file<br>
Just run:<br>

`python gif_maker.py animation.json`

## Gif viewer

