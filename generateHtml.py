#!/usr/bin/env python
import os
import argparse
import datetime
import subprocess
import contextlib

import jinja2
import packaging.utils

parser = argparse.ArgumentParser()
parser.add_argument(
    'wheel',
    type=lambda path: os.path.basename(path),
    help='Path to wheel. Will be used to determine the version. It can also be just the wheel filename.'
)
parser.add_argument(
    'outputDir',
    help='Directory where HTML files will be rendered to.'
)

args = parser.parse_args()

_, version, _, _ = packaging.utils.parse_wheel_filename(args.wheel)

commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], universal_newlines=True, cwd='OpenTimelineIO')
commitISOTime = subprocess.check_output(['git', 'show', '-s', '--format=%cI', 'HEAD'], universal_newlines=True, cwd='OpenTimelineIO')

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("public"),
    autoescape=jinja2.select_autoescape()
)

with contextlib.suppress(FileExistsError):
    os.makedirs(args.outputDir)

for templateName in ['index', 'console']:
    template = env.get_template(f'{templateName}.html.in')

    with open(f'{args.outputDir}/{templateName}.html', 'w') as fd:
        fd.write(
            template.render(
                version=str(version),
                commit=commit.strip(),
                wheel=args.wheel,
                originalTimestamp=commitISOTime.strip(),
                utcTimestamp=datetime.datetime.fromisoformat(commitISOTime.strip()).astimezone(datetime.timezone.utc)
            )
        )
