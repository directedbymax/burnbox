# BurnBox Release Process

Unless you're a core BurnBox developer making a release, you'll probably never need to follow it.

## Preparing the release

### Update the version in these places

- [ ] `cli/pyproject.toml`
- [ ] `cli/burnbox_cli/resources/version.txt`
- [ ] `desktop/pyproject.toml`
- [ ] `desktop/setup.py`
- [ ] `desktop/chat.hideaway.burnbox.appdata.xml`
- [ ] `docs/source/conf.py` (`version` at the top, and the `versions` list too)
- [ ] `snap/snapcraft.yaml`

### You also must edit these files

- [ ] `desktop/chat.hideaway.burnbox.appdata.xml` should have the correct release date, and links to correct screenshots
- [ ] `CHANGELOG.md` should be updated to include a list of all major changes since the last release

### Update dependencies

Check `cli/pyproject.toml` to see if any hard-coded versions should be updated. Then, update the dependencies like this:

```sh
cd cli
poetry update
cd ..
```

If you update `flask-socketio`, ensure that you also update the [socket.io.min.js](https://github.com/micahflee/burnbox/blob/develop/cli/burnbox_cli/resources/static/js/socket.io.min.js) file to a version that is [supported](https://flask-socketio.readthedocs.io/en/latest/#version-compatibility) by the updated version of `flask-socketio`.

Check `desktop/pyproject.toml` to see if any hard-coded versions should be updated. Then, update the dependencies like this:

```
cd desktop
poetry update
cd ..
```

Update the docs dependencies like this:

```
cd docs
poetry update
cd ..
```

Update the versions of `meek`, `obfs4proxy`, and `snowflake` in the `desktop/scripts/build-pt-*` scripts, both the bash and PowerShell scripts. You can find the latest versions by looking at the tags in their git repos: [meek](https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/meek/-/tags), [obfs4proxy](https://gitlab.com/yawning/obfs4/-/tags), [snowflake](https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/snowflake/-/tags).

### Update the documentation

- [ ] Update all of the documentation in `docs` to cover new features, including taking new screenshots if necessary

### Finalize localization

- [ ] Merge all the translations from weblate:
      ```
      git remote add weblate https://hosted.weblate.org/projects/burnbox/translations/
      git pull weblate main
      ```
- [ ] In `docs` run `poetry run ./check-weblate.py [API_KEY]` to see which translations are >90% in the app and docs
- [ ] Edit `cli/burnbox_cli/settings.py`, make sure `self.available_locales` lists only locales that are >90% translated
- [ ] From the `desktop` folder in the virtual env, run `./scripts/countries-update-list.py` to make sure the localized country list for censorship circumvention is available in all available languages
- [ ] Edit `docs/source/conf.py`, make sure `languages` lists only languages that are >90% translated
- [ ] Edit `docs/build.sh` and make sure `LOCALES=` lists the same languages as above, in `docs/source/conf.py`
- [ ] Make sure the latest documentation is built and committed:
  ```
  cd docs
  poetry install
  poetry run ./build.sh
  ```

### Make sure Snapcraft packaging works

Ensure you have the ability to run `poetry export`. You may need to run `poetry self add poetry-plugin-export@latest`, as in recent versions of Poetry it is now a plugin rather than in the core.

Enter the `cli` directory and run `poetry export > ../snap/local/cli-requirements.txt`

Enter the `desktop` directory and run `poetry export > ../snap/local/desktop-requirements.txt`. Now edit this file and remove the first line that has a `-e` with a path to the `cli` folder - we don't want it.

In `snap/snapcraft.yaml`:

- [ ] Update the version number near the top of the file.
- [ ] The `tor`, `libevent`, `obfs4`, `snowflake-client`, and `meek-client` parts should be updated if necessary

To test locally:

- Install snapcraft with: `sudo snap install snapcraft --classic`
- Build snap with: `snapcraft`
- Install with: `sudo snap install ./burnbox_${VERSION}_amd64.snap --devmode`

To test in the edge branch:

With every commit to the `main` branch, Snapcraft's CI should trigger builds. If you just merged to `main` and consider this to be what will become the new version's 'tag', you can also click 'Trigger a build' in the Snapcraft.io web interface.

Make sure the builds all succeeded at https://snapcraft.io/burnbox/builds (you must be logged in), and test them. You can install them with: `snap install burnbox --edge`

### Make sure the Flatpak packaging works

In `flatpak/chat.hideaway.burnbox.yaml`:

- [ ] Update `tor` and `libevent` 
- [ ] Update `obfs4proxy`, `meek-client`, and `snowflake-client` dependencies. To do this, edit the script `flatpak/generate-golang-dependencies.py` and make sure that the repository URLs and tags are the latest versions. Then run this command from the root of the burnbox repository folder:

  ```sh
  ./flatpak/generate-golang-dependencies.py
  ```

- [ ] Update the Python dependencies. This is super hacky. You need to use both the poetry and pip parts of [this tool](https://github.com/flatpak/flatpak-builder-tools), but the version from [this PR](https://github.com/flatpak/flatpak-builder-tools/pull/353):
  ```sh
  # get burnbox-cli dependencies
  cd flatpak-build-tools/poetry
  ./flatpak-poetry-generator.py ../../burnbox/cli/poetry.lock --production
  ../flatpak-json2yaml.py ./generated-poetry-sources.json
  mv generated-poetry-sources.yml burnbox-cli.yaml

  # get burnbox dependencies
  cd flatpak-build-tools/pip
  ./flatpak-pip-generator $(../../burnbox/flatpak/poetry-to-requirements.py ../../burnbox/desktop/pyproject.toml | grep -v PySide6)
  ../flatpak-json2yaml.py ./python3-modules.json
  mv python3-modules.yml burnbox-desktop.yaml
  ```

  Now, move `burnbox-desktop.yaml` and `burnbox-cli.yaml` into the `flatpak/` folder. For the `burnbox-cli.yaml` file, adjust the `pip3 install` step so that it includes the `--use-pep517` argument.

- [ ] Build and test the Flatpak package to ensure it works:
  ```sh
  flatpak-builder build --force-clean --jobs=$(nproc) --install-deps-from=flathub --install --user flatpak/chat.hideaway.burnbox.yaml
  flatpak run chat.hideaway.burnbox
  ```

### Create a signed git tag

- [ ] There must be a PGP-signed git tag for the version, e.g. for BurnBox 2.1, the tag must be `v2.1`

The first step for the Linux, macOS, and Windows releases is the same.

Verify the release git tag:

```sh
git fetch
git tag -v v$VERSION
```

If the tag verifies successfully, check it out:

```sh
git checkout v$VERSION
```

## Making the release

### Linux Snapcraft release

From https://snapcraft.io/burnbox/releases (you must be logged in), find the release that corresponds to the recent builds that ran against our `main` branch (the Build ID mentioned can be cross-referenced to the build log, as the ID appears in the log). You can then 'promote' that release from latest/edge to latest/beta, then latest/candidate, then latest/stable.

### Linux Flatpak release

- [ ] Create a new branch in https://github.com/flathub/chat.hideaway.burnbox for the version
- [ ] Overwrite the manifest in the flathub repo with the updated version in [flatpak/chat.hideaway.burnbox.yaml](./flatpak/chat.hideaway.burnbox.yaml)
- [ ] Edit it so that the sources for `burnbox` and `burnbox-cli` are the GitHub repo, with the correct git tag, rather than the local filesystem
- [ ] Ensure you also copy across the `burnbox-cli.yaml`, `burnbox-desktop.yaml`, `meek-client`, `snowflake` and `obfs4proxy` from the `flatpak/` folder into the flathub repository, so that the flathub repository has all the latest dependencies.
- [ ] Make a PR in the flathub repo, and merge it to make a release

### Windows release

Create a Windows 11 VM, and set it up like this:

- Install [git for Windows](https://git-scm.com/download/win).
- Install the latest version of 3.12 [from python.org](https://www.python.org/downloads/).
- Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), making sure to check "Desktop development with C++".
- Download and install [7-Zip (x64)](https://7-zip.org/). Add `C:\Program Files\7-Zip` to your path.
- Download and install [gpg4win](https://gpg4win.org/). Add `C:\Program Files (x86)\GnuPG\bin` to your path.
- Install the Windows SDK from here: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/.
- Go to https://dotnet.microsoft.com/download/dotnet-framework and download and install .NET Framework 3.5 SP1 Runtime. I downloaded `dotnetfx35.exe`.
- Go to https://wixtoolset.org/docs/wix3/ and download and install WiX toolset. I downloaded `wix314.exe`. Add `C:\Program Files (x86)\WiX Toolset v3.14\bin` to the path.

Clone the BurnBox git repo and checkout the release tag.

If you've used this git repo for a previous release, clean it up:

- In the `burnbox/desktop` folder, delete `build` and `dist` from the previous build.
- Delete the poetry environment. You can find its name by run `poetry env list`, and then you can delete it with `poetry env remove [ENV_NAME]`.

Install Poetry and deps. Open a Developer PowerShell for VS window, change to the `burnbox` folder, and run:

```powershell
cd desktop
pip install poetry
poetry install
```

Github Actions will build the binaries. Find the Github Actions `build` workflow, switch to the summary tab, download `win64-build.zip`, and copy it to the Windows packaging environment.

Extract `win64-build.zip`. Run:

```
poetry run python .\scripts\build-windows.py codesign [path]
poetry run python .\scripts\build-windows.py package [path]
```

This will create:

- `desktop/dist/BurnBox-win64-$VERSION.msi`

### macOS release

In order to make a universal2 binary, you must following these instructions using a Mac with Apple Silicon. To keep a clean environment, you can use VM.

Set up the VM like this:

- Install [Homebrew](https://brew.sh/)
- `brew install create-dmg libiodbc`
- Install the latest Python 3.12 from https://www.python.org/downloads/
- Install ARM64 version of Go from https://go.dev/dl/
- Install "Postgres.app with PostgreSQL 16 (Universal)" from https://postgresapp.com/downloads.html

Clone the BurnBox git repo and checkout the release tag.

If you've used this git repo for a previous release, clean it up:

```sh
cd desktop
rm -rf build dist
# Delete the old poetry environment
/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry env remove $(poetry env list | grep "(Activated)" | cut -d" " -f1)
```

Install and build dependencies:

```sh
cd desktop
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m pip install poetry
/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry install
/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry run python ./scripts/get-tor.py macos
./scripts/build-pt-obfs4proxy.sh
./scripts/build-pt-snowflake.sh
./scripts/build-pt-meek.sh
```

Make the Apple Silicon app bundle:

```sh
/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry run python ./setup-freeze.py bdist_mac
/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry run python ./scripts/build-macos.py cleanup-build
```

The Apple Silicon app bundle will be in `build` folder called `BurnBox.app`.

Github Actions will build the Intel app bundle. Find the Github Actions `build` workflow, switch to the summary tab, and download the `mac-intel-build` artifact. Extract it, and you'll get the Intel `BurnBox.app` folder.

Let's create some consistent directories for the next step:

```sh
mkdir ~/tmp/intel
mkdir ~/tmp/arm64
mkdir ~/tmp/universal
```

Now move the `build/BurnBox.app` into `~/tmp/arm64`, and extract the Intel .app from the Github Actions build artifact above, and move it into `~/tmp/intel`.

Next, merge these two app bundles into a single universal2 app bundle:

```sh

/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry run ./scripts/macos-merge-universal.py ~/tmp/intel/BurnBox.app ~/tmp/arm64/BurnBox.app ~/tmp/universal/BurnBox.app
```

You will need to have obtained a Developer ID Certificate from our Apple team account. The 'Development certificates' don't work for production-ready code-signing.

Only Glenn as the 'Account Holder' can request Developer ID certs, so you will need to provide him a CSR to do so. Refer to https://developer.apple.com/help/account/create-certificates/create-developer-id-certificates/ and https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request/ . The private key will be in your keychain. Glenn can send you the cert once it's issued, and you should add that to your keychain too.

Finally, code sign and package the universal2 app bundle.

```sh
/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry run python ./scripts/build-macos.py codesign ~/tmp/universal/BurnBox.app
/Library/Frameworks/Python.framework/Versions/3.12/bin/poetry run python ./scripts/build-macos.py package ~/tmp/universal/BurnBox.app
```

The will create `dist/BurnBox-$VERSION.dmg` in the `desktop` directory that you're still cd'd into.

Now, notarize the release. You will need an app-specific Apple ID password set up. You will also need to change the `--apple-id` to your Apple ID email. The team ID below, however, is consistent to all of us, it's the Science & Design team ID.

```sh
export APPLE_PASSWORD="changeme" # This must be an app-specific Apple ID password, not your main Apple ID password
export VERSION=$(cat ../cli/burnbox_cli/resources/version.txt)

# Notarize it
xcrun notarytool submit --apple-id "you@example.com" --team-id 7WLJ4UBL5L --password "$APPLE_PASSWORD" --progress --wait dist/BurnBox-$VERSION.dmg
```

If this is your first time notarizing with this Apple ID, it can take a very long time (like 9 hours), because Apple builds up a sort of 'signature' of your request and this kind of app. All subsequent notarizations (for future releases) should be much faster (a couple of minutes).

```sh
# After it's approved, staple the ticket
xcrun stapler staple dist/BurnBox-$VERSION.dmg
```

This will (re)create `desktop/dist/BurnBox-$VERSION.dmg`, signed and notarized. The dmg is now ready for release.

### Source package

To make a source package, run `./build-source.sh $TAG`, where `$TAG` is the name of the signed git tag, e.g. `v2.1`.

This will create `dist/burnbox-$VERSION.tar.gz`.

## Publishing the release

### PGP signatures

After following all of the previous steps, gather these files:

- `burnbox_${VERSION}_amd64.snap`
- `BurnBox.flatpak` (rename to `BurnBox-$VERSION.flatpak`)
- `BurnBox-win64-$VERSION.msi`
- `BurnBox-$VERSION.dmg`
- `burnbox-$VERSION.tar.gz`

Create a PGP signature for each of these files, e.g:

```sh
gpg -a --detach-sign BurnBox-$VERSION.tar.gz
gpg -a --detach-sign [... and so on]
```

### Create a release on GitHub:

- Match it to the version tag, put the changelog in description of the release
- Upload all 8 files (binary and source packages and their `.asc` signatures)

### Update burnbox-cli on PyPi

```sh
cd cli
poetry install
poetry publish --build
```

### Update Homebrew

- Make a PR to [homebrew-cask](https://github.com/homebrew/homebrew-cask) to update the macOS version

### Update burnbox.hideaway.chat

- Upload all 10 files to https://burnbox.hideaway.chat/dist/$VERSION/
- Update the [burnbox-website](https://github.com/micahflee/burnbox-website) repo:
  - Edit `latest-version.txt` to match the latest version
  - Update the version number and download links
  - Deploy to https://burnbox.hideaway.chat/

### Update docs.burnbox.hideaway.chat

- Upload everything from `docs/build/docs` to https://docs.burnbox.hideaway.chat/

### Update the community

- Blog, toot, etc.
