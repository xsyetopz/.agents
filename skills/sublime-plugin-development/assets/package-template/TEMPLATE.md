# Sublime Text package starter

Replace `Example`, `example`, command IDs, settings, and descriptions consistently. Keep `.python-version` at `3.8` only when that is the selected stable API environment. Remove keybindings or resources that are not part of the requested UX.

Pure logic can be tested with:

```sh
python3 -m unittest discover -s tests
```

The Sublime integration still requires a clean-profile package reload/install smoke test.
