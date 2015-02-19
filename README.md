# revu

Help review your patches!

## Quickstart

```
mkvirutalenv --python=$(which python3.4) revu
workon revu
# You might need to install libgit2-dev & libffi-dev
pip install -r requirements.txt
python setup.py develop
```

Now, visit [GitHub's Settings Page](https://github.com/settings/applications)
and generate a new token. Copy that token to `~/.github.key`.

Next, write a `~/.revu.conf`, such as:

```
[hy]
repo = hylang/hy
path = /home/tag/dev/local/hy

[openstates]
repo = sunlightlabs/openstates
path = /home/tag/dev/sunlight/openstates
```

## Using revu

First, be sure that you're in your virtualenv by doing a `workon revu`.

Next, you can run `revu hy` to start a `revu` session. Open another terminal
and type in `tmux attach-session -t revu`. This pane will be controled by the
`revu` controller.

Some good first commands: `log`, `comments`, or `diff`.

![](http://i.imgur.com/zh0gajE.jpg)
