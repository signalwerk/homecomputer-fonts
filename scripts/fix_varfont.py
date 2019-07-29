#!/usr/bin/env python3
# coding: utf-8

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import ROUND_XY_TO_GRID, USE_MY_METRICS


def fix_font(path, outpath, name0, name1, name3):
    f = TTFont(path)
    glyf_table = f["glyf"]

    # Fix glyf table

    for name, glyph in glyf_table.glyphs.items():
        glyph.expand(glyf_table)
        found_metrics = False
        _lsb, width = f["hmtx"][name]
        if glyph.isComposite() and hasattr(glyph, "components"):
            for c in glyph.components:

                # Unset the component rounding flag
                c.flags &= ~ROUND_XY_TO_GRID

                # Set the use my metrics flag if appropriate
                c.flags &= ~USE_MY_METRICS
                if not found_metrics and f["hmtx"][c.glyphName][1] == width:
                    c.flags |= USE_MY_METRICS
                    found_metrics = True

    # Merge STAT, gasp and name tables

    patch = TTFont()
    patch.importXML("../patch/patch.ttx")

    # Copy and patch name table
    name = patch["name"]
    name.setName(name0, 0, 3, 1, 0x409)
    name.setName(name1, 1, 3, 1, 0x409)
    name.setName(name3, 3, 3, 1, 0x409)
    name.setName(name3, 4, 3, 1, 0x409)
    name.setName(name3, 6, 3, 1, 0x409)
    f["name"] = name

    # Copy gasp and STAT tables
    f["gasp"] = patch["gasp"]
    f["STAT"] = patch["STAT"]

    f.save(outpath)
    f.saveXML(outpath + ".ttx")


fix_font(
    "../fonts/SixtyfourGX.ttf",
    "../fonts/Sixtyfour.ttf",
    u"Font Copyright 2008-2019 by Jens Kutilek. Based on the Commodore 64 character set.",
    u"Sixtyfour",
    u"2.000;JENS;Sixtyfour",
)

fix_font(
    "../fonts/WorkbenchGX.ttf",
    "../fonts/Workbench.ttf",
    u"Font Copyright 2008-2019 by Jens Kutilek. Based on the Amiga 500 Workbench 1.3 character set.",
    u"Workbench",
    u"2.000;JENS;Workbench",
)