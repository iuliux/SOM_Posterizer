Image posterizer using Self Organizing Maps
===========================================

Usage:
------

Sample run:

    > python posterize.py imgs/1.jpg

The resulting posterized image will be displayed and saved with the name
`orig-image-name_sgm.extension` in the same folder as the original image.

Also, a nice plot could be activated in `posterize.py`, add `do_plot=True` to
the arguments of the `posterize()` function calling (in main)

TODO: add a command line flag for plot enabling
