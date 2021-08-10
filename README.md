# prsconv3
Convert Tombo files to CSV

## Usage

To get this code, run
```bash
git clone https://github.com/Chris-Kimmel/prsconv3
```
Make sure you have Tombo and Pandas installed.

To run this code, navigate to the directory that contains this README. Then type any of these commands:

> To list available commands
> ```
> python . --help
> ```

> To extract events tables from fast5s:
> ```bash
> python . events tests/files/fast5_dir out.csv
> ```

> To convert `.tombo.stats` files to CSV format
> ```bash
> python . stats tests/files/stats/23456_WT_cellular.tombo.stats out.csv
> ```

_Note_: To run this script from another filepath, the user must replace "`.`" with the path to the directory that contains this README file. For example, the user might run `python /fs/project/PAS1405/kimmel/projects/prsconv3 --help`.

## Bugs

Please report any bugs on the GitHub issues page (https://github.com/Chris-Kimmel/prsconv3/issues). Even if they don't get fixed, it's helpful to have a list of everything wrong with the code. Poorly documented features also warrant an issue.

## Roadmap
- [x] Start with prscovn2.py. Update its CLI in a way that makes sense for a tool that will accept multiple kinds of file input, not just `.tombo.per_read_stats` files. Make the user specify long or wide-format output for `.tombo.per_read_stats` files.
- [x] Add browser-file-->CSV converters (wiggle and bedgraph).
- [x] Add direct `.tombo.stats`-->CSV converter
- [x] Add engine to extract events tables from fast5s
- [ ] Make a user-friendlier interface and improve documentation
- [ ] Get test coverage as high as I can (or add any tests at all)
- [ ] Package and upload to PyPI
- [ ] Extract additional info from fast5s, such as ammeter sampling frequency and available corrected groups
- [ ] Set up some kind of CI tool
