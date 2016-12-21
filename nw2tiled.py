
#  Copyright (c) 2016, Aeva M. Palecek

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.etree import ElementTree
from xml.dom import minidom

from nw_parser import DotNWParser
from graal_parser import DotGraalParser


def load_level(level_path):
    for parser in [DotNWParser, DotGraalParser]:
        try:
            return parser(level_path)
        except AssertionError:
            continue
    raise Exception("Unable to determine level file format: %s" % level_path)


def pretty_print(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def encode_as_csv(level):
    data = []
    for y in range(64):
        for x in range(64):
            tile_x, tile_y = level.board[x][y]
            tiled_index = (tile_x + (128 * tile_y)) + 1
            data.append(str(tiled_index))
        
    return ",".join(data)


def encode_as_tmx(level):
    root = Element('map')
    root.attrib['version'] = "1.0"
    root.attrib['orientation'] = "orthogonal"
    root.attrib['renderorder'] = "right-down"
    root.attrib['width'] = "64"
    root.attrib['height'] = "64"
    root.attrib['tilewidth'] = "16"
    root.attrib['tileheight'] = "16"
    root.attrib['nextobjectid'] = "1"

    tileset = SubElement(root, 'tileset')
    tileset.attrib['firstgid'] = "1"
    tileset.attrib['source'] = "pics1.tsx"

    layer = SubElement(root, 'layer')
    layer.attrib['name'] = "map"
    layer.attrib['width'] = "64"
    layer.attrib['height'] = "64"

    data = SubElement(layer, 'data')
    data.attrib['encoding'] = "csv"
    data.text = encode_as_csv(level)

    return root


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "First argument must be a level file."
        exit()
        
    level_path = sys.argv[1]
    tiles_path = os.path.join("sprites", "pics1.png")
    if len(sys.argv) >= 3:
        tiles_path = sys.argv[2]

    level_name = os.path.split(level_path)[-1]
    if len(sys.argv) >= 4:
        level_name = sys.argv[3]
    out_path = os.path.join("out", level_name + ".tmx")

    for path in [level_path, tiles_path]:
        if not os.path.isfile(path):
            print "No such file: " + path
            exit()

    level = load_level(level_path)
    tmx = encode_as_tmx(level)

    with open(out_path, 'w') as output:
        output.write(pretty_print(tmx))
