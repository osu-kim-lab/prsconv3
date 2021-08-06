# prsconv3
Convert Tombo files to CSV

## Roadmap
- [x] Start with prscovn2.py. Update its CLI in a way that makes sense for a tool that will accept multiple kinds of file input, not just `.tombo.per_read_stats` files. Make the user specify long or wide-format output for `.tombo.per_read_stats` files.
- [x] Add browser-file-->CSV converters (wiggle and bedgraph).
- [x] Add direct `.tombo.stats`-->CSV converter
- [x] Add engine to extract events tables from fast5s
- [ ] Get test coverage as high as I can (or add any tests at all)
- [ ] Package and upload to PyPI
- [ ] Set up some kind of CI tool
- [ ] Extract additional info from fast5s, such as ammeter sampling frequency and available corrected groups
