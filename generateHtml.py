#!/usr/bin/env python
import os
import sys
import subprocess

import jinja2
import packaging.utils


wheel = os.path.basename(sys.argv[1])
outputDir = sys.argv[2]

_, version, _, _ = packaging.utils.parse_wheel_filename(wheel)

commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], universal_newlines=True)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("public"),
    autoescape=jinja2.select_autoescape()
)

os.makedirs(outputDir)

for templateName in ['index', 'console']:
    template = env.get_template(f'{templateName}.html.in')

    with open(f'{outputDir}/{templateName}.html', 'w') as fd:
        fd.write(template.render(version=str(version), commit=commit.strip(), wheel=wheel))
